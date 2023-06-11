import pandas as pd
from pathlib import Path


def hh_id_create(df: pd.DataFrame):
    """
    This method creates the household ID for which is invariable across years. This new ID will enable 'xtset' functionalities in STATA for panel data regression.

    Parameters:
        df: A pandas dataframe which contains the column hh_id.
    """

    df = pd.DataFrame(df)

    df["hh_id_panel"] = df["hh_id"].str.slice(0, 3) + df["hh_id"].str.slice(5, 10)

    print(df["hh_id_panel"].nunique())

    return df
