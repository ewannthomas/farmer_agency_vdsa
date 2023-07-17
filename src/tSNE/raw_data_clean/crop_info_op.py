from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
from utils.long_frame import long_frame
import pandas as pd
import numpy as np
import json


def crop_info_op():
    """
    This function is specifically cleans the Crop_info_op files in each year under the Cultivation questionnaire.
    """

    tag = "Crop_info_op"

    raw_path, interim_path, processed_path, external_path = dir_values()

    interim_file = interim_path.joinpath(f"{tag}.csv")

    if not interim_file.exists():
        east_cols = {
            "vdsid": "hh_id",
            "cult_id/hhid/vdsid": "hh_id",
            "var_name": "crop_variety_name",
            "var_type": "crop_variety_type",
            "plot_co": "plot_code",
            "ow_stat": "plot_ownership_status",
            "op_main_prod__rate": "op_main_prod_rate",
            "rent_for": "rent_tenure",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
            "var_name": "crop_variety_name",
            "var_type": "crop_variety_type",
            "plot_co": "plot_code",
            "crop": "crop_name",
        }

        # unncecessary cols to be removed
        remove_cols = [
            "var_type_ot",
            "plot_name",
            "remarks",
            "op_remarks",
            "irri_area",
            "plot_ownership_status",  # this and
            "ow_stat",  # this is the same column.
            "rent_val",
            "rent_tenure",  # this and
            "rent_for",  # this is the same column
        ]

        df = data_wrangler(
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
        )

        index_cols = [
            "hh_id",
            "plot_code",
            "season",
            "crop_name",
            "crop_variety_name",
            "crop_variety_type",
        ]

        df = to_float(
            df=df,
            cols=[
                "crop_variety_type",
                "prct_area",
                "op_main_prod_qty",
                "op_main_prod_rate",
                "op_by_prod_qty",
                "op_by_prod_rate",
                "op_ot_prod_qty",
                "op_ot_prod_rate",
            ],
            error_action="raise",
        )

        # cleaning index columns
        for col in index_cols:
            if col != "hh_id":
                if df[col].dtype == "object":
                    if col == "plot_code":
                        df[col] = df[col].str.strip()
                    else:
                        df[col] = df[col].str.strip().str.lower()

        # removing duplicates by handling each HH separately

        conds = [
            (
                # IBH10C0031
                (df["hh_id"] == "IBH10C0031")
                & (df["plot_code"] == "C")
                & (df["season"] == "rabi")
                & (df["crop_name"] == "wheat")
                & (df["crop_variety_name"] == "up262")
                & (df["crop_variety_type"] == 2)
                & (df["prct_area"] == 100)
                & (
                    df["op_main_prod_unit"].isna()
                )  # target var which identifies the dup and has some information missing
            ),
            (
                # IBH11C0053
                (df["hh_id"] == "IBH11C0053")
                & (df["plot_code"] == "Q")
                & (df["season"] == "kharif")
                & (df["crop_name"] == "paddy")
                & (df["crop_variety_name"] == "sargu 52")
                & (df["crop_variety_type"] == 1)
                & (df["prct_area"] == 50)
                & (
                    df["op_main_prod_unit"].isna()
                )  # target var which identifies the dup and has some information missing
            ),
            (
                # IBH13B0036
                (df["hh_id"] == "IBH13B0036")
                & (df["plot_code"] == "D")
                & (df["season"] == "kharif")
                & (df["crop_name"] == "paddy")
                & (df["crop_variety_name"] == "mtv 7029")
                & (df["crop_variety_type"] == 1)
                & (df["prct_area"] == 100)
                & (
                    df["op_main_prod_unit"].isna()
                )  # target var which identifies the dup and has some information missing
            ),
            (
                # IBH13B0041
                (df["hh_id"] == "IBH13B0041")
                & (df["plot_code"] == "B")
                & (df["season"] == "kharif")
                & (df["crop_name"] == "paddy")
                & (df["crop_variety_name"] == "mtv 7029")
                & (df["crop_variety_type"] == 1)
                & (df["prct_area"] == 100)
                & (
                    df["op_main_prod_unit"].isna()
                )  # target var which identifies the dup and has some information missing
            ),
            (
                # IBH13B0200
                (df["hh_id"] == "IBH13B0200")
                & (df["plot_code"] == "B")
                & (df["season"] == "kharif")
                & (df["crop_name"] == "paddy")
                & (df["crop_variety_name"] == "mtv 7029")
                & (df["crop_variety_type"] == 1)
                & (df["prct_area"] == 100)
                & (
                    df["op_main_prod_unit"].isna()
                )  # target var which identifies the dup and has some information missing
            ),
            (
                # IBH13C0032
                (df["hh_id"] == "IBH13C0032")
                & (df["plot_code"] == "E")
                & (df["season"] == "kharif")
                & (df["crop_name"] == "paddy")
                & (df["crop_variety_name"] == "rajendra mansoory")
                & (df["crop_variety_type"] == 2)
                & (df["prct_area"] == 100)
                & (
                    df["op_main_prod_unit"].isna()
                )  # target var which identifies the dup and has some information missing
            ),
            (
                # IBH13C0037
                (df["hh_id"] == "IBH13C0037")
                & (df["plot_code"] == "F")
                & (df["season"] == "kharif")
                & (df["crop_name"] == "paddy")
                & (df["crop_variety_name"] == "rajendra mansoory")
                & (df["crop_variety_type"] == 2)
                & (df["prct_area"] == 100)
                & (
                    df["op_main_prod_unit"].isna()
                )  # target var which identifies the dup and has some information missing
            ),
            (
                # IOR14B0035
                (df["hh_id"] == "IOR14B0035")
                & (df["plot_code"] == "A")
                & (df["season"] == "kharif")
                & (df["crop_name"] == "paddy")
                & (df["crop_variety_name"] == "pooja")
                & (df["crop_variety_type"] == 1)
                & (df["prct_area"] == 100)
                & (
                    df["op_by_prod_qty"].isna()
                )  # target var which identifies the dup and has some information missing
            ),
        ]

        for x in conds:
            df = df[~x]  # manually verified. Will remove 8 rows

        # creating the crop type column to map crop names to their categories
        # importing the json mapper of crop names
        crop_name_map = "./src/tSNE/raw_data_clean/crop_names_map.json"
        with open(crop_name_map, "r") as in_file:
            crop_map = dict(json.load(in_file))

        crop_type_map = "./src/tSNE/raw_data_clean/crop_type_map.json"
        with open(crop_type_map, "r") as in_file:
            crop_map_type = dict(json.load(in_file))

        df["crop_type"] = df["crop_name"].replace(crop_map)
        df["crop_type"] = df["crop_type"].replace(crop_map_type)

        # mapping crop_variety_type values
        crop_variety_type_map = {
            1: "Local",
            2: "Improved/HYV",
            3: "Hybrid",
            4: "BT",
            5: "Others",
        }
        df["crop_variety_type"] = df["crop_variety_type"].replace(crop_variety_type_map)

        check_duplicates(
            df=df,
            index_cols=[
                "hh_id",
                "plot_code",
                "season",
                "crop_name",
                "crop_variety_name",
                "crop_variety_type",
            ],
            master_check=False,
            write_file=False,
        )

        # exporting long dataframe
        long_frame(
            tag=tag,
            df=df,
            cols=[
                "prct_area",
                "op_main_prod_qty",
                "op_by_prod_qty",
                "op_ot_prod_qty",
                "op_main_prod_rate",
                "op_by_prod_rate",
                "op_ot_prod_rate",
            ],
        )

        df = widen_frame(
            df=df,
            index_cols=["hh_id", "plot_code", "season", "crop_type"],
            wide_cols=[
                "prct_area",
                "op_main_prod_qty",
                "op_by_prod_qty",
                "op_ot_prod_qty",
                "op_main_prod_rate",
                "op_by_prod_rate",
                "op_ot_prod_rate",
            ],
            agg_dict={
                "prct_area": "sum",
                "op_main_prod_qty": "sum",
                "op_by_prod_qty": "sum",
                "op_ot_prod_qty": "sum",
                "op_main_prod_rate": "mean",
                "op_by_prod_rate": "mean",
                "op_ot_prod_rate": "mean",
            },
        )

        # # converting df to float
        # cols = [col for col in df.columns if col not in ["hh_id_panel"]]
        # df = to_float(
        #     df=df,
        #     cols=cols,
        #     error_action="raise",
        # )

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
