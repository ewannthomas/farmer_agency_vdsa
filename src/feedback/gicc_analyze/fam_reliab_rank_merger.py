import pandas as pd
from utils.dir_values import dir_values
from utils.merger_info import merger_info

raw_path, interim_path, long_path, processed_path, external_path = dir_values()


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

    print(df)

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


def fam_reliab_rank_merger():
    df = pd.merge(
        left=family_comp(),
        right=reliab_rank(),
        left_on=["hh_id", "sur_yr", "hh_id_panel"],
        right_on=["hh_id", "sur_yr", "hh_id_panel"],
        how="inner",
        validate="1:m",
        indicator=True,
    )

    merger_info(df)

    df.drop("_merge", axis=1, inplace=True)

    print(df)

    # final export as csv to be used in stata
    stata_file_path = interim_path.joinpath("stata_files/gicc_fam_reliab_rank.csv")

    df.to_csv(stata_file_path, index=False)
