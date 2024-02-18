from pathlib import Path

import joblib
import pandas as pd
from sklearn import datasets, svm

BASE_DIR = Path(__file__).resolve(strict=True).parents[2]
RESOURCES_DIR = BASE_DIR / "resources"


def train_iris_model() -> None:
    X, y = datasets.load_iris(return_X_y=True)
    clf = svm.SVC(probability=True)
    clf.fit(X, y)
    joblib.dump(clf, RESOURCES_DIR / "iris_model.joblib")


def store_iris_to_csv() -> None:
    iris = datasets.load_iris()
    iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)
    iris_df["target"] = iris.target
    iris_df.columns = iris_df.columns.str.replace(" ", "_").str.replace("_(cm)", "")
    iris_df.to_csv(RESOURCES_DIR / "iris_train.csv", index=False)


if __name__ == "__main__":
    train_iris_model()
    store_iris_to_csv()
