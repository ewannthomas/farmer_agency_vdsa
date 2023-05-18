from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
import pandas as pd
import numpy as np
import json


def stock_inv():
    """
    This function is specifically cleans the Stock inventory files in each year under the GES questionnaire.
    """

    tag = "Stock_inv"

    raw_path, interim_path, processed_path, external_path = dir_values()

    interim_file = interim_path.joinpath(f"{tag}.csv")

    if not interim_file.exists():
        east_cols = {
            "vdsid": "hh_id",
            "unit_price": "unit_price_stock",
            "tot_value": "total_value_stock",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
            "unit_pr_stock": "unit_price_stock",
            "tot_val_stock": "total_value_stock",
        }

        # unncecessary cols to be removed
        remove_cols = ["remarks_f", "remarks"]

        df = data_wrangler(
            tag=tag, rename_east=east_cols, rename_sat=sat_cols, remove_cols=remove_cols
        )

        # Removing duplicates
        df = df.drop_duplicates()  # manually verified. Will remove 5 observations

        # cleaning item_category names
        df["stock_category"] = df["stock_category"].str.strip().str.lower()
        df["stock_category"] = df["stock_category"].replace(
            {
                "fert.& pesticides": "inputs",
                "fertilizers": "inputs",
                "cooking": "cooking fuel",
                "cookings": "cooking fuel",
                "input": "inputs",
                "others items": "other items",
                "others": "other items",
            }
        )

        # cleaning numeric columns
        df = to_float(
            df=df, cols=["qty_stock", "unit_price_stock", "total_value_stock"]
        )

        # check_duplicates(
        #     df=df,
        #     index_cols=["hh_id", "stock_category"],
        #     master_check=False,
        #     write_file=True,
        # )

        df = widen_frame(
            df=df,
            index_cols=["hh_id", "stock_category"],
            wide_cols=["qty_stock", "unit_price_stock", "total_value_stock"],
            agg_dict={
                "qty_stock": "sum",
                "unit_price_stock": "sum",
                "total_value_stock": "sum",
            },
        )

        # print(df.columns)

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
