from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
from utils.long_frame import long_frame
import pandas as pd
import numpy as np
import json


def sales_purchase():
    """
    This function is specifically appends the sales and purchase files in each year under the Transaction questionnaire.
    """

    tag = "Sale_pur"

    raw_path, interim_path, processed_path, external_path = dir_values()

    interim_file = interim_path.joinpath(f"{tag}.csv")

    if not interim_file.exists():
        east_cols = {
            "vdsid": "hh_id",
            "cult_id/hhid/vdsid": "hh_id",
            "hhid/vdsid": "hh_id",
            # "pur_pl_dist": "pur_dist",
            # "sold_pl_dist": "sold_dist",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
            "item_pur_sold": "item_category",
        }

        # unncecessary cols to be removed
        remove_cols = ["remarks"]

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

        # cleaning item_category
        df["item_category"] = df["item_category"].str.strip().str.lower()

        # laoding mapper for item_category
        item_cat_map_path = "./src/tSNE/raw_data_clean/sales_pur_item_cats.json"
        with open(item_cat_map_path, "r") as in_file:
            item_cat_mapper = dict(json.load(in_file))

        df["item_category"] = df["item_category"].replace(item_cat_mapper)

        df["item_category"] = df["item_category"].str.strip().str.lower()

        # print(df["item_category"].unique())

        # print(df["item_category"].nunique())

        # extrapolating pur_pl_dist on to pur_dist when later is non missing
        df["pur_dist"] = np.where(
            (df["pur_dist"].isna()) & (df["pur_pl_dist"].astype(str).str.isdigit()),
            df["pur_pl_dist"],
            df["pur_dist"],
        )  # manually verified

        # mapping pur_from amd sold_to columns
        person_map = {
            1: "Friend",
            2: "Relative",
            3: "Money lender",
            4: "Employer",
            5: "Tenant",
            6: "Shop",
            7: "SHG",
            8: "Government",
            9: "Others",
        }

        for col in ["pur_from", "sold_to"]:
            df[col] = df[col].map(
                person_map
            )  # map function use has been checked and verified

        # converting values to float
        df["sold_qty"] = np.where(df["sold_qty"].str.isdigit(), df["sold_qty"], "")
        df = to_float(
            df=df,
            cols=[
                "pur_cost",
                "pur_dist",
                "sold_cost",
                "sold_dist",
                "pur_qty",
                "sold_qty",
            ],
            error_action="raise",
        )

        # removing the duplicates
        df.drop_duplicates(inplace=True)

        check_duplicates(
            df=df, index_cols=["hh_id"], master_check=True, write_file=True
        )

        # splitting data to sold and purchase datasets and then appending

        pur_cols = [
            "hh_id",
            "sur_yr",
            "sur_mon_yr",
            "item_category",
            "pur_qty",
            "pur_cost",
            "pur_dist",
            "pur_from",
        ]

        df_pur = (
            df[pur_cols]
            .rename(
                columns={
                    "pur_cost": "market_cost",
                    "pur_dist": "dist_to_market",
                    "pur_from": "from_whom",
                    "pur_qty": "quantity",
                }
            )
            .dropna(
                axis=0,
                subset=["market_cost", "dist_to_market", "from_whom", "quantity"],
                how="all",
            )
        )

        df_pur["pur_sold"] = "purchased"

        sold_cols = [
            "hh_id",
            "sur_yr",
            "sur_mon_yr",
            "item_category",
            "sold_qty",
            "sold_cost",
            "sold_dist",
            "sold_to",
        ]

        df_sold = (
            df[sold_cols]
            .rename(
                columns={
                    "sold_cost": "market_cost",
                    "sold_dist": "dist_to_market",
                    "sold_to": "from_whom",
                    "sold_qty": "quantity",
                }
            )
            .dropna(
                axis=0,
                subset=["market_cost", "dist_to_market", "from_whom", "quantity"],
                how="all",
            )
        )

        df_sold["pur_sold"] = "sold"

        df = pd.concat([df_pur, df_sold], axis=0).reset_index(drop=True)

        # adding month column
        df["month"] = pd.to_datetime(df["sur_mon_yr"]).dt.month_name()

        # droppimg sur_mon_yr values as we have year and month capturing the necesary information
        df.drop("sur_mon_yr", axis=1, inplace=True)

        # creating total_monetary value of sale or purchase
        df["total_value"] = df["market_cost"] * df["quantity"]
        df["total_value"] = np.where(
            df["total_value"].isna(), df["market_cost"], df["total_value"]
        )  # manually verified that whenever, total cost is misisng its because quantity is missing.

        # removing missing values from the index columns
        df["from_whom"] = np.where(
            df["from_whom"].isna(), "undefined", df["from_whom"]
        )  # manully verified

        check_duplicates(
            df=df,
            index_cols=[
                "hh_id",
                "sur_yr",
                "month",
                "pur_sold",
                "item_category",
                "from_whom",
            ],
            master_check=False,
            write_file=False,
        )  # dups will betaken care it widen_frame

        # exporting long dataframe
        long_frame(
            tag=tag,
            df=df,
            cols=["market_cost", "dist_to_market", "quantity", "total_value"],
        )

        df = widen_frame(
            df=df,
            index_cols=[
                "hh_id",
                "month",
                "pur_sold",
                "item_category",
                "from_whom",
            ],
            wide_cols=["dist_to_market", "total_value"],
            agg_dict={"dist_to_market": "mean", "total_value": "sum"},
        )

        print(df)

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
