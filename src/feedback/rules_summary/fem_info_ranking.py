import pandas as pd
from utils.dir_values import dir_values
from utils.merger_info import merger_info
from utils.info_ranking import info_ranking

interim_path, long_path, results_folder = dir_values()

"""How many female headed households gave highest rank for information from institutions?"""
"""How many female headed households sought information from institutions for which inputs?"""


# importing family comp
def family_comp():
    tag = "Family_comp"
    file_path = long_path.joinpath(f"{tag}.csv")
    df = pd.read_csv(file_path, low_memory=False)

    df = df[df["relation"] == 1]
    df = df[df["female"] == 1]
    return df


def merger():
    # family comp with info_ranking
    df = pd.merge(
        left=family_comp(),
        right=info_ranking(),
        left_on=["hh_id", "sur_yr", "hh_id_panel"],
        right_on=["hh_id", "sur_yr", "hh_id_panel"],
        how="inner",
        validate="1:m",
        indicator=True,
    )

    df = merger_info(df=df)

    # print(df)

    return df


# summary tables start here:
def count_fem_hh_institutions():
    """Table with levels: institutions for all female headed households"""
    stats_file = results_folder.joinpath("count_fem_hh_institutions.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            df[df["rank"] == 1].groupby(["institutions"])["hh_id_panel"].nunique()
        ).reset_index()
        df.to_csv(stats_file, index=False)


def count_fem_hh_inputs():
    """Table with levels: inputs for all female headed households"""
    stats_file = results_folder.joinpath("count_fem_hh_inputs.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            df[df["rank"] == 1].groupby(["inputs"])["hh_id_panel"].nunique()
        ).reset_index()
        df.to_csv(stats_file, index=False)


# year summary tables start here:
def count_fem_hh_institutions_yr():
    """Table with levels: year and institutions for all female headed households"""
    stats_file = results_folder.joinpath("count_fem_hh_institutions_yr.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            df[df["rank"] == 1]
            .groupby(["sur_yr", "institutions"])["hh_id_panel"]
            .nunique()
        ).reset_index()

        df = df.pivot(
            index="sur_yr", columns="institutions", values="hh_id_panel"
        ).reset_index()
        df.to_csv(stats_file, index=False)


def count_fem_hh_inputs_yr():
    """Table with levels: year and institutions for all female headed households"""
    stats_file = results_folder.joinpath("count_fem_hh_inputs_yr.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            df[df["rank"] == 1].groupby(["sur_yr", "inputs"])["hh_id_panel"].nunique()
        ).reset_index()

        df = df.pivot(
            index="sur_yr", columns="inputs", values="hh_id_panel"
        ).reset_index()
        df.to_csv(stats_file, index=False)
