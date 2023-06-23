import pandas as pd
from utils.dir_values import dir_values
from utils.merger_info import merger_info
from utils.coping_mech import cop_mech

interim_path, long_path, results_folder = dir_values()

"""Does households belonging to different castes adopt different coping mechanisms?"""


def gen_info():
    tag = "Gen_info"
    file_path = long_path.joinpath(f"{tag}.csv")
    df = pd.read_csv(file_path, low_memory=False)

    return df


def merger():
    df_left = gen_info()
    df_right = cop_mech()

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
def caste_cop_mech_all():
    """Table with all levels: caste, problem, adopted by, and coping mech"""

    """All necessary levels are included. Lengthy table!"""
    stats_file = results_folder.joinpath("count_caste_cop_mech_all.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            df.groupby(["caste_group", "problem", "adopted_by", "cop_mech"])[
                "hh_id_panel"
            ].nunique()
        ).reset_index()

        df = df.pivot(
            index=[
                "caste_group",
                "problem",
                "adopted_by",
            ],
            columns="cop_mech",
            values="hh_id_panel",
        ).reset_index()

        df.to_csv(stats_file, index=False)


def caste_cop_mech():
    """Table with levels: caste, and coping mech"""

    stats_file = results_folder.joinpath("count_caste_cop_mech.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            df.groupby(["caste_group", "cop_mech"])["hh_id_panel"].nunique()
        ).reset_index()

        df = df.pivot(
            index=[
                "caste_group",
            ],
            columns="cop_mech",
            values="hh_id_panel",
        ).reset_index()

        df.to_csv(stats_file, index=False)


def caste_cop_mech_problem():
    """Table with levels: caste, problem and coping mech"""

    stats_file = results_folder.joinpath("count_caste_cop_mech_problem.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            df.groupby(["caste_group", "problem", "cop_mech"])["hh_id_panel"].nunique()
        ).reset_index()

        df = df.pivot(
            index=[
                "caste_group",
                "problem",
            ],
            columns="cop_mech",
            values="hh_id_panel",
        ).reset_index()

        df.to_csv(stats_file, index=False)


# year summary tables start here:
def caste_cop_mech_all_yr():
    """Table with all levels: year, caste, problem, adopted by, and coping mech"""

    stats_file = results_folder.joinpath("count_caste_cop_mech_all_yr.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            df.groupby(["sur_yr", "caste_group", "problem", "adopted_by", "cop_mech"])[
                "hh_id_panel"
            ].nunique()
        ).reset_index()

        df = df.pivot(
            index=[
                "sur_yr",
                "caste_group",
                "problem",
                "adopted_by",
            ],
            columns="cop_mech",
            values="hh_id_panel",
        ).reset_index()

        df.to_csv(stats_file, index=False)


def caste_cop_mech_yr():
    """Table with levels: year, caste, and coping mech"""

    stats_file = results_folder.joinpath("count_caste_cop_mech_yr.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            df.groupby(["sur_yr", "caste_group", "cop_mech"])["hh_id_panel"].nunique()
        ).reset_index()

        df = df.pivot(
            index=[
                "sur_yr",
                "caste_group",
            ],
            columns="cop_mech",
            values="hh_id_panel",
        ).reset_index()

        df.to_csv(stats_file, index=False)


def caste_cop_mech_problem_yr():
    """Table with all levels: year, caste, problem, and coping mech"""

    stats_file = results_folder.joinpath("count_caste_cop_mech_problem_yr.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            df.groupby(["sur_yr", "caste_group", "problem", "cop_mech"])[
                "hh_id_panel"
            ].nunique()
        ).reset_index()

        df = df.pivot(
            index=[
                "sur_yr",
                "caste_group",
                "problem",
            ],
            columns="cop_mech",
            values="hh_id_panel",
        ).reset_index()

        df.to_csv(stats_file, index=False)
