from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
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

        item_map = {
            "house or farm buildings": "Materials purchased for house/farm building",
            "farm machinery and implements": "Machinery & implements",
            "others": "Others",
            "investments on water exploration": "Investment on water exploration",
            "consumer durables": "Consumer durables",
            "agril land & residential plots": "Investment on soil and water conservation",
            "mat. pur. for house/farm building": "Materials purchased for house/farm building",
            "machinery and implements": "Machinery & implements",
            "inv. on water exploration": "Investment on water exploration",
            "rainfed land": "Rain-fed land",
            "others (sand)": "Others",
            "machinery & implements": "Machinery & implements",
            "motorcycle": "Consumer durables",
            "laptop": "Consumer durables",
            "irrigated land": "Irrigated land",
            "motercycle": "Consumer durables",
            "t.v": "Consumer durables",
        }

        df["item_category"] = df["item_category"].replace(item_map)

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

        df = widen_frame(
            df=df,
            index_cols=[
                "hh_id",
                "sur_mon_yr",
                "pur_sold",
                "item_category",
                "from_whom",
            ],
            wide_cols=["market_cost", "dist_to_market", "quantity"],
            agg_dict={
                "market_cost": "sum",
                "dist_to_market": "mean",
                "quantity": "sum",
            },
        )

        # print(df)

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
