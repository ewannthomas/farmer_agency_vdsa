from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
from utils.long_frame import long_frame
from utils.to_float import to_float
import pandas as pd
import numpy as np


def family_comp():
    """
    This function is specifically cleans the Family composition block file in each year under the GES questionnaire.
    """
    tag = "Family_comp"

    raw_path, interim_path, processed_path, external_path = dir_values()

    interim_file = interim_path.joinpath(f"{tag}.csv")

    if not interim_file.exists():
        east_cols = {
            "vdsid": "hh_id",
            "mari_yr": "marriage_yr",
            "subs_occcp": "subs_occp",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "yr_stop_edu": "yr_edu_ter",
            "rel": "relation",
            "rel_ot": "relation_ot",
        }

        # unncecessary cols to be removed
        remove_cols = [
            "mem_org_name_ot",  # these columns are empty and hence removed for this block
            "os_purpose_ot",
            "work_own_farm",
            "ot_occp",
            "edu_dist",
            "edu_place",
            "yrs_memship",
            "outside_since",
            "mem_name",
            "remarks",  # values from here onwards are expected not to add any value and removed. The have valid entries
            "remarks_a",
            "old_mem_id",
            "pre_mem_id",
            "mem_org_name",
            "ch_stat_ot",
            "relation_ot",
            "mari_stat_ot",
            "rea_stop_edu_ot",
            "main_occp_ot",
            "subs_occp_ot",
            "os_purpose",
            "spouse_m_id",
            "spouse_f_id",
            "child_m_id",
            "child_f_id",
            "edu_level_ot",
        ]

        df = data_wrangler(
            tag=tag, rename_east=east_cols, rename_sat=sat_cols, remove_cols=remove_cols
        )

        # CLEANING DUPLICATES #######################################################################
        # removing duplicates across all column
        df.drop_duplicates(
            inplace=True
        )  # manually checked and removes 4 obs which are pure duplicates

        # Manually removing duplicates for specific households if gender is missing
        # IBH14C0057
        df = df[
            ~(
                (df["hh_id"] == "IBH14C0057")
                & (df["sl_no"] == 5)
                & (df["ch_stat"] == 1)
                & (df["gender"].isna())
            )
        ]
        # IBH14D0010
        df = df[
            ~(
                (df["hh_id"] == "IBH14D0010")
                & (df["sl_no"] == 3)
                & (df["ch_stat"] == 1)
                & (df["gender"].isna())
            )
        ]
        # Manually removing duplicates for specific households if age is increasing by 1
        # IBH12C0046
        df = df[
            ~(
                (df["hh_id"] == "IBH12C0046")
                & (df["sl_no"] == 5)
                & (df["ch_stat"] == 0)
                & (df["age"] == 2)
            )
        ]

        # IOR12C0042
        df = df[
            ~(
                (df["hh_id"] == "IOR12C0042")
                & (df["sl_no"] == 3)
                & (df["ch_stat"] == 0)
                & (df["age"] == 15)
            )
        ]

        # IOR13B0202
        df = df[
            ~(
                (df["hh_id"] == "IOR13B0202")
                & (df["sl_no"] == 3)
                & (df["ch_stat"] == 0)
                & (df["age"] == 1)
            )
        ]

        # Recoding male memeber value of household IJH11C0004 to remove duplicates
        conds = (
            (df["hh_id"] == "IJH11C0004")
            & (df["sl_no"] == 1)
            & (df["ch_stat"] == 0)
            & (df["gender"] == "M")
        )

        df["sl_no"] = np.where(conds, 4, df["sl_no"])

        #######################################################################################

        # cleaning gender column
        gender_dict = {"m": 0, "f": 1, "male": 0, "female": 1}
        df["gender"] = df["gender"].str.strip().str.lower()
        df["gender"] = df["gender"].replace(gender_dict)

        # cleaning liv_wf_os columns
        family_dict = {"family": "with family"}
        df["liv_wf_os"] = df["liv_wf_os"].str.strip().str.lower()
        df["liv_wf_os"] = df["liv_wf_os"].replace(family_dict)

        # cleaning age column
        # print(df["age"].isna().value_counts())
        df["age_new"] = np.where(df["age"].str.isnumeric(), df["age"], 9999)
        df["age"] = df["age"].str.strip().str.lower()

        conds = [
            (df["age"] == "5 months") & (df["age_new"] == 9999),
            (df["age"] == "6 months") & (df["age_new"] == 9999),
            (df["age"] == "4months") & (df["age_new"] == 9999),
            (df["age"] == "7months") & (df["age_new"] == 9999),
            (df["age"] == "1 month") & (df["age_new"] == 9999),
            (df["age"] == "4 months") & (df["age_new"] == 9999),
            (df["age"] == "1month") & (df["age_new"] == 9999),
            (df["age"] == "11 months") & (df["age_new"] == 9999),
            (df["age"] == "10 months") & (df["age_new"] == 9999),
            (df["age"] == "7 months") & (df["age_new"] == 9999),
            (df["age"] == "8 months") & (df["age_new"] == 9999),
            (df["age"] == "9 months") & (df["age_new"] == 9999),
            (df["age"] == "6months") & (df["age_new"] == 9999),
            (df["age"] == "3 months") & (df["age_new"] == 9999),
            (df["age"] == "6m") & (df["age_new"] == 9999),
            (df["age"] == "2m") & (df["age_new"] == 9999),
            (df["age"] == "2 months") & (df["age_new"] == 9999),
            (df["age"] == "28 days") & (df["age_new"] == 9999),
            (df["age"] == "18 days") & (df["age_new"] == 9999),
            (df["age_new"] == 9999),
        ]
        opts = [
            "0.42",
            "0.5",
            "0.33",
            "0.58",
            "0.083",
            "0.33",
            "0.083",
            "0.92",
            "0.83",
            "0.58",
            "0.667",
            "0.75",
            "0.5",
            "0.25",
            "0.5",
            "0.167",
            "0.167",
            "0.078",
            "0.05",
            np.nan,
        ]

        df["age_new"] = np.select(conds, opts, default=df["age_new"])
        df["age_new"] = df["age_new"].astype(float)  # manually verified
        df.drop("age", axis=1, inplace=True)

        df.rename(columns={"gender": "female", "age_new": "age"}, inplace=True)

        # For some reason remove_cols is not catching this column. So initiating a specific removal.
        df.drop("relation_ot", axis=1, inplace=True)

        ###############################################################################################################
        # this is a special move to remove members whio changed their status in the household by marriage, migration etc and are thus repeating themselves.
        # we observe 22 such obs and hence 11 will be removed. All entries were manually verified by inspecting the dups.csv created by check_duplicates util function
        # removing duplicates across ch_stat variables in 22 obs

        # IBH12C0035
        df = df[
            ~((df["hh_id"] == "IBH12C0035") & (df["sl_no"] == 5) & (df["ch_stat"] == 1))
        ]

        # IBH14D0038 fuur memeber of this family changed status
        df = df[
            ~((df["hh_id"] == "IBH14D0038") & (df["sl_no"] == 6) & (df["ch_stat"] == 0))
        ]

        df = df[
            ~((df["hh_id"] == "IBH14D0038") & (df["sl_no"] == 7) & (df["ch_stat"] == 0))
        ]
        df = df[
            ~((df["hh_id"] == "IBH14D0038") & (df["sl_no"] == 8) & (df["ch_stat"] == 0))
        ]
        df = df[
            ~((df["hh_id"] == "IBH14D0038") & (df["sl_no"] == 9) & (df["ch_stat"] == 0))
        ]
        df = df[
            ~(
                (df["hh_id"] == "IBH14D0038")
                & (df["sl_no"] == 10)
                & (df["ch_stat"] == 0)
            )
        ]
        df = df[
            ~(
                (df["hh_id"] == "IBH14D0038")
                & (df["sl_no"] == 11)
                & (df["ch_stat"] == 0)
            )
        ]

        # IJH14A0030
        df = df[
            ~((df["hh_id"] == "IJH14A0030") & (df["sl_no"] == 1) & (df["ch_stat"] == 3))
        ]

        # IJH14A0054
        df = df[
            ~((df["hh_id"] == "IJH14A0054") & (df["sl_no"] == 2) & (df["ch_stat"] == 3))
        ]

        # IOR13C0047
        df = df[
            ~((df["hh_id"] == "IOR13C0047") & (df["sl_no"] == 3) & (df["ch_stat"] == 1))
        ]

        # IOR13D0055
        df = df[
            ~((df["hh_id"] == "IOR13D0055") & (df["sl_no"] == 8) & (df["ch_stat"] == 4))
        ]

        # checking duplicates
        check_duplicates(
            df=df,
            index_cols=[
                "hh_id",
                "sl_no",
            ],
            master_check=False,
            write_file=True,
        )

        ###############################################################################################################
        # there was one entry in hh IGJ13B0048 where a sl_no id was empty. Replacing it with the next number in sequence
        cond = df["sl_no"].str.isdigit() == False
        df["sl_no"] = np.where(
            cond, 8, df["sl_no"]
        )  # for some reason sl_no is object but behave like an integer. But if to_float touches it, it will be plagued by NaN

        df["sl_no"] = df["sl_no"].astype(str)
        # print(df["sl_no"].unique())
        # print(df["sl_no"].nunique())
        # print(df["sl_no"].value_counts(dropna=False))

        # exporting long dataframe
        long_frame(tag=tag, df=df)

        # converting categorical columns to dummies
        string_cols = [
            "mari_stat",
            "edu_level",
            "yrs_edu",
            "rea_stop_edu",
            "main_occp",
            "subs_occp",
            "deg_ab",
            "liv_wf_os",
            "freq_visits",
        ]

        # removing vars which need not added to widened data. All vars-widening attempt lead to memory error at 20GB.
        df.drop(
            ["marriage_yr", "os_place", "yr_edu_ter", "ch_stat"],
            axis=1,
            inplace=True,
        )

        cols = [col for col in df.columns if col not in ["hh_id_panel", "sur_yr"]]
        cols = [col for col in cols if col in string_cols]
        df = pd.get_dummies(data=df, columns=cols, dtype=float)

        df = to_float(df=df, cols=["sl_no"])
        # print(df["sl_no"].unique())
        # print(df["sl_no"].nunique())
        # print(df["sl_no"].value_counts(dropna=False))

        df = widen_frame(df=df, index_cols=["hh_id", "sl_no"])

        print(df)

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
