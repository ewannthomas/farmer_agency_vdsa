from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
import pandas as pd
import numpy as np


def livestock():
    """
    This function is specifically cleans the Livestock inventory file in each year under the GES questionnaire.
    """

    tag = "Livestock_inv"

    raw_path, interim_path, processed_path, external_path = dir_values()

    interim_file = interim_path.joinpath(f"{tag}.csv")

    if not interim_file.exists():
        east_cols = {"vdsid": "hh_id", "preent_val": "present_val"}

        sat_cols = {
            "vds_id": "hh_id",
        }

        # unncecessary cols to be removed
        remove_cols = ["remarks_c", "mem_owns", "remarks"]

        df = data_wrangler(
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
        )

        # removing duplicates across all columns
        df.drop_duplicates(
            inplace=True
        )  # manually checked and 1 entry will be removed.

        df.rename(
            columns={
                "present_val": "livestock_present_value",
                "resource_no": "livestock_count",
                "no_of_rea": "on_farm_reared_count",
                "no_pur": "purchased_count",
                "no_rec_gift": "received_gift_count",
                "no_sha_rea": "shared_rearing_count",
            },
            inplace=True,
        )

        # recoding the label in livestock_type column
        df["livestock_type"] = df["livestock_type"].str.strip().str.lower()

        conds = [
            df["livestock_type"].isin(
                [
                    "bullocks(local)",
                    "bullocks(impr.)",
                    "bullock (improved)",
                    "bullock (local)",
                ]
            ),
            df["livestock_type"].isin(
                [
                    "he buffaloes(local)",
                    "she buffaloes(local)",
                    "she buffaloes(impr.)",
                    "young cattle (buffaloe)",
                    "she buffalo (local)",
                    "he buffalo (local)",
                    "young stock buffalo (<3 years)",
                    "young stock buffallo (<3years)",
                    "she buffalo (improved)",
                    "he buffalo (improved)",
                ]
            ),
            df["livestock_type"].isin(["poultry", "duck", "pigeon"]),
            df["livestock_type"].isin(
                [
                    "cows(local)",
                    "cow (local)",
                    "cows(impr./cross bred)",
                    "cow (cross breed)",
                    "cow (crossbreed)",
                    "cow (improved)",
                    "cow (improved/cross breed)",
                    "cow (impr./crossbreed)",
                    "young stock(<3 years)",
                    "young stock",
                    "young stock cattle (<3years)",
                    "young stock cattle (<3 years)",
                    "young stock cattel (<3 years)",
                ]
            ),
        ]

        opts = ["bullocks", "buffalo", "poultry", "cow"]

        df["livestock_type"] = np.select(conds, opts, default=df["livestock_type"])

        # converting presetn value column to float
        df = to_float(
            df=df,
            cols=[
                "livestock_present_value",
                "on_farm_reared_count",
                "purchased_count",
                "received_gift_count",
                "shared_rearing_count",
            ],
        )

        # grouping by and summing the numeric values at hh_id and livestock type
        df = df.groupby(["hh_id", "livestock_type"]).agg(sum).reset_index()

        check_duplicates(
            df=df,
            index_cols=["hh_id", "livestock_type"],
            master_check=False,
            write_file=True,
        )

        df = widen_frame(df=df, index_cols=["hh_id", "livestock_type"])

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
