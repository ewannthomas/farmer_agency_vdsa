from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
from utils.long_frame import long_frame
import pandas as pd
import numpy as np
import json


def cult_inputs():
    """
    This function is specifically cleans the cultivation input files in each year under the Cultivation questionnaire.
    """

    tag = "Cult_ip"

    raw_path, interim_path, processed_path, external_path = dir_values()

    interim_file = interim_path.joinpath(f"{tag}.csv")

    if not interim_file.exists():
        east_cols = {
            "vdsid": "hh_id",
            "cult_id/hhid/vdsid": "hh_id",
            "remarks": "crop_ip_remarks",
            "ip_remarks": "crop_ip_remarks",
            "ow_stat": "plot_ownership_status",
            "rent_for": "rent_tenure",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
            "year_total_income": "hh_id",
            "plot_co": "plot_code",
            "remarks": "crop_ip_remarks",
            "ip_remarks": "crop_ip_remarks",
        }

        # unncecessary cols to be removed
        remove_cols = ["plot_name", "round_no", "village"]

        df = data_wrangler(
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
        )

        # cleaning sur_mon_yr column
        df["sur_mon_yr"] = df["sur_mon_yr"].str.strip()
        conds = [
            (df["hh_id"] == "IOR14A0010") & (df["sur_mon_yr"].astype(str) == "12 14"),
            (df["hh_id"] == "IOR14A0033") & (df["sur_mon_yr"].astype(str) == "06 14"),
            (df["hh_id"] == "IOR14A0041") & (df["sur_mon_yr"].astype(str) == "12 14"),
            (df["hh_id"] == "IOR14A0046") & (df["sur_mon_yr"].astype(str) == "12"),
            (df["hh_id"] == "IOR14A0047") & (df["sur_mon_yr"].astype(str) == "12/"),
            (df["hh_id"] == "IOR14A0050") & (df["sur_mon_yr"].astype(str) == "11"),
            (df["hh_id"] == "IAP10D0047") & (df["sur_mon_yr"].astype(str) == "12 10"),
            (df["hh_id"] == "IKN10A0037") & (df["sur_mon_yr"].astype(str) == "08 10"),
            (df["hh_id"] == "IKN10A0038") & (df["sur_mon_yr"].astype(str) == "07 10"),
        ]

        opts = [
            "12/14",
            "6/14",
            "12/14",
            "12/14",
            "12/14",
            "11/14",
            "12/10",
            "8/10",
            "7/10",
        ]

        df["sur_mon_yr"] = np.select(conds, opts, default=df["sur_mon_yr"].astype(str))

        # making the date column correct
        df["sur_mon_yr"] = pd.to_datetime(df["sur_mon_yr"], format="%m/%y")

        # cleaning categorical variables
        # cleaning lab_type
        lab_type_mapping = {
            "FM": "Family Male",
            "HM": "Hired Male",
            "EM": "Exchange Male",
            "FF": "Family Female",
            "HF": "Hired Female",
            "EF": "Exchange Female",
            "FC": "Family Child",
            "HC": "Hired Child",
            "EC": "Exchange Child",
            "OB": "Own Bullocks",
            "HB": "Hired Bullocks",
            "EB": "Exchange Bullocks",
            "TR": "Tractor",
            "PT": "Power Tiller",
            "CH": "Combined Harvester",
            "SP": "Sprayer",
            "SD": "Seed Drill",
            "MK": "BBF Marker",
            "DS": "Duster",
            "ET": "Electric Motor",
            "RS": "Regular farm servant",
            "SM": "Submersible pump",
            "TH": "Thresher",
            "DP": "Diesel pump",
        }

        df["lab_type"] = df["lab_type"].map(
            lab_type_mapping
        )  # map() is used to remove 3 vague obs with values 0,6,B

        # cleaning operatins columns
        df["operation"] = df["operation"].str.strip()

        operations_map = "./src/tSNE/raw_data_clean/cultivation_operations_map.json"
        with open(operations_map, "r") as in_file:
            crop_ops_type = dict(json.load(in_file))

        df["operation"] = df["operation"].replace(crop_ops_type)

        # creating total labour cost and material cost
        df["val_mat"] = np.where(df["val_mat"].str.isdigit(), df["val_mat"], "")
        df = to_float(df=df, cols=["work_hr", "wage", "val_mat"], error_action="raise")
        df = to_float(
            df=df, cols=["val_mat"], error_action="raise"
        )  # the converted values were checked and their missing value count was also verified. You have nothing to worry. This operation didnot remove any existing data
        df["labour_cost"] = df["work_hr"] * df["wage"]

        # renaming value of material as material cost
        df.rename(columns={"val_mat": "material_cost"}, inplace=True)

        # adding month column
        df["month"] = pd.to_datetime(df["sur_mon_yr"]).dt.month_name()

        # droppimg sur_mon_yr values as we have year and month capturing the necesary information
        df.drop("sur_mon_yr", axis=1, inplace=True)

        check_duplicates(
            df=df,
            index_cols=["hh_id", "month", "plot_code", "season", "operation"],
            master_check=False,
            write_file=True,
        )

        # exporting long dataframe
        long_frame(tag=tag, df=df)

        # widening the frame
        df = widen_frame(
            df=df,
            index_cols=["hh_id", "month", "plot_code", "season", "operation"],
            wide_cols=["labour_cost", "material_cost"],
            agg_dict={"labour_cost": "sum", "material_cost": "sum"},
        )

        print(df)

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
