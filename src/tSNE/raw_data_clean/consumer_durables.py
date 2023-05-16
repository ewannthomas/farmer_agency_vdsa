from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
import pandas as pd
import numpy as np


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
        df.rename(columns={"item_qty": "qty", "present_value_durable": "present_value"})

        # removing duplicates across acolumns.
        # df.drop_duplicates(
        #     inplace=True
        # )  # 870 obs will be removed. Even I'm surprised and they look legit dups. check these values more exhaustively if have time later.

        # cleaning item_name column

        df["item_name"] = df["item_name"].str.strip().str.lower()
        print(df["item_name"].value_counts())
        print(df.size)

        check_duplicates(
            df=df,
            index_cols=["hh_id", "item_name"],
            master_check=True,
            write_file=True,
        )

        # df.to_csv(interim_file, index=False)
