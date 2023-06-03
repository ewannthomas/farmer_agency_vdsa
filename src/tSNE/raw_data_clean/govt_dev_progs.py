from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
import pandas as pd
import numpy as np
import json


def govt_dev_progs():
    """
    This function is specifically appends the benefits from govt dev programs files in each year under the Transaction questionnaire.
    """
    # This function deviates in terms of usage from others because for years 2011, 2013, 2014 in east and 2014 in sat the amount of benefit
    # from govt is read in as a problematic string which requires two rounds of it being written out as a csv and read again. This fucntion achieves the above

    tag = "Govt_dev_progs_benefits"

    raw_path, interim_path, processed_path, external_path = dir_values()

    interim_file = interim_path.joinpath(f"{tag}.csv")

    if not interim_file.exists():
        east_cols = {
            "vdsid": "hh_id",
            "cult_id/hhid/vdsid": "hh_id",
            "hhid/vdsid": "hh_id",
            "program": "program_name",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
            "who_ben": "id_who_ben",
            "prog_name": "program_name",
        }

        # unncecessary cols to be removed
        remove_cols = ["is_prog_active"]

        df = data_wrangler(
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
        )

        # cleaning the sur_mon_yr column
        df["sur_mon_yr"] = pd.to_datetime(
            df["sur_mon_yr"],
            format="%m/%y",
        )

        # cleaning program name column
        df["program_name"] = df["program_name"].str.strip().str.lower()

        govt_prog_mapper_path = "./src/tSNE/raw_data_clean/govt_ben_progs_map.json"
        with open(govt_prog_mapper_path, "r") as in_file:
            govt_progs_map = dict(json.load(in_file))

        df["program_name"] = df["program_name"].replace(govt_progs_map)
        # print(df["program_name"].unique())
        # print(df["program_name"].nunique())

        # cleaning amount of benefits columns
        df = to_float(df=df, cols=["amt_ben"], error_action="raise")

        # aggreagting amt_ben over index cols
        df = df.groupby(["hh_id", "program_name"])["amt_ben"].agg(sum).reset_index()

        df = widen_frame(
            df=df,
            index_cols=["hh_id", "program_name"],
            wide_cols=["amt_ben"],
            agg_dict={"amt_ben": "sum"},
        )

        print(df)

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
