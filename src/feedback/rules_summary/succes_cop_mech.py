import pandas as pd
from utils.dir_values import dir_values
from utils.merger_info import merger_info
from utils.coping_mech import cop_mech

interim_path, long_path, results_folder = dir_values()

"""How many households were successful?"""
"""How many households were successful in which calamity?"""
"""What coping mechanisms lead to success?"""

"""Number of tables: """


def success():
    tag = "total_cult_yr"
    file_path = long_path.joinpath(f"{tag}.csv")
    df = pd.read_csv(file_path, low_memory=False)
    return df


def merger():
    df_left = success()
    df_right = cop_mech()

    df = pd.merge(
        left=df_left,
        right=df_right,
        on=["hh_id_panel", "sur_yr"],
        how="inner",
        validate="m:m",
        indicator=True,
    )

    df = merger_info(df)

    return df


def success_count():
    """Count of successful households"""
    stats_file = results_folder.joinpath("success_count.csv")
    if not stats_file.exists():
        df = success()

        df = df.groupby(["success"])["hh_id_panel"].nunique().reset_index()

        df.to_csv(stats_file, index=False)


def success_calamity_count():
    """Count of successful households"""
    stats_file = results_folder.joinpath("success_calamity_count.csv")
    if not stats_file.exists():
        df = merger()

        df = df.groupby(["success", "problem"])["hh_id_panel"].nunique().reset_index()

        df = df.pivot(
            index="problem", columns="success", values="hh_id_panel"
        ).reset_index()

        df.to_csv(stats_file, index=False)


def success_cop_mech():
    """Number of successful households by coping mechanisms"""
    stats_file = results_folder.joinpath("success_cop_mech.csv")
    if not stats_file.exists():
        df = merger()

        df = df.groupby(["cop_mech", "success"])["hh_id_panel"].nunique().reset_index()

        df = df.pivot(
            index="cop_mech", columns="success", values="hh_id_panel"
        ).reset_index()

        df.to_csv(stats_file, index=False)


def success_cop_mech_yr():
    """Number of successful households by coping mechanisms"""
    stats_file = results_folder.joinpath("success_cop_mech_yr.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            df.groupby(["sur_yr", "cop_mech", "success"])["hh_id_panel"]
            .nunique()
            .reset_index()
        )

        df = df.pivot(
            index="cop_mech", columns=["sur_yr", "success"], values="hh_id_panel"
        ).reset_index()

        df.to_csv(stats_file, index=False)
