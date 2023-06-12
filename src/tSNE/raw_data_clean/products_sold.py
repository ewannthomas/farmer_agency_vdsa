from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
from utils.long_frame import long_frame
import pandas as pd
import numpy as np
import json


def products_sold():
    """
    This function is specifically appends the products sold files in each year under the Transaction questionnaire.
    """

    tag = "Prod_Sold"

    raw_path, interim_path, processed_path, external_path = dir_values()

    interim_file = interim_path.joinpath(f"{tag}.csv")

    if not interim_file.exists():
        east_cols = {
            "vdsid": "hh_id",
            "cult_id/hhid/vdsid": "hh_id",
            "hhid/vdsid": "hh_id",
        }

        sat_cols = {"vds_id": "hh_id", "vdsid": "hh_id"}

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

        # cleaning crop list
        df["crop_lst_prod"] = df["crop_lst_prod"].str.strip().str.title()

        df["crop_lst_prod"] = np.where(
            df["crop_lst_prod"] != "Crop", "Livestock Products", "Crop"
        )

        # cleaning the sold_in_out column
        sold_map = {
            0: "Within Village",
            1: "Within Village",
            6: "Within Village",
            2: "Outside Village",
        }
        df["sold_in_out"] = df["sold_in_out"].replace(sold_map)

        # cleaning sold_to_co column
        sold_to_map = {
            1: "Fellow farmer",
            10: "Fellow farmer",
            2: "Shop",
            3: "Broker",
            4: "Moneylender",
            5: "Input supplier",
            6: "Co-operative",
            7: "Trader/Commission agent",
            8: "Processor",
            9: "Others",
        }
        df["sold_to_co"] = df["sold_to_co"].replace(sold_to_map)

        # converting numeric cols to float
        df = to_float(
            df=df,
            cols=["qty_sold", "unit_pri", "os_dist", "os_mar_costs"],
            error_action="raise",
        )

        # creating total sales value
        df["total_sales"] = df["qty_sold"] * df["unit_pri"]

        # creating outside village market cost
        df["outside_village_market_cost"] = df["qty_sold"] * df["os_mar_costs"]

        # removing duplicates
        df.drop_duplicates(
            inplace=True
        )  # manually verified. Will remove 6 observations

        check_duplicates(
            df=df, index_cols=["hh_id"], master_check=True, write_file=True
        )

        # exporting long dataframe
        long_frame(
            tag=tag,
            df=df,
            cols=["total_sales", "os_dist", "outside_village_market_cost"],
        )

        df = widen_frame(
            df=df,
            index_cols=[
                "hh_id",
                "sur_mon_yr",
                "crop_lst_prod",
                "sold_in_out",
                "sold_to_co",
            ],
            wide_cols=["total_sales", "os_dist", "outside_village_market_cost"],
            agg_dict={
                "total_sales": "sum",
                "outside_village_market_cost": "sum",
                "os_dist": "mean",
            },
        )

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
