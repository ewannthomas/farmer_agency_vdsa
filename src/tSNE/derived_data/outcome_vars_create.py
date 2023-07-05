from utils.dir_for_derived import dir_values
from utils.widen_frame import widen_frame
from utils.long_frame import long_frame
import pandas as pd
import numpy as np

# defining directories
interim_path, results_path, long_data_path = dir_values()


def total_production_create(tag: str):
    """A function to create the total cultivation variable for each household by either crop type and year or just by year .
    Input file: Crop_info_op.csv
    Output: Total production by household for each crop in each year
    """

    input_file = long_data_path.joinpath("Crop_info_op.csv")

    df = pd.read_csv(input_file)

    df["main_prod_total"] = df["op_main_prod_qty"] * df["op_main_prod_rate"]
    df["by_prod_total"] = df["op_by_prod_qty"] * df["op_by_prod_rate"]
    df["ot_prod_total"] = df["op_ot_prod_qty"] * df["op_ot_prod_rate"]

    df["total_prodn"] = df[
        [
            "main_prod_total",
            "by_prod_total",
            "ot_prod_total",
        ]
    ].sum(axis=1, skipna=True)

    # filetring out fallows
    df = df[df["crop_type"] != "Fallow"]  # manually verified the numbers. All good!
    # creating total production of each household at hh, crop type and year level

    if tag == "total_cult_crop":
        df = (
            df.groupby(
                [
                    "hh_id_panel",
                    "crop_type",
                    "sur_yr",
                ]
            )["total_prodn"]
            .sum()
            .reset_index()
        )

    elif tag == "total_cult_yr":
        df = (
            df.groupby(
                [
                    "hh_id_panel",
                    "sur_yr",
                ]
            )["total_prodn"]
            .sum()
            .reset_index()
        )

    return df


def first_diff_create(tag: str):
    """This function creates the first difference values from the total production variable"""
    df = total_production_create(tag)

    # print(df)

    # creating the difference in values

    if tag == "total_cult_crop":
        df["diff"] = df.groupby(
            [
                "hh_id_panel",
                "crop_type",
            ]
        )[
            "total_prodn"
        ].diff(periods=1, axis=0)

    elif tag == "total_cult_yr":
        df["diff"] = df.groupby("hh_id_panel")["total_prodn"].diff(periods=1, axis=0)

    return df


def success_create(tag: str):
    """This function check the sign of the  first difference variable or direction of growth of total production varibale to classify households as success or failure."""
    df = first_diff_create(tag)

    # creating the success variable
    conds = [
        df["diff"] > 0,
        df["diff"] < 0,
        df["diff"].isna(),
        df["diff"] == 0,
    ]
    opts = [1, 0, 1, 1]
    df["success"] = np.select(conds, opts, default=999)

    # print(df["success"].value_counts(dropna=False))

    # print(df.shape)

    if tag == "total_cult_crop":
        df = df.groupby(
            [
                "hh_id_panel",
                "crop_type",
            ]
        )

    elif tag == "total_cult_yr":
        df = df.groupby("hh_id_panel")

    proxy_list = []

    for i in df:
        i[1]["success"] = i[1]["success"].product(
            skipna=True
        )  # taking a product will isolate all the hh which has only 1. If there exists any 0, the entire hh crop category wiil be 0.

        if i[1]["success"].eq(0).all():
            if (i[1]["diff"] > 0).any():
                i[1][
                    "success"
                ] = (
                    np.nan
                )  # redefining success to missing to exclue hh with mixed values

        if i[1]["total_prodn"].eq(0).all():
            i[1]["success"] = 0  # making hh with zero prodn across years as failed

        # making success nan for housheolds with only one year of prodcution
        if len(i[1]) == 1:
            i[1]["success"] = np.nan

        # if i[1]["success"].isna().all():
        #     print(i[1])

        # holdimg data in proxy list to append it back
        proxy_list.append(i[1])

    df = pd.concat(proxy_list, axis=0)

    # print(df["success"].value_counts(dropna=False))

    # print(df)

    return df


def outcome_vars_create():
    """This fucntion creates two datastes with the outcome variable success based on the tag provided to it.

    Dataset 1: (tag=total_cult_crop) creates success and total production at hh, crop type, year level.

    Dataset 2: (tag=total_cult_yr) creates success and total production at hh, year level
    """
    tags = ["total_cult_crop", "total_cult_yr"]

    for tag in tags:
        interim_file = interim_path.joinpath(f"{tag}.csv")

        if not interim_file.exists():
            df = success_create(tag)

            # sending long frame to long_data folder
            long_frame(
                df=df,
                tag=tag,
                hh_id=False,
            )

            if tag == "total_cult_crop":
                cols = ["hh_id_panel", "crop_type"]
            elif tag == "total_cult_yr":
                cols = ["hh_id_panel"]
            # widening frame
            df = widen_frame(df=df, index_cols=cols, hh_id=False)

            # print(df)

            df.to_csv(interim_file, index=False)

        else:
            print(f"{tag} derived file exists.")
