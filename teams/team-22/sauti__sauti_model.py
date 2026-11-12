"""Load the datathon checkpoint and format Kiswahili replies and semantic frames."""

from datetime import datetime, timedelta
from importlib.util import module_from_spec, spec_from_file_location
import json
import re
import sys
from zoneinfo import ZoneInfo


TRACK_C_INTENTS = {
    "alarm_set",
    "calendar_query",
    "calendar_set",
    "datetime_query",
    "lists_createoradd",
    "lists_query",
    "news_query",
    "play_music",
    "qa_definition",
    "weather_query",
}
TRACK_C_SLOT_LABELS = {"O"} | {
    f"{prefix}-{slot_type}"
    for slot_type in ("location", "date", "time", "item", "term")
    for prefix in ("B", "I")
}


INTENTS = {
    "alarm_set": "kuweka kengele",
    "calendar_query": "kuangalia ratiba yako",
    "calendar_set": "kuongeza tukio kwenye ratiba yako",
    "datetime_query": "kujua tarehe au saa",
    "lists_createoradd": "kuunda orodha au kuongeza kipengee",
    "lists_query": "kuangalia kilicho kwenye orodha",
    "news_query": "kupata habari",
    "play_music": "kusikiliza muziki",
    "qa_definition": "kujua maana ya neno au dhana",
    "weather_query": "kujua hali ya hewa",
}
SLOTS = {"date": "Tarehe", "time": "Muda", "location": "Mahali", "item": "Kipengee", "term": "Mada"}

SPELLING = {
    "kehso": "kesho",
    "keshho": "kesho",
    "kenglee": "kengele",
    "kenegle": "kengele",
    "mkutnao": "mkutano",
}
INTENT_CUES = {"kengele": "alarm_set", "mkutano": "calendar_set"}
CALENDAR_CHOICES = {"calendar_query": "Angalia ratiba", "calendar_set": "Ongeza tukio"}
# Conservative cutoffs for this checkpoint's uncalibrated softmax scores.
CLARIFICATION_MAX_SCORE = 0.30
CLARIFICATION_MAX_GAP = 0.08
CLARIFICATION_MIN_PAIR_SCORE = 0.45
RELATIVE_DAYS = {"juzi": -2, "jana": -1, "leo": 0, "kesho": 1, "kesho kutwa": 2}
MONTHS = (
    "Januari", "Februari", "Machi", "Aprili", "Mei", "Juni",
    "Julai", "Agosti", "Septemba", "Oktoba", "Novemba", "Desemba",
)


def normalize_words(words):
    normalized = []
    for word in words:
        match = re.fullmatch(r"([^\w]*)([a-zA-Z]+)([^\w]*)", word)
        if not match or (corrected := SPELLING.get(match[2].lower())) is None:
            normalized.append(word)
            continue
        if match[2].isupper():
            corrected = corrected.upper()
        elif match[2][0].isupper():
            corrected = corrected.capitalize()
        normalized.append(match[1] + corrected + match[3])
    return normalized


def format_reply(intent, entities, *, today=None):
    action = INTENTS.get(intent)
    if action is None:
        return "Sijaelewa ombi hilo. Jaribu kuliandika kwa maneno mengine."
    details = []
    for entity in entities:
        kind, value = entity["type"], entity["value"]
        if kind not in SLOTS:
            continue
        if kind in {"date", "time"}:
            phrase = " ".join(normalize_words(value.casefold().split()))
            phrase = re.sub(r"^\W+|\W+$", "", phrase)
            offset = RELATIVE_DAYS.get(phrase)
            if offset is not None:
                if today is None:
                    today = datetime.now(ZoneInfo("Africa/Nairobi")).date()
                date = today + timedelta(days=offset)
                details.append(f"Tarehe: {date.day} {MONTHS[date.month - 1]} {date.year} ({phrase})")
                continue
        details.append(f"{SLOTS[kind]}: {value}")
    return "\n".join([f"Nimeelewa kuwa unataka {action}.", *details])


def interpret_prediction(ranked, entities, words, corrected):
    """Return a reply, or offer choices when the scores give little guidance."""
    (intent, score), (alternative, runner_up) = ranked
    if score < CLARIFICATION_MAX_SCORE and score - runner_up < CLARIFICATION_MAX_GAP:
        if score + runner_up < CLARIFICATION_MIN_PAIR_SCORE:
            return {"reply": "Sijaelewa ombi lako vizuri. Unaweza kuliandika kwa maneno mengine?"}
        if {intent, alternative} == CALENDAR_CHOICES.keys():
            question = "Unataka kuona ratiba yako au kuongeza tukio?"
        else:
            question = "Sijaelewa ombi lako vizuri. Unataka kufanya nini?"
        return {
            "reply": question,
            "choices": [
                {"label": CALENDAR_CHOICES.get(choice, INTENTS[choice].capitalize()),
                 "reply": explain_prediction(choice, entities, words, corrected),
                 "frame": {"intent": choice, "slots": entities}}
                for choice in (intent, alternative)
            ],
        }
    return {
        "reply": explain_prediction(intent, entities, words, corrected),
        "frame": {"intent": intent, "slots": entities},
    }


