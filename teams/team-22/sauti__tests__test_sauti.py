import json
from datetime import date
from http.server import HTTPServer
from pathlib import Path
import sys
from threading import Thread
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

# Make discovery work both from the repository root and from ``sauti/``.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sauti import handler_for
from sauti_model import format_reply, interpret_prediction, normalize_words


class SautiTests(unittest.TestCase):
    def setUp(self):
        self.seen = []

        def respond(message):
            self.seen.append(message)
            if message == "hitilafu":
                raise RuntimeError("model temporarily unavailable")
            if message == "chaguo":
                return {
                    "reply": "Unataka kuona ratiba yako au kuongeza tukio?",
                    "choices": [
                        {
                            "label": "Angalia ratiba",
                            "reply": "Nimeelewa kuwa unataka kuangalia ratiba yako.",
                            "frame": {"intent": "calendar_query", "slots": []},
                        },
                        {
                            "label": "Ongeza tukio",
                            "reply": "Nimeelewa kuwa unataka kuongeza tukio kwenye ratiba yako.",
                            "frame": {"intent": "calendar_set", "slots": []},
                        },
                    ],
                }
            return format_reply("alarm_set", [{"type": "time", "value": "saa moja asubuhi"}])

        self.server = HTTPServer(("127.0.0.1", 0), handler_for(respond))
        self.thread = Thread(target=self.server.serve_forever)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.server.server_port}"
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.thread.join)
        self.addCleanup(self.server.shutdown)

    def post(self, payload):
        request = Request(self.url + "/api/reply", data=json.dumps(payload).encode(),
                          headers={"Content-Type": "application/json"})
        return urlopen(request, timeout=3)

    def test_interface_and_plain_language_reply(self):
        with urlopen(self.url, timeout=3) as response:
            page = response.read()
            self.assertIn(b'id="composer"', page)
            self.assertIn(b'id="character-count"', page)
        with urlopen(self.url + "/app.js", timeout=3) as response:
            script = response.read()
            self.assertIn(b"Maelezo ya modeli", script)
            self.assertIn(b"result.choices", script)
        with self.post({"message": "  Weka kengele saa moja asubuhi. "}) as response:
            self.assertEqual(json.load(response), {
                "reply": "Nimeelewa kuwa unataka kuweka kengele.\nMuda: saa moja asubuhi",
            })
        self.assertEqual(self.seen, ["Weka kengele saa moja asubuhi."])

    def test_track_c_clarification_choices_and_frames_survive_api(self):
        with self.post({"message": "chaguo"}) as response:
            result = json.load(response)
        self.assertEqual(result["reply"], "Unataka kuona ratiba yako au kuongeza tukio?")
        self.assertEqual(
            [choice["frame"]["intent"] for choice in result["choices"]],
            ["calendar_query", "calendar_set"],
        )
        self.assertTrue(all(choice["frame"]["slots"] == [] for choice in result["choices"]))

    def test_track_c_choices_and_typo_normalization_preserve_original_frame(self):
        choices = interpret_prediction(
            [("calendar_set", 0.28), ("calendar_query", 0.25)], [], [], []
        )
        self.assertEqual(len(choices["choices"]), 2)
        self.assertEqual(
            [choice["frame"]["intent"] for choice in choices["choices"]],
            ["calendar_set", "calendar_query"],
        )

        original_words = [("Weka", (0, 4)), ("kenglee", (5, 12)), ("kehso", (13, 18))]
        corrected = normalize_words([word for word, _ in original_words])
        self.assertEqual(corrected, ["Weka", "kengele", "kesho"])
        slot = {"type": "date", "value": "kehso", "start": 13, "end": 18}
        result = interpret_prediction(
            [("alarm_set", 0.9), ("calendar_set", 0.05)],
            [slot], original_words, corrected,
        )
        self.assertEqual(result["frame"], {"intent": "alarm_set", "slots": [slot]})
        self.assertIn("Tarehe:", result["reply"])
        self.assertIn("kama", result["reply"])
        self.assertNotIn("\ufffd", result["reply"])

    def test_relative_date_is_explained_with_a_fixed_nairobi_calendar_date(self):
        reply = format_reply(
            "datetime_query", [{"type": "date", "value": "kesho"}],
            today=date(2026, 11, 12),
        )
        self.assertIn("Tarehe: 13 Novemba 2026 (kesho)", reply)

    def test_invalid_input_does_not_reach_model(self):
        for value in ("   ", "a" * 281, 123):
            with self.subTest(value=value), self.assertRaises(HTTPError) as error:
                self.post({"message": value})
            self.assertEqual(error.exception.code, 400)
            error.exception.close()
        self.assertFalse(self.seen)

    def test_model_failure_returns_retryable_error(self):
        with self.assertLogs(level="ERROR"), self.assertRaises(HTTPError) as error:
            self.post({"message": "hitilafu"})
        self.assertEqual(error.exception.code, 503)
        with error.exception as response:
            self.assertIn("Jaribu tena", json.load(response)["error"])
