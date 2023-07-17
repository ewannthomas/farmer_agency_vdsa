from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
from utils.long_frame import long_frame
import pandas as pd
import numpy as np
import json


def fin_transacts():
    """
    This function is specifically appends the financial transactions files in each year under the Transaction questionnaire.
    """

    tag = "Fin_Trans"

    raw_path, interim_path, processed_path, external_path = dir_values()

    interim_file = interim_path.joinpath(f"{tag}.csv")

    if not interim_file.exists():
        east_cols = {
            "vdsid": "hh_id",
            "cult_id/hhid/vdsid": "hh_id",
            "hhid/vdsid": "hh_id",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
        }

        # unncecessary cols to be removed
        remove_cols = [
            "from_whom",
            "from_whom_ot",
            # "who_sp",
            "purpose",
            "cast_co",
            "cast_co_ot",
            "id_who_did",
            "remarks",  # either all cols empty or near empty
        ]

        df = data_wrangler(
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
        )

        # making the date column correct
        # df["sur_mon_yr"] = df["sur_mon_yr"].str.replace("27/11/2014", "11/2014")
        df["sur_mon_yr"] = pd.to_datetime(
            df["sur_mon_yr"],
            format="%m/%y",
            errors="coerce",
        )

        # now inorder to correct the date values in 2014, we are slicing it out of the data and cleaning it
        df_time_missing = df[df["sur_mon_yr"].isna()]
        df_time_missing["sur_mon_yr"] = df_time_missing["sur_mon_yr"].astype(str)

        # correcting date for hh_id=IOR14C0033
        df_time_missing["dt_int"] = np.where(
            (df_time_missing["hh_id"] == "IOR14C0033")
            & (df_time_missing["dt_int"] == "02/08"),
            "08/14",
            df_time_missing["dt_int"],
        )
        # correcting date for hh_id=IOR14C0039
        df_time_missing["dt_int"] = np.where(
            (df_time_missing["hh_id"] == "IOR14C0039")
            & (df_time_missing["dt_int"] == "10 14"),
            "10/14",
            df_time_missing["dt_int"],
        )

        df_time_missing["sur_mon_yr"] = np.where(
            (df_time_missing["sur_mon_yr"] == "NaT")
            & (df_time_missing["sur_yr"] == 2014),
            df_time_missing["dt_int"],
            df_time_missing["sur_mon_yr"],
        )

        df_time_missing["sur_mon_yr"] = pd.to_datetime(
            df_time_missing["sur_mon_yr"],
            format="%m/%y",
            errors="coerce",
        )

        # appending the corrected slice back
        df = df[~(df["sur_mon_yr"].isna())]
        df = pd.concat([df, df_time_missing], axis=0).reset_index(drop=True)

        # cleaning category and source
        df["fin_category"] = df["fin_category"].str.strip().str.lower()

        df = df[
            ~(df["fin_category"] == "fin_category")
        ]  # removing unnecessary header which crept in as an obs manually verified. 1 obs will be removed

        fin_cat_map = {
            "recipts & payment": "receipts and payments",
            "receipts & payments": "receipts and payments",
            "savings & deposits": "savings and deposits",
            "saving & deposite": "savings and deposits",
            "gifts": "gift and remittances",
            "remittances": "gift and remittances",
        }
        df["fin_category"] = df["fin_category"].replace(fin_cat_map)

        df["fin_source"] = df["fin_source"].str.strip().str.lower()

        # print(df["fin_category"].unique())
        # print(df["fin_source"].nunique())

        # cleaning the who_sp column
        gender_map = {"b": "both", "m": "male", "f": "female"}
        df["who_sp"] = df["who_sp"].str.strip().str.lower()
        df["who_sp"] = df["who_sp"].replace(gender_map)

        # renamimg the columns
        df.rename(
            columns={
                "amt_giv": "amount_given",
                "amt_rec": "amount_received",
                "who_sp": "amount_spend_by",
            },
            inplace=True,
        )

        # removing duplicates
        df.drop_duplicates(inplace=True)  # manually verified. 99 obs will be removed

        # adding month column
        df["month"] = pd.to_datetime(df["sur_mon_yr"]).dt.month_name()
        # droppimg sur_mon_yr values as we have year and month capturing the necesary information
        df.drop("sur_mon_yr", axis=1, inplace=True)

        check_duplicates(
            df=df,
            index_cols=["hh_id", "month", "fin_category"],
            master_check=False,
            write_file=True,
        )

        # exporting long dataframe
        long_frame(
            tag=tag,
            df=df,
            cols=["amount_given", "amount_received"],
        )

        df = widen_frame(
            df=df,
            index_cols=["hh_id", "month", "fin_category", "amount_spend_by"],
            wide_cols=["amount_given", "amount_received"],
            agg_dict={"amount_given": "sum", "amount_received": "sum"},
            index_miss=True,
        )

        df.to_csv(interim_file, index=False)
    else:
        print(f"{tag} interim file exists")
