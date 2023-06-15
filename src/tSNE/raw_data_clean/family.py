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

        # checking duplicates
        check_duplicates(
            df=df,
            index_cols=["hh_id", "sl_no", "ch_stat"],
            master_check=False,
            write_file=True,
        )

        # converting index columns to strings because serial numbers are floats and will give trouble in multi-index coliumn renaming
        df["sl_no"] = df["sl_no"].astype(str)
        df["ch_stat"] = df["ch_stat"].astype(str)

        df.rename(columns={"gender": "female"}, inplace=True)

        # For some reason remove_cols is not catching this column. So initiating a specific removal.
        df.drop("relation_ot", axis=1, inplace=True)

        df = to_float(df=df, cols=["relation"])

        # exporting long dataframe
        long_frame(tag=tag, df=df)

        df = widen_frame(df=df, index_cols=["hh_id", "sl_no", "ch_stat"])

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
