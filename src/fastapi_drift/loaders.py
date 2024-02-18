import json
import sqlite3
from pathlib import Path

import pandas as pd
from fastapi_drift.schemas import Response

BASE_DIR = Path(__file__).resolve(strict=True).parents[2]
RESOURCES_DIR = BASE_DIR / "resources"


def load_train_data():
    df = pd.read_csv(RESOURCES_DIR / "iris_train.csv")
    return df


class PredDataLoader:
    def run_loader(self):
        df = (
            self.load_sql_db_to_df()
            .pipe(self._explode_json_cols)
            .pipe(self._create_target_col)
            .pipe(self._map_target_col)
            .pipe(self._rm_proba_cols)
        )
        return df.copy()

    @staticmethod
    def load_sql_db_to_df() -> pd.DataFrame:
        conn = sqlite3.connect(RESOURCES_DIR / "predictions_store.db")
        df = pd.read_sql_query("SELECT * FROM iris", conn)
        conn.close()
        return df

    @staticmethod
    def _explode_json_cols(df: pd.DataFrame) -> pd.DataFrame:
        df["request"] = df["request"].apply(json.loads)
        df["response"] = df["response"].apply(json.loads)
        df1 = pd.json_normalize(df["request"])
        df2 = pd.json_normalize(df["response"])
        return pd.concat([df1, df2], axis=1)

    @staticmethod
    def _create_target_col(df: pd.DataFrame) -> pd.DataFrame:
        df["target"] = (
            df[list(Response.__fields__.keys())]
            .idxmax(axis=1)
            .str.replace("_probability", "")
        )
        return df

    @staticmethod
    def _map_target_col(df: pd.DataFrame) -> pd.DataFrame:
        df["target"] = df["target"].map(Response.target_mapper)
        return df

    @staticmethod
    def _rm_proba_cols(df: pd.DataFrame) -> pd.DataFrame:
        df = df.loc[:, ~df.columns.str.endswith("_probability")]
        return df
