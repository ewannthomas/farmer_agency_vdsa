from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.hh_id_create import hh_id_create
from utils.long_frame import long_frame
import pandas as pd
import numpy as np


def gen_info_cleaner():
    """
    This function is specifically cleans the Gen_info.xlsx file in each year under the GES questionnaire.
    """

    raw_path, interim_path, processed_path, external_path = dir_values()

    tag = "Gen_info"

    interim_file = interim_path.joinpath(f"{tag}.csv")

    if not interim_file.exists():
        east_cols = {"vdsid": "hh_id", "the_man_blo": "block"}

        sat_cols = {"vds_id": "hh_id", "teh_man_blo": "block"}

        # unncecessary cols to be removed
        remove_cols = [
            "dt_int",
            "dt_check",
            "sou_hh_no",
            "head_name",
            "son_wife_of",
            "lon_deg",
            "lon_min",
            "lon_sec",
            "lat_deg",
            "lat_min",
            "lat_sec",
            "altitude",
            "inv_name",
            "name_sup",
            "pre_hh_no",
            "old_hh_no",
            "vdsid_hhid",
            "cs_hh_no",
        ]

        df = data_wrangler(
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
        )

        # converting numeric columns to floats
        df = to_float(
            df=df,
            cols=[
                "family_size",
                "oper_holding",
                "when_head",
                "when_head_dry",
                "dry_rate",
                "when_head_irri",
                "irri_rate",
                "val_resi_plot",
                "no_animals",
                "val_animals",
                "val_farm_impl",
                "val_ot_assets",
                "cash_rec",
                "loan_rec",
                "distance",
                "year_immi",
            ],
        )

        # blanket processes for string cols
        col_list = df.columns

        selected_cols = [
            "village",
            "block",
            "district",
            "state",
            "country",
            "market_place",
            "caste",
            "sub_caste",
            "religion",
            "immi_to_vil",
            "how_head_ot",
            "reas_immi",
        ]

        special_cols = ["how_head_ot", "reas_immi"]

        for col in col_list:
            if df[col].dtype == "object":
                df[col] = df[col].str.strip()

            if col in selected_cols:
                df[col] = df[col].str.title().str.replace(" ", "_")

        for col in special_cols:
            df[col] = df[col].str.title().str.replace("_", " ")

        # cleaning religion column
        conds = [
            df["religion"].isin(["Hindu", "Hindi", "Hindu24", "Obc", "Sarna", "Saran"]),
            df["religion"].isin(
                [
                    "Christian",
                    "Christion",
                    "Christan",
                    "Christain",
                    "Christians",
                    "1988",
                ]
            ),
            df["religion"].isin(["Boudh", "Boudha"]),
            df["religion"].isin(["Muslim"]),
            df["religion"].isin(["Jain"]),
        ]

        options = ["Hinduism", "Christianity", "Buddhism", "Islam", "Jainism"]

        df["religion"] = np.select(conds, options, default=df["religion"])

        # cleaning caste groups column
        df["caste_group"] = df["caste_group"].str.upper()

        conds = [
            df["caste_group"].isin(["EBC", "SBC"]),
            df["caste_group"].isin(["BC"]),
        ]

        options = ["SBC/SEBC/EBC", "OBC"]

        df["caste_group"] = np.select(conds, options, default=df["caste_group"])

        # exporting long dataframe
        long_frame(tag=tag, df=df)

        df = hh_id_create(df=df)

        print(df)

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
