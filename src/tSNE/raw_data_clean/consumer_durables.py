from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
from utils.long_frame import long_frame
from utils.to_float import to_float
import pandas as pd
import numpy as np
import json


def cons_durab():
    """
    This function is specifically cleans the Consumer Durables files in each year under the GES questionnaire.
    """

    tag = "Consumer_durables"

    raw_path, interim_path, processed_path, external_path = dir_values()

    interim_file = interim_path.joinpath(f"{tag}.csv")

    if not interim_file.exists():
        east_cols = {
            "vdsid": "hh_id",
            "item_durable": "item_name",
            "no_durable": "item_qty",
            "pre_val": "present_value_durable",
            "id_who_owns": "who_owns_durable",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
            "item_con_du": "item_name",
            "no_con_du": "item_qty",
            "val_con_du": "present_value_durable",
            "who_owns_con_du": "who_owns_durable",
            "item_durable": "item_name",
            "no_durable": "item_qty",
            "pre_val": "present_value_durable",
            "id_who_owns": "who_owns_durable",
        }

        # unncecessary cols to be removed
        remove_cols = ["remarks_e_con_du", "who_owns_durable", "remarks"]

        df = data_wrangler(
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
        )

        # renaming the column
        df.rename(
            columns={"item_qty": "qty", "present_value_durable": "present_value"},
            inplace=True,
        )

        print(df.shape[0])

        # cleaning item_name column
        df["item_name"] = df["item_name"].str.strip().str.lower()

        cons_durab_map = "./src/tsne/raw_data_clean/consumer_durables_name_map.json"

        with open(cons_durab_map, "r") as infile:
            all_names = dict(json.load(infile))

        df["item_name"] = df["item_name"].replace(
            all_names
        )  # all names are checked and no missing values exist here

        # print(df["item_name"].unique())

        # exporting long dataframe
        long_frame(tag=tag, df=df)

        df = widen_frame(
            df=df,
            index_cols=["hh_id", "item_name"],
            wide_cols=["qty", "present_value"],
            agg_dict={"qty": "sum", "present_value": "sum"},
        )

        check_duplicates(
            df=df,
            index_cols=["hh_id", "item_name"],
            master_check=False,
            write_file=False,
        )

        # converting all except hh id to float
        cols = [col for col in df.columns if col not in ["hh_id_panel"]]
        df = to_float(df=df, cols=cols, error_action="raise")

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