def explain_prediction(intent, entities, words, corrected):
    notes = []
    for (original, (start, end)), replacement in zip(words, corrected):
        clean = re.sub(r"^\W+|\W+$", "", replacement).casefold()
        if original == replacement:
            continue
        relevant = any(
            slot["type"] in {"date", "time"} and slot["start"] < end and start < slot["end"]
            for slot in entities
        )
        if relevant or INTENT_CUES.get(clean) == intent:
            note = f"Nimesoma ‘{original}’ kama ‘{replacement}’."
            if note not in notes:
                notes.append(note)
    return "\n".join([format_reply(intent, entities), *notes])


def load_responder(repository, checkpoint):
    import torch
    from transformers import AutoConfig, AutoModel, AutoTokenizer

    repository = repository.resolve()
    if str(repository) not in sys.path:
        sys.path.insert(0, str(repository))
    architecture = spec_from_file_location("_sauti_architecture", repository / "train_joint_intent_slot.py")
    training = module_from_spec(architecture)
    sys.modules[architecture.name] = training
    try:
        architecture.loader.exec_module(training)
    finally:
        del sys.modules[architecture.name]

    metadata_path = checkpoint.parent / "metrics_and_errors.json"
    if not metadata_path.is_file():
        raise FileNotFoundError(
            "Checkpoint-matched metrics_and_errors.json must be beside the checkpoint: "
            f"{metadata_path}"
        )
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    intent_labels = metadata["intent_labels"]
    slot_labels = metadata["slot_labels"]
    missing_intents = sorted(TRACK_C_INTENTS - set(intent_labels))
    unexpected_intents = sorted(set(intent_labels) - TRACK_C_INTENTS)
    if missing_intents or unexpected_intents or len(intent_labels) != len(TRACK_C_INTENTS):
        raise ValueError(
            "Checkpoint intent labels do not match the Track C schema. "
            f"Missing={missing_intents}; unexpected={unexpected_intents}. Retrain on "
            "Team_22_Dataset_Track_C.csv and keep its metrics beside the checkpoint."
        )
    missing_slot_labels = sorted(TRACK_C_SLOT_LABELS - set(slot_labels))
    unexpected_slot_labels = sorted(set(slot_labels) - TRACK_C_SLOT_LABELS)
    if missing_slot_labels or unexpected_slot_labels or len(slot_labels) != len(TRACK_C_SLOT_LABELS):
        raise ValueError(
            "Checkpoint slot labels do not match the Track C schema. "
            f"Missing={missing_slot_labels}; unexpected={unexpected_slot_labels}."
        )
    required_metrics = {
        "intent", "slot_exact_type_character_span_micro", "full_frame_exact_match",
        "json_validity", "unseen_slot_values",
    }
    missing_metrics = sorted(required_metrics - set(metadata.get("test", {})))
    if missing_metrics:
        raise ValueError(
            "Checkpoint metadata has no complete Track C test evaluation. "
            f"Missing={missing_metrics}."
        )
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(metadata["model_name"], use_fast=True)
    class CheckpointModel(training.JointTransformerModel):
        """Reuse the training model's forward pass with weights supplied by our checkpoint."""

        def __init__(self):
            torch.nn.Module.__init__(self)
            config = AutoConfig.from_pretrained(metadata["model_name"])
            self.encoder = AutoModel.from_config(config, add_pooling_layer=False)
            self.dropout = torch.nn.Dropout(0.1)
            self.intent_classifier = torch.nn.Linear(config.hidden_size, len(intent_labels))
            self.slot_classifier = torch.nn.Linear(config.hidden_size, len(slot_labels))
            use_crf = metadata["slot_decoder"] == "constrained_linear_chain_crf"
            self.crf = training.LinearChainCRF(slot_labels) if use_crf else None

    model = CheckpointModel()
    weights = torch.load(checkpoint, map_location="cpu", weights_only=True)
    weights.pop("encoder.pooler.dense.weight", None)
    weights.pop("encoder.pooler.dense.bias", None)
    model.load_state_dict(weights, strict=True)
    model.to(device).eval()

    @torch.inference_mode()
    def respond(text):
        words, spans = training.whitespace_words(text)
        corrected = normalize_words(words)
        encoded = tokenizer(
            corrected, is_split_into_words=True, truncation=True, max_length=128,
            return_tensors="pt",
        )
        word_ids = encoded.word_ids()
        first = [
            word_id is not None and (index == 0 or word_id != word_ids[index - 1])
            for index, word_id in enumerate(word_ids)
        ]
        if not any(first):
            return "Jaribu kuandika ombi lako kwa maneno machache ya Kiswahili."
        mask = torch.tensor([first], dtype=torch.bool, device=device)
        result = model(
            encoded["input_ids"].to(device), encoded["attention_mask"].to(device),
            first_subtoken_mask=mask, decode_slots=True,
        )
        scores, indices = result["intent_logits"][0].softmax(dim=-1).topk(2)
        ranked = [(intent_labels[index], score) for index, score in zip(indices.tolist(), scores.tolist())]
        predictions = result["slot_predictions"]
        ids = (predictions[0] if predictions is not None
               else result["slot_logits"][mask].argmax(dim=-1).tolist())
        tags = [slot_labels[index] for index in ids]
        slots = training.bio_tags_to_char_slots(text, tags)
        visible = [word_id for word_id, include in zip(word_ids, first) if include]
        return interpret_prediction(
            ranked, slots, [(words[i], spans[i]) for i in visible], [corrected[i] for i in visible],
        )

    return respond
