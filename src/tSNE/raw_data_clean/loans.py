from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
from utils.long_frame import long_frame
import pandas as pd
import numpy as np
import json


def loans():
    """
    This function is specifically appends the loans transactions files in each year under the Transaction questionnaire.
    """

    tag = "Loans"

    raw_path, interim_path, processed_path, external_path = dir_values()

    interim_file = interim_path.joinpath(f"{tag}.csv")

    if not interim_file.exists():
        east_cols = {
            "vdsid": "hh_id",
            "cult_id/hhid/vdsid": "hh_id",
            "hhid/vdsid": "hh_id",
            "who_did_id": "id_who_did",
        }

        sat_cols = {"vds_id": "hh_id", "vdsid": "hh_id", "who_did_id": "id_who_did"}

        # unncecessary cols to be removed
        remove_cols = [
            "id_who_did",
        ]  # "who_sp_ben"

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

        # cleaning loan_source column
        for col in ["loan_category", "loan_source"]:
            df[col] = df[col].str.strip().str.lower()

        # recoding loan source values
        loan_source_map_path = "./src/tSNE/raw_data_clean/loan_source_map.json"
        with open(loan_source_map_path, "r") as in_file:
            loan_source_mapper = dict(json.load(in_file))

        df["loan_source"] = df["loan_source"].replace(loan_source_mapper)
        df["loan_source"] = df["loan_source"].str.strip().str.lower()
        print(df["loan_source"].unique())

        # converting numerics to float
        df = to_float(
            df=df, cols=["loan_repaid", "loan_rec", "loan_int"], error_action="raise"
        )

        # removing duplicates
        df.drop_duplicates(
            inplace=True
        )  # manually verified. 21 observations will be removed

        check_duplicates(
            df=df,
            index_cols=["hh_id", "sur_mon_yr", "loan_source"],
            master_check=True,
            write_file=True,
        )

        df.rename(
            columns={"loan_rec": "loan_received", "loan_int": "interest_on_loan"},
            inplace=True,
        )

        # exporting long dataframe
        long_frame(
            tag=tag, df=df, cols=["loan_repaid", "loan_received", "interest_on_loan"]
        )

        df = widen_frame(
            df=df,
            index_cols=["hh_id", "sur_mon_yr", "loan_source"],
            wide_cols=["loan_repaid", "loan_received", "interest_on_loan"],
            agg_dict={
                "loan_repaid": "sum",
                "loan_received": "sum",
                "interest_on_loan": "mean",
            },
        )

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
