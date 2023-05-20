from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
import pandas as pd
import numpy as np


def govt_assist():
    """
    This function is specifically cleans the govt progam assistance files in each year under the GES questionnaire.
    """

    tag = "Govt_assist"

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
        remove_cols = ["is_prog_active"]

        df = data_wrangler(
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
        )
        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
