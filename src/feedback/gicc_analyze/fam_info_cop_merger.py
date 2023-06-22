import pandas as pd
from utils.dir_values import dir_values
from utils.merger_info import merger_info

raw_path, interim_path, long_path, processed_path, external_path = dir_values()


# importing family comp
def family_comp(male=False):
    tag = "Family_comp"
    file_path = long_path.joinpath(f"{tag}.csv")
    df = pd.read_csv(file_path, low_memory=False)

    df = df[df["relation"] == 1]
    # df = df[df["sur_yr"] == 2010]
    if male == False:
        df = df[df["female"] == 1]

    return df


def info_ranking():
    tag = "Info_ranking"
    file_path = long_path.joinpath(f"{tag}.csv")
    df = pd.read_csv(file_path, low_memory=False)

    # df = df[df["sur_yr"] == 2010]

    return df


def cop_mech():
    tag = "Coping_Mech"
    file_path = long_path.joinpath(f"{tag}.csv")
    df = pd.read_csv(file_path, low_memory=False)

    # df = df[df["sur_yr"] == 2010]

    return df


def fam_info_cop_merger():
    # family comp with info_ranking
    df = pd.merge(
        left=family_comp(),
        right=info_ranking(),
        left_on=["hh_id", "sur_yr", "hh_id_panel"],
        right_on=["hh_id", "sur_yr", "hh_id_panel"],
        how="inner",
        validate="1:m",
        indicator=True,
    )

    df = merger_info(df=df)

    # df = df[df["rank"] == 1]

    # merging coping mechnaism to family + info
    df = pd.merge(
        left=df,
        right=cop_mech(),
        left_on=["hh_id", "sur_yr", "hh_id_panel"],
        right_on=["hh_id", "sur_yr", "hh_id_panel"],
        how="inner",
        validate="m:m",
        indicator=True,
    )

    df = merger_info(df=df)

    # print(df[df["hh_id_panel"] == "IAPA0220"])

    # df = df.groupby(["hh_id_panel", "_merge"])["hh_id_panel"].nunique()

    # converting the merge of coping mech to long

    df = df.melt(
        id_vars=[
            "hh_id",
            "sur_yr",
            "hh_id_panel",
            "female",
            "inputs",
            "institutions",
            "rank",
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
    stata_file_path = interim_path.joinpath("stata_files/gicc_fam_info_cop_mech.csv")

    df.to_csv(stata_file_path, index=False)

    # return df


def famall_info_cop_merger():
    # family comp with info_ranking
    df = pd.merge(
        left=family_comp(male=True),
        right=info_ranking(),
        left_on=["hh_id", "sur_yr", "hh_id_panel"],
        right_on=["hh_id", "sur_yr", "hh_id_panel"],
        how="inner",
        validate="1:m",
        indicator=True,
    )

    df = merger_info(df=df)

    df = df[df["rank"] == 1]

    # merging coping mechnaism to family + info
    df = pd.merge(
        left=df,
        right=cop_mech(),
        left_on=["hh_id", "sur_yr", "hh_id_panel"],
        right_on=["hh_id", "sur_yr", "hh_id_panel"],
        how="inner",
        validate="m:m",
        indicator=True,
    )

    df = merger_info(df=df)

    # print(df[df["hh_id_panel"] == "IAPA0220"])

    # df = df.groupby(["hh_id_panel", "_merge"])["hh_id_panel"].nunique()

    # converting the merge of coping mech to long

    df = df.melt(
        id_vars=[
            "hh_id",
            "sur_yr",
            "hh_id_panel",
            "female",
            "inputs",
            "institutions",
            "rank",
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
    stata_file_path = interim_path.joinpath("stata_files/gicc_famall_info_cop_mech.csv")

    df.to_csv(stata_file_path, index=False)

    return df
