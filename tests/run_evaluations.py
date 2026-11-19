
import json
from datetime import datetime, timezone
from pathlib import Path

from src.ollama_client import analyze_alert, MODEL


PROJECT_ROOT = Path(__file__).resolve().parents[1]

ALERT_FILE = (
    PROJECT_ROOT
    / "data/sample-alerts/TC-001-terminal-shell.json"
)

REPORT_DIRECTORY = PROJECT_ROOT / "reports/runs"


def run_test():
    with ALERT_FILE.open("r", encoding="utf-8") as file:
        alert = json.load(file)

    test_id = alert["test_id"]

    print(f"Running security test: {test_id}")
    print(f"Model: {MODEL}")

    # Submit the alert to the existing Ollama client
    analysis = analyze_alert(alert)

    # Store the raw analysis text returned by our client
    result = {
        "test_id": test_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": MODEL,
        "input_alert": alert,
        "model_response": analysis,
        "evaluation_status": "Pending human review"
    }

    REPORT_DIRECTORY.mkdir(parents=True, exist_ok=True)

    output_file = REPORT_DIRECTORY / f"{test_id}-response.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(result, file, indent=2, ensure_ascii=False)

    print("\nMODEL ANALYSIS\n")
    print(analysis)

    print(f"\nResult saved to: {output_file}")


if __name__ == "__main__":
    run_test()
