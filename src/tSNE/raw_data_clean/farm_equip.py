from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.widen_frame import widen_frame
from utils.long_frame import long_frame
import pandas as pd
import numpy as np
import json


def farm_equip():
    """
    This function is specifically cleans the Farm_Equipment files in each year under the GES questionnaire.
    """

    tag = "Farm_Equipment"

    raw_path, interim_path, processed_path, external_path = dir_values()

    interim_file = interim_path.joinpath(f"{tag}.csv")

    if not interim_file.exists():
        east_cols = {"vdsid": "hh_id"}

        sat_cols = {"vds_id": "hh_id", "item_no": "item_qty", "item_val": "present_val"}

        # unncecessary cols to be removed
        remove_cols = ["remarks", "remarks_d"]

        df = data_wrangler(
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
        )

        df = to_float(df=df, cols=["present_val"])

        # cleaning item name column
        df["item_name"] = df["item_name"].str.strip().str.lower()

        farm_equip_map = "./src/tsne/raw_data_clean/farm_equip_map.json"

        with open(farm_equip_map, "r") as infile:
            all_names = dict(json.load(infile))

        df["item_name"] = df["item_name"].replace(
            all_names
        )  # all name sare checked and no missing values exist here

        df["item_name"] = df["item_name"].str.replace(" ", "_").str.lower()
        df["item_name"] = df["item_name"].str.replace("(", "").str.replace(")", "")

        # cleaning the present value column
        df.rename(
            columns={
                "present_val": "farm_equipment_present_value",
                "item_name": "farm_equip_name",
                "item_qty": "farm_equip_qty",
            },
            inplace=True,
        )

        # exporting long dataframe
        long_frame(
            tag=tag,
            df=df,
            cols=["farm_equip_qty", "horse_power", "farm_equipment_present_value"],
        )

        df = widen_frame(
            df=df,
            index_cols=["hh_id", "farm_equip_name"],
            wide_cols=["farm_equip_qty", "horse_power", "farm_equipment_present_value"],
            agg_dict={
                "farm_equip_qty": "sum",
                "horse_power": "max",
                "farm_equipment_present_value": "sum",
            },
            index_miss=True,
        )

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
