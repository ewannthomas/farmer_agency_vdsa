import pandas as pd
from utils.dir_values import dir_values
from utils.merger_info import merger_info
from utils.coping_mech import cop_mech

interim_path, long_path, results_folder = dir_values()

"""Does coping mechanism adopted by a household vary by the features of land owned?"""


def land():
    tag = "Landholding"
    file_path = long_path.joinpath(f"{tag}.csv")
    df = pd.read_csv(file_path, low_memory=False)
    return df


def merger():
    df_left = land()
    df_right = cop_mech()

    df = pd.merge(
        left=df_left,
        right=df_right,
        on=["hh_id", "sur_yr", "hh_id_panel"],
        how="outer",
        validate="m:m",
        indicator=True,
    )

    df = merger_info(df)

    return df


# Feature 1 : Soil Type
def soil_type():
    stats_file = results_folder.joinpath("soil_type_cop_mech.csv")
    if not stats_file.exists():
        df = merger()

        df = df.groupby(["soil_type"])["hh_id_panel"].nunique().reset_index()

        print(df)
