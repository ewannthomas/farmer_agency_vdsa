from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
import pandas as pd
import numpy as np
import json


def reliab_rank():
    """
    This function is specifically cleans the reliability ranking files in each year under the GES questionnaire.
    """

    tag = "Reliability_ranking"

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

        # cleaning source of assisstance
        df["sou_assistance"] = df["sou_assistance"].str.strip().str.lower()

        source_aasist_map = "./src/tsne/raw_data_clean/reliab_rank_map.json"

        with open(source_aasist_map, "r") as infile:
            all_names = dict(json.load(infile))

        df["sou_assistance"] = df["sou_assistance"].replace(
            all_names
        )  # all name sare checked and no missing values exist here

        # renamimng and converting ranks to floats

        df = to_float(df=df, cols=["rank_rel_dro", "rank_rel_flo"])

        df.rename(
            columns={
                "rank_rel_flo": "reliab_rank_in_flood",
                "rank_rel_dro": "reliab_rank_in_drought",
            },
            inplace=True,
        )

        check_duplicates(
            df=df,
            index_cols=["hh_id", "sou_assistance"],
            master_check=False,
            write_file=False,
        )  # there are 6 dups here. they have been dealt with in the widen_frame function

        df = widen_frame(
            df=df,
            index_cols=["hh_id", "sou_assistance"],
            wide_cols=["reliab_rank_in_flood", "reliab_rank_in_drought"],
            agg_dict={"reliab_rank_in_flood": "min", "reliab_rank_in_drought": "min"},
        )

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
