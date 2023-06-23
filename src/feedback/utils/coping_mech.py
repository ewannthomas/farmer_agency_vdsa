import pandas as pd
from utils.dir_values import dir_values

interim_path, long_path, results_folder = dir_values()


def cop_mech():
    """A function to convert coping mechnaism dataset in long_data folder to further long along columns cop_mech_m_* and cop_mech_f_*"""
    """This function doesn't alter the data at source and requires to be called everytime when the long form of the coping mechanism dataset is required."""
    tag = "Coping_Mech"

    interim_file = long_path.joinpath(f"{tag}.csv")

    df = pd.read_csv(interim_file)

    df = df.melt(
        id_vars=[
            "hh_id",
            "sur_yr",
            "hh_id_panel",
            "ado_co_me",
            "problem",
            "percent_of_income_lost",
            "losses_in_rupees",
        ],
        value_vars=[
            "cop_mech_f1",
            "cop_mech_f2",
            "cop_mech_f3",
            "cop_mech_f4",
            "cop_mech_f5",
            "cop_mech_f6",
            "cop_mech_m1",
            "cop_mech_m2",
            "cop_mech_m3",
            "cop_mech_m4",
            "cop_mech_m5",
            "cop_mech_m6",
        ],
        var_name="adopted_by",
        value_name="cop_mech",
    )

    return df
