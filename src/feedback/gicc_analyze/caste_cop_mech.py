import pandas as pd
from utils.dir_values import dir_values
from utils.merger_info import merger_info

from gicc_analyze.info_caste import gen_info
from gicc_analyze.fam_info_cop_merger import cop_mech

raw_path, interim_path, long_path, processed_path, external_path = dir_values()

"""Does households belonging to different castes adopt different coping mechanisms?"""


def caste_cop_mech():
    """Does households belonging to different castes adopt different coping mechanisms?"""

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

    # converting the merge of coping mech to long

    df = df.melt(
        id_vars=[
            "hh_id",
            "sur_yr",
            "hh_id_panel",
            "caste_group",
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

    # final export as csv to be used in stata
    stata_file_path = interim_path.joinpath("stata_files/caste_cop_mech.csv")

    df.to_csv(stata_file_path, index=False)

    return df
