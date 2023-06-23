import pandas as pd
from utils.dir_values import dir_values
from utils.merger_info import merger_info
from utils.info_ranking import info_ranking

interim_path, long_path, results_folder = dir_values()

"""Does access to information and institutions by the household vary by caste of household head?"""


def gen_info():
    tag = "Gen_info"
    file_path = long_path.joinpath(f"{tag}.csv")
    df = pd.read_csv(file_path, low_memory=False)

    return df


def merger():
    df_left = gen_info()
    df_right = info_ranking()

    df = pd.merge(
        left=df_left[["hh_id", "sur_yr", "hh_id_panel", "caste_group"]],
        right=df_right,
        on=["hh_id", "sur_yr", "hh_id_panel"],
        how="inner",
        validate="1:m",
        indicator=True,
    )

    df = merger_info(df)

    return df


# summary tables start here:
def count_caste_info():
    """Table with levels: caste and institutions"""
    stats_file = results_folder.joinpath("count_caste_info.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            df[df["rank"] == 1]
            .groupby(["caste_group", "institutions"])["hh_id_panel"]
            .nunique()
        ).reset_index()

        df = df.pivot(
            index="institutions",
            columns="caste_group",
            values="hh_id_panel",
        ).reset_index()

        df.to_csv(stats_file, index=False)


# year summary tables start here:
def count_caste_info_yr():
    """Table with levels: years, caste and institutions"""
    stats_file = results_folder.joinpath("count_caste_info_yr.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            df[df["rank"] == 1]
            .groupby(["sur_yr", "caste_group", "institutions"])["hh_id_panel"]
            .nunique()
        ).reset_index()

        df = df.pivot(
            index=["sur_yr", "institutions"],
            columns="caste_group",
            values="hh_id_panel",
        ).reset_index()

        df.to_csv(stats_file, index=False)
