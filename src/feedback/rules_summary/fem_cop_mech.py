import pandas as pd
from utils.dir_values import dir_values
from utils.merger_info import merger_info
from utils.coping_mech import cop_mech

interim_path, long_path, results_folder = dir_values()

"""How many female headed households adopted what coping mechanism for each calamity?"""


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
        right=cop_mech(),
        left_on=["hh_id", "sur_yr", "hh_id_panel"],
        right_on=["hh_id", "sur_yr", "hh_id_panel"],
        how="inner",
        validate="1:m",
        indicator=True,
    )

    df = merger_info(df=df)

    # print(df)

    return df


# summary tables start here
def count_fem_hh_cop_mech():
    """Table with levels: problem, coping mechanism"""

    stats_file = results_folder.joinpath("count_fem_hh_cop_mech.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            (df.groupby(["problem", "cop_mech"])["hh_id_panel"].nunique())
            .reset_index()
            .pivot(index=["cop_mech"], columns="problem", values="hh_id_panel")
            .reset_index()
        )
        df.to_csv(stats_file, index=False)


# year summary tables start here:
def count_fem_hh_cop_mech_yr():
    """Table with levels: problem, coping mechanism"""

    stats_file = results_folder.joinpath("count_fem_hh_cop_mech_yr.csv")
    if not stats_file.exists():
        df = merger()

        df = (
            (df.groupby(["sur_yr", "problem", "cop_mech"])["hh_id_panel"].nunique())
            .reset_index()
            .pivot(
                index=["sur_yr", "cop_mech"], columns="problem", values="hh_id_panel"
            )
            .reset_index()
        )
        df.to_csv(stats_file, index=False)
