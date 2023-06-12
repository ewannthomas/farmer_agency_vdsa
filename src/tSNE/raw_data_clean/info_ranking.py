from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
from utils.long_frame import long_frame
import pandas as pd
import numpy as np
import json


def info_ranking():
    """
    This function is specifically cleans the Info ranking files in each year under the GES questionnaire.
    """

    tag = "Info_ranking"

    raw_path, interim_path, processed_path, external_path = dir_values()

    interim_file = interim_path.joinpath(f"{tag}.csv")

    if not interim_file.exists():
        east_cols = {
            "vdsid": "hh_id",
            "item_info": "inputs",
            "input_dealer": "Input Dealer",
            "seed_comp": "Seed Company",
            "farmers": "Other Farmers",
            "ngo": "NGO",
            "govt_dept": "Agriculture/Veterinary Dept",
            "kvk": "Research Station",
            "media": "Media",
            "krishi_melas": "Krishi-melas",
            "others": "Others",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
            "input_dealer": "Input Dealer",
            "seed_comp": "Seed Company",
            "ot_farmers": "Other Farmers",
            "ngo": "NGO",
            "agri_vete_dept": "Agriculture/Veterinary Dept",
            "rese_station": "Research Station",
            "media": "Media",
            "krishi_melas": "Krishi-melas",
            "others": "Others",
        }

        # unncecessary cols to be removed
        remove_cols = []

        df = data_wrangler(
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
        )
        # removing duplicate values
        df.drop_duplicates(inplace=True)  # manually verifed. Will remove 4 obs

        # cleaning inputs column
        df["inputs"] = df["inputs"].str.strip().str.lower()

        inputs_dict = {
            "cattle/poultry disease": "treatment of cattle/poultry diseases",
            "treatment of cattle/poultry": "treatment of cattle/poultry diseases",
            "seed selection": "seed selection and storage",
            "seed selection & storage": "seed selection and storage",
            "use of fertilizer": "chemical fertilizer",
            "use of pesticide": "use of pesticides",
            "wheather information": "weather information",
        }

        df["inputs"] = df["inputs"].replace(inputs_dict)

        # removing duplicate values post cleanin input values
        df.drop_duplicates(
            ["hh_id", "inputs"], inplace=True
        )  # manually verifed. Will remove 1 obs

        # renaming columns
        df.rename(
            columns={
                "rese_station": "research_station",
                "ip_manu": "input_manufacturer",
            },
            inplace=True,
        )

        # converting rank columns to float
        df = to_float(df=df, cols=df.columns[3:])

        check_duplicates(
            df=df, index_cols=["hh_id", "inputs"], master_check=False, write_file=True
        )

        # exporting long dataframe
        long_frame(tag=tag, df=df)

        df = widen_frame(df=df, index_cols=["hh_id", "inputs"])

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
