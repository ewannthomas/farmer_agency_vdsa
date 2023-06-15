import pandas as pd
from utils.dir_values import dir_values

raw_path, interim_path, long_path, processed_path, external_path = dir_values()

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

df.to_csv(interim_file, index=False)
