import pandas as pd
from utils.dir_values import dir_values
from utils.merger_info import merger_info

interim_path, long_path, results_folder = dir_values()

"""What are the institutions which female headed households trust the most for assisstance during a calamity?"""


def reliab_rank():
    tag = "Reliability_ranking"
    file_path = long_path.joinpath(f"{tag}.csv")
    df = pd.read_csv(file_path, low_memory=False)

    df = df.melt(
        id_vars=["hh_id", "sur_yr", "hh_id_panel", "sou_assistance"],
        value_vars=["reliab_rank_in_drought", "reliab_rank_in_flood"],
        var_name="calamity",
        value_name="reliab_rank",
    )

    df["calamity"] = df["calamity"].str.replace("reliab_rank_in_", "")

    # print(df)

    # df = df[df["sur_yr"] == 2010]

    return df


def family_comp():
    tag = "Family_comp"
    file_path = long_path.joinpath(f"{tag}.csv")
    df = pd.read_csv(file_path, low_memory=False)

    df = df[df["relation"] == 1]
    # df = df[df["sur_yr"] == 2010]
    df = df[df["female"] == 1]

    df = df[["hh_id", "sur_yr", "hh_id_panel", "female"]]

    return df


def merger():
    df = pd.merge(
        left=family_comp(),
        right=reliab_rank(),
        left_on=["hh_id", "sur_yr", "hh_id_panel"],
        right_on=["hh_id", "sur_yr", "hh_id_panel"],
        how="inner",
        validate="1:m",
        indicator=True,
    )

    df = merger_info(df)

    # print(df)

    return df


# summary tables start here
def count_fem_hh_reliab_rank():
    """Table with levels: sou_assistance, drought and flood"""
    stats_file = results_folder.joinpath("count_fem_hh_reliab_rank.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            (
                df[df["reliab_rank"] == 1]
                .groupby(["calamity", "sou_assistance"])["hh_id_panel"]
                .nunique()
            )
            .reset_index()
            .rename(columns={"hh_id_panel": "count of female hh"})
        )

        df = df.pivot(
            index="sou_assistance",
            columns="calamity",
            values="count of female hh",
        ).reset_index()

        df.to_csv(stats_file, index=False)


# year summary tables start here
def count_fem_hh_reliab_rank_yr():
    stats_file = results_folder.joinpath("count_fem_hh_reliab_rank_yr.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            df[df["reliab_rank"] == 1]
            .groupby(["sur_yr", "calamity", "sou_assistance"])["hh_id_panel"]
            .nunique()
        ).reset_index()

        df = (
            df.pivot(
                index=["sur_yr", "calamity"],
                columns="sou_assistance",
                values="hh_id_panel",
            )
            .reset_index()
            .sort_values(by=["calamity", "sur_yr"])
        )

        df.to_csv(stats_file, index=False)
