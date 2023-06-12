from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
from utils.long_frame import long_frame
import pandas as pd
import numpy as np
import json


def gender_crop_cult():
    """
    This function is specifically cleans the Gender crop decision making files in each year under the GES questionnaire.
    """

    tag = "Gend_crop_cult"

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

        # Cleaning activity column
        df["activity"] = df["activity"].str.strip().str.lower().str.replace(" ", "_")

        conds = [
            (df["activity"] == "transport_of_fym_&_appl."),
            (df["activity"] == "chemical_fertilizer_appl."),
            (df["activity"] == "land_prepration"),
            (df["activity"] == "seed_selection_ans_storage"),
        ]

        opts = [
            "transport_of_fym_and_application",
            "chemical_fertilizer_application",
            "land_preparation",
            "seed_selection_and_storage",
        ]

        df["activity"] = np.select(conds, opts, default=df["activity"])

        # removing duplicate entries across all columns
        df.drop_duplicates(inplace=True)

        # removing cases where * is present for men and men_women for the same activity in specific hh from odisha
        # Specify the conditions for selecting rows to remove
        conditions = [
            (df["hh_id"] == "IOR14D0054")
            & (df["activity"] == "seed_selection_and_storage")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0054")
            & (df["activity"] == "watching")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0055")
            & (df["activity"] == "chemical_fertilizer_application")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0055")
            & (df["activity"] == "hand_weeding")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0055")
            & (df["activity"] == "irrigation")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0055")
            & (df["activity"] == "land_preparation")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0055")
            & (df["activity"] == "plant_protection_measures")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0055")
            & (df["activity"] == "seed_selection_and_storage")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0055")
            & (df["activity"] == "selection_of_crop")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0055")
            & (df["activity"] == "selection_of_variety")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0055")
            & (df["activity"] == "sowing_seed")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0055")
            & (df["activity"] == "transplanting")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0055")
            & (df["activity"] == "transport_of_fym_and_application")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0056")
            & (df["activity"] == "chemical_fertilizer_application")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0056")
            & (df["activity"] == "hand_weeding")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0056")
            & (df["activity"] == "harvesting")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0056")
            & (df["activity"] == "interculture")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0056")
            & (df["activity"] == "marketing")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0056")
            & (df["activity"] == "plant_protection_measures")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0056")
            & (df["activity"] == "selection_of_crop")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0056")
            & (df["activity"] == "selection_of_variety")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0056")
            & (df["activity"] == "sowing_seed")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0056")
            & (df["activity"] == "threshing")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0056")
            & (df["activity"] == "transport_of_fym_and_application")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0056")
            & (df["activity"] == "watching")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0057")
            & (df["activity"] == "seed_selection_and_storage")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0058")
            & (df["activity"] == "seed_selection_and_storage")
            & (df["men"] == "*"),
            (df["hh_id"] == "IOR14D0058")
            & (df["activity"] == "threshing")
            & (df["men"] == "*"),
        ]

        # Create a list of values to replace for each condition
        replace_values = ["###"] * len(conditions)

        # Use numpy select to update the "men" column based on the conditions
        df["men"] = np.select(conditions, replace_values, df["men"])

        df = df[~(df["men"] == "###")]

        check_duplicates(
            df=df,
            index_cols=["hh_id", "activity"],
            master_check=False,
            write_file=False,
        )

        # replacing * with 1
        for col in ["men", "women", "men_women"]:
            df[col] = df[col].str.strip().str.replace("*", "1")

        # exporting long dataframe
        long_frame(tag=tag, df=df)

        # widening the data frame
        df = widen_frame(df=df, index_cols=["hh_id", "activity"])

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
