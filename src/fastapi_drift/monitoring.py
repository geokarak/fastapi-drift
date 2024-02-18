from pathlib import Path

from evidently.metric_preset import DataDriftPreset
from evidently.report import Report
from fastapi_drift.loaders import PredDataLoader, load_train_data

BASE_DIR = Path(__file__).resolve(strict=True).parents[2]
STATIC_DIR = BASE_DIR / "static"


def get_data_drift_report() -> str:
    data_drift_report = Report(
        metrics=[
            DataDriftPreset(),
        ]
    )

    reference_data = load_train_data()
    current_data = PredDataLoader().run_loader()

    data_drift_report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=None,
    )

    report_location = STATIC_DIR / "drift.html"
    data_drift_report.save_html(str(report_location))

    return report_location


if __name__ == "__main__":
    get_data_drift_report()
