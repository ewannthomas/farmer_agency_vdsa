from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
import pandas as pd
import numpy as np
import json


def building():
    """
    This function is specifically appends the buildings files in each year under the GES questionnaire.
    """

    tag = "Building"

    raw_path, interim_path, processed_path, external_path = dir_values()

    interim_file = interim_path.joinpath(f"{tag}.csv")

    if not interim_file.exists():
        east_cols = {
            "vdsid": "hh_id",
            "cult_id/hhid/vdsid": "hh_id",
            "hhid/vdsid": "hh_id",
            "val_pre": "building_value",
            "id_who_owns": "who_owns_buil",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
            "item_buil": "item_building",
            "val_buil": "building_value",
        }

        # unncecessary cols to be removed
        remove_cols = ["remarks_e_buil"]

        df = data_wrangler(
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
        )

        # cleaning the category values in the item_building column
        df["item_building"] = df["item_building"].str.strip().str.title()

        conds = [
            (df["item_building"].isin(["Type Of House", "Type Of House (Code)"])),
            (
                df["item_building"].isin(
                    [
                        "Cooking Gas (Lpg)",
                        "Cooking Gas(Lpg)",
                        "Cooking Gas (Gobar)",
                    ]
                )
            ),
            (
                df["item_building"].isin(
                    [
                        "Star Connection",
                        "Star Connection (Cable/Dish)",
                        "Cable Connection",
                    ]
                )
            ),
            (df["item_building"].isin(["Others", "Others (Specify)", "Others-Motor"])),
            (
                df["item_building"].isin(
                    ["Area Of Courtyard", "Area Of Courtyard (Sq.Feet)"]
                )
            ),
            (df["item_building"].isin(["Kerosene Stove", "Kerosen Stove"])),
        ]

        opts = [
            "Type Of House",
            "Cooking Gas",
            "Cable TV",
            "Others",
            "Area Of Courtyard",
            "Kerosene Stove",
        ]

        df["item_building"] = np.select(conds, opts, default=df["item_building"])
        # print(df['item_building'].unique())

        # pivoting values for columns specificcaly for eastindia

        conds = [
            (df["region"] == "eastindia")
            & (df["item_building"] == "Residential House")
            & (df["facility"].isna()),
            (df["region"] == "eastindia")
            & (df["item_building"] == "Type Of House")
            & (df["facility"].isna()),
            (df["region"] == "eastindia")
            & (df["item_building"] == "Area Of Courtyard")
            & (df["facility"].isna()),
            (df["region"] == "eastindia")
            & (
                ~df["item_building"].isin(
                    ["Residential House", "Type Of House", "Area Of Courtyard"]
                )
            )
            & (df["facility"].isna()),
        ]

        opts = [
            df["own_rented"].astype(str),
            df["house_type"].astype(str),
            df["courtyard_pre"].astype(str),
            df["facility_pre"].astype(str),
        ]

        df["facility"] = np.select(conds, opts, default=df["facility"])

        # bring building value from wide to long

        df_build_value = (
            df[df["item_building"] == "Residential House"]
            .melt(
                id_vars="hh_id",
                value_vars="building_value",
                var_name="item_building",
                value_name="value",
            )
            .rename(columns={"value": "facility"})
        )

        df_build_value = to_float(df=df_build_value, cols=["facility"])

        df_build_value.dropna(axis=0, subset="facility", inplace=True)

        df = pd.concat([df, df_build_value], axis=0)

        # removing wide columns from east india
        df.drop(
            [
                "own_rented",
                "house_type",
                "courtyard_pre",
                "facility_pre",
                "region",
                "who_owns_buil",
                "remarks",
                "building_value",
            ],
            axis=1,
            inplace=True,
        )

        # removing one duplicate
        # print(df.shape)
        df.drop_duplicates(
            subset=["hh_id", "item_building"], inplace=True
        )  # manually verified and removed only one obs
        # print(df.shape)

        check_duplicates(
            df=df,
            index_cols=["hh_id", "item_building"],
            master_check=False,
            write_file=True,
        )  # manually verified. One observation removed.

        df = widen_frame(df=df, index_cols=["hh_id", "item_building"])

        # print(df)

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
