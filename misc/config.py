from datetime import datetime
from pathlib import Path


class Paths:
    logs = Path("logs")

    @staticmethod
    def get_log_path() -> Path:
        return Path(Paths.logs, f"{datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}.log")

    resources = Path("resources")
    favicon = Path(resources, "favicon.png")
    model = Path(resources, "logreg.pickle")
    tfidf_vectorizer = Path(resources, "tfidf_vectorizer.pickle")
