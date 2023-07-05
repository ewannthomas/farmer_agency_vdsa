import pandas as pd
from utils.dir_values import dir_values
from utils.merger_info import merger_info
from utils.coping_mech import cop_mech

interim_path, long_path, results_folder = dir_values()

"""How many male and female headed households adopted which coping mechanism and was successful?"""


# importing family comp
def family_comp():
    tag = "Family_comp"
    file_path = long_path.joinpath(f"{tag}.csv")
    df = pd.read_csv(file_path, low_memory=False)

    df = df[df["relation"] == 1]
    # df = df[df["female"] == 1]
    return df


# importing success
def success():
    tag = "total_cult_yr"
    file_path = long_path.joinpath(f"{tag}.csv")
    df = pd.read_csv(file_path, low_memory=False)
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


def merger_2():
    # family comp with info_ranking
    df = pd.merge(
        left=merger(),
        right=success(),
        left_on=["sur_yr", "hh_id_panel"],
        right_on=["sur_yr", "hh_id_panel"],
        how="outer",
        validate="m:1",
        indicator=True,
    )

    df = merger_info(df=df)

    # print(df)

    return df


# summary tables start here
def success_gender_cop_mech():
    """Table with levels: problem, coping mechanism"""

    stats_file = results_folder.joinpath("success_gender_cop_mech.csv")
    if not stats_file.exists():
        df = merger_2()

        df = (
            (df.groupby(["success", "female", "cop_mech"])["hh_id_panel"].nunique())
            .reset_index()
            .pivot(
                index=["cop_mech"], columns=["female", "success"], values="hh_id_panel"
            )
            .reset_index()
        )
        df.to_csv(stats_file, index=False)


# year summary tables start here:
def success_gender_cop_mech_yr():
    """Table with levels: problem, coping mechanism"""

    stats_file = results_folder.joinpath("success_gender_cop_mech_yr.csv")
    if not stats_file.exists():
        df = merger_2()

        df = (
            (
                df.groupby(["sur_yr", "female", "success", "cop_mech"])[
                    "hh_id_panel"
                ].nunique()
            )
            .reset_index()
            .pivot(
                index=["cop_mech", "female"],
                columns=["sur_yr", "success"],
                values="hh_id_panel",
            )
            .reset_index()
        )
        df.to_csv(stats_file, index=False)
