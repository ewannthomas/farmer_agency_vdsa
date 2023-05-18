from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
import pandas as pd
import numpy as np
import json


def gender_decs_making():
    """
    This function is specifically cleans the Gender decision making files in each year under the GES questionnaire. This fucntion deals with the 'Resource ownership and decision-making' part of the GES questionnaire.
    """

    tag = "Gend_decision_making"

    raw_path, interim_path, processed_path, external_path = dir_values()

    interim_file = interim_path.joinpath(f"{tag}.csv")

    if not interim_file.exists():
        east_cols = {
            "vdsid": "hh_id",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
        }

        # unncecessary cols to be removed
        remove_cols = []

        df = data_wrangler(
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
        )

        male_cols = ["ownership_m", "deci_making_m", "who_infl_util_m"]

        female_cols = ["ownership_f", "deci_making_f", "who_infl_util_f"]

        actual_cols = ["ownership", "deci_making", "who_infl_util"]

        col_dict = {
            "M": "Male",
            "F": "Female",
            "B": "Both",
            "N": np.nan,
            "NA": np.nan,
        }

        for male, female, actual in zip(male_cols, female_cols, actual_cols):
            df[male] = df[male].str.strip()
            df[female] = df[female].str.strip()
            df[actual] = df[actual].str.strip()

            # replacing missing values in male columns with values in female columns
            df[male] = np.where(df[male].isna(), df[female], df[male])

            # replacing mapped male cols to the actuals
            df[actual] = np.where(df[actual].isna(), df[male], df[actual])
            df[actual] = df[actual].replace(col_dict)

            # print(df[actual].unique())

        df.drop(female_cols, axis=1, inplace=True)
        df.drop(male_cols, axis=1, inplace=True)

        # cleaning resource category  and resources columns
        df["reso_category"] = df["reso_category"].str.strip().str.lower()
        df["resource"] = df["resource"].str.strip().str.lower()

        resource_dict = {
            "pesticide": "pesticides",
            "fertilizer": "fertilizers",
            "seed": "seeds",
            "others(specify)": "others",
            "others (specify)": "others",
            "women stepping out of house": "women stepping out of the house",
            "women stepping out of th": "women stepping out of the house",
            "exp.on health care": "expenditure on health care",
            "expenditure of helth car": "expenditure on health care",
            "fodder production & use": "fodder production and use",
        }

        df["resource"] = df["resource"].replace(resource_dict)

        df.drop_duplicates(subset=["hh_id", "reso_category", "resource"], inplace=True)

        check_duplicates(
            df=df,
            index_cols=["hh_id", "reso_category", "resource"],
            master_check=True,
            write_file=True,
        )

        df = widen_frame(df=df, index_cols=["hh_id", "reso_category", "resource"])

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
