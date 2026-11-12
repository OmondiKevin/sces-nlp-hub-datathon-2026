"""Render Sauti in Colab with a checkpoint trained on the final Track C data."""

from importlib.util import find_spec, module_from_spec, spec_from_file_location
import json
import os
from pathlib import Path
import subprocess
import sys


APP = Path(__file__).resolve().parent
TEAM_REPO = APP.parent
EXPECTED_INTENTS = {
    "alarm_set", "calendar_query", "calendar_set", "datetime_query",
    "lists_createoradd", "lists_query", "news_query", "play_music",
    "qa_definition", "weather_query",
}
MODEL_DIR = Path(os.environ.get("TRACK_C_MODEL_DIR", TEAM_REPO / "models" / "track_c_final"))
CHECKPOINT_ID = os.environ.get("TRACK_C_CHECKPOINT_ID", "").strip()


def validate_metadata(metadata):
    intent_labels = metadata.get("intent_labels", [])
    if set(intent_labels) != EXPECTED_INTENTS or len(intent_labels) != len(EXPECTED_INTENTS):
        raise ValueError("Checkpoint metadata does not use the finalized Track C action labels.")
    expected_slots = {"O"} | {
        f"{prefix}-{slot_type}"
        for slot_type in ("location", "date", "time", "item", "term")
        for prefix in ("B", "I")
    }
    slot_labels = metadata.get("slot_labels", [])
    if set(slot_labels) != expected_slots or len(slot_labels) != len(expected_slots):
        raise ValueError("Checkpoint metadata does not use all five Track C slot schemas.")
    test = metadata.get("test", {})
    required_metrics = {
        "intent", "slot_exact_type_character_span_micro",
        "full_frame_exact_match", "json_validity", "unseen_slot_values",
    }
    if not required_metrics.issubset(test):
        raise ValueError("Checkpoint metrics are missing the required Track C evaluation results.")


def open_demo():
    from google.colab import output
    from IPython.display import HTML, JSON, display

    dependencies = ("transformers", "sentencepiece", "tzdata")
    missing = [package for package in dependencies if find_spec(package) is None]
    if missing:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", *missing], check=True)

    if not (TEAM_REPO / "train_joint_intent_slot.py").is_file() or not (TEAM_REPO / "track_c_evaluation.py").is_file():
        raise FileNotFoundError(
            "The current Team 22 repository files are required. Open this notebook "
            "from the checkout containing train_joint_intent_slot.py and track_c_evaluation.py."
        )

    metadata_path = MODEL_DIR / "metrics_and_errors.json"
    checkpoint_candidates = (MODEL_DIR / "best_model.pt", MODEL_DIR / "joint_model.pt")
    checkpoint = next((path for path in checkpoint_candidates if path.is_file()), None)
    runtime_files = Path("/content/sauti-runtime")
    runtime_files.mkdir(exist_ok=True)

    if checkpoint is None and CHECKPOINT_ID:
        if not metadata_path.is_file():
            raise FileNotFoundError(
                f"The matching metrics file is missing: {metadata_path}. Keep it beside the uploaded checkpoint."
            )
        validate_metadata(json.loads(metadata_path.read_text(encoding="utf-8")))
        if find_spec("gdown") is None:
            subprocess.run([sys.executable, "-m", "pip", "install", "-q", "gdown"], check=True)
        import gdown

        checkpoint = runtime_files / "best_model.pt"
        print("Downloading the final Track C checkpoint...")
        if gdown.download(id=CHECKPOINT_ID, output=str(checkpoint), resume=True) is None:
            raise RuntimeError("The checkpoint download failed. Run the cell again to retry.")
        (runtime_files / "metrics_and_errors.json").write_bytes(metadata_path.read_bytes())

    if checkpoint is None:
        raise FileNotFoundError(
            f"No final checkpoint found in {MODEL_DIR}. After the Colab training run, "
            "place best_model.pt and its matching metrics_and_errors.json there, or set "
            "TRACK_C_MODEL_DIR / TRACK_C_CHECKPOINT_ID. The old checkpoint is intentionally not loaded."
        )
    if not metadata_path.is_file() and checkpoint.parent != runtime_files:
        raise FileNotFoundError(f"The checkpoint-matched metrics file is missing beside {checkpoint}.")
    active_metadata = (
        runtime_files / "metrics_and_errors.json"
        if checkpoint.parent == runtime_files
        else metadata_path
    )
    metadata = json.loads(active_metadata.read_text(encoding="utf-8"))
    validate_metadata(metadata)

    spec = spec_from_file_location("sauti_colab_model", APP / "sauti_model.py")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    print("Loading the Sauti model...")
    respond = module.load_responder(TEAM_REPO, checkpoint)

    def reply(message):
        if not isinstance(message, str) or not 1 <= len(message.strip()) <= 280:
            return JSON({"error": "Andika ombi lenye herufi 1 hadi 280."})
        result = respond(message.strip())
        return JSON(result if isinstance(result, dict) else {"reply": result})

    output.register_callback("sauti.reply", reply)

    web = APP / "web"
    html = (web / "index.html").read_text(encoding="utf-8")
    styles = (web / "app.css").read_text(encoding="utf-8")
    script = (web / "app.js").read_text(encoding="utf-8")
    layout = html[html.index("<header"):html.index("<script src=")]
    # The same UI sends requests through Colab's kernel callback in this environment.
    bridge = """
    window.sautiReply = async (message, signal) => {
      const response = google.colab.kernel.invokeFunction("sauti.reply", [message], {});
      const cancelled = new Promise((_, reject) => {
        signal.addEventListener("abort", () => reject(new Error("Request cancelled")), {once: true});
      });
      const output = await Promise.race([response, cancelled]);
      return output.data["application/json"];
    };
    """
    display(HTML(f"<style>{styles}</style>{layout}<script>(() => {{ {bridge}\n{script} }})();</script>"))


if __name__ == "__main__":
    open_demo()
