import pandas as pd
from utils.dir_values import dir_values
from utils.merger_info import merger_info

# from gicc_analyze.fam_info_cop_merger import family_comp
from gicc_analyze.fam_info_cop_merger import info_ranking

raw_path, interim_path, long_path, processed_path, external_path = dir_values()

"""Does access to information and institutions by the household vary by caste of household head?"""


def gen_info():
    tag = "Gen_info"
    file_path = long_path.joinpath(f"{tag}.csv")
    df = pd.read_csv(file_path, low_memory=False)

    return df


def gen_info_ranking():
    """Does access to information and institutions by the household vary by caste of household head?"""

    df_left = gen_info()
    df_right = info_ranking()

    df = pd.merge(
        left=df_left[["hh_id", "sur_yr", "hh_id_panel", "caste_group"]],
        right=df_right,
        on=["hh_id", "sur_yr", "hh_id_panel"],
        how="inner",
        validate="1:m",
        indicator=True,
    )

    df = merger_info(df)

    # final export as csv to be used in stata
    stata_file_path = interim_path.joinpath("stata_files/gen_info_ranking.csv")

    df.to_csv(stata_file_path, index=False)

    return df
