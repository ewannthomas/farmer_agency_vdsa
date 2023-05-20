from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
import pandas as pd
import numpy as np
import json


def proact_measures():
    """
    This function is specifically cleans the proactive measures files in each year under the GES questionnaire.
    """

    tag = "Proactive_measure"

    raw_path, interim_path, processed_path, external_path = dir_values()

    interim_file = interim_path.joinpath(f"{tag}.csv")

    if not interim_file.exists():
        east_cols = {
            "vdsid": "hh_id",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
        }

        # unncecessary cols to be removed
        remove_cols = []

        df = data_wrangler(
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
        )

        # removing duplicates
        df.drop_duplicates(inplace=True)  # manually verified and will remove 7 entries

        # cleaning ctive measure columnn
        df["proac_mea"] = df["proac_mea"].str.strip().str.lower()
        # pd.Series(df["proac_mea"].unique()).to_csv(interim_file)
        # print(df["proac_mea"].unique())
        # print(df["proac_mea"].nunique())

        # renamimg variables
        df.rename(
            cplumns={
                "ad_proac_mea": "adopted_proact_measures",
                "proac_mea": "proact_measure",
            }
        )

        check_duplicates(df=df, index_cols=[], master_check=True, write_file=True)

        # df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
