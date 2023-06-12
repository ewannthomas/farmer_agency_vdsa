from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
from utils.long_frame import long_frame
import pandas as pd
import numpy as np
import re


def coping_mech():
    """
    This function is specifically cleans the Coping_Mech.xlsx file in each year under the GES questionnaire.
    """

    tag = "Coping_Mech"

    raw_path, interim_path, processed_path, external_path = dir_values()

    interim_file = interim_path.joinpath(f"{tag}.csv")

    if not interim_file.exists():
        east_cols = {"vdsid": "hh_id"}

        sat_cols = {
            "vds_id": "hh_id",
            "affect": "affected",
            "ad_co_me": "ado_co_me",
            "inc_loss_rs": "loss_rs",
            "prct_inc_loss": "loss_prct_inc",
            "inc_loss_prct": "loss_prct_inc",
            "co_me_m1": "co_mech_m1",
            "co_me_m2": "co_mech_m2",
            "co_me_m3": "co_mech_m3",
            "co_me_m_ot": "co_mech_m_ot",
            "co_me_f1": "co_mech_f1",
            "co_me_f2": "co_mech_f2",
            "co_me_f3": "co_mech_f3",
            "co_me_f_ot": "co_mech_f_ot",
        }

        # unncecessary cols to be removed
        remove_cols = []

        df = data_wrangler(
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
        )

        # cleaning problem column
        df["problem"] = df["problem"].str.strip().str.lower()

        anthro_conds = [
            "death of earning member",
            "loss due to theft/dacoit/fire",
            "litigation of property",
            "dengue fever",
            "conflicts",
            "minimum support price less",
            "court expenditure",
            "health problems",
            "loss in farming due to accident/sickness",
            "loss due to fire",
            "others (permanent illness)",
            "loss in farming due to accident/s",
            "loss due to accident",
            "loss in farming due accident/s",
            "physical injury",
        ]

        bio_conds = [
            "death of livestock",
            "wild boars",
            "pests and diseases",
            "pests & disease",
            "seed failed",
            "flood and pest diseases",
            "others (elephant attack)",
            "crop loss by elephant",
            "loss by wild boars",
            "loss in waterlemon crop",
            "crop mess by elephant",
            "loss in business",
        ]

        clim_fd = [
            "drought",
            "flood/cyclone",
        ]

        clim_oth = [
            "heavy rainfall",
            "heavy rainafall",
            "heavy rain and frost",
            "heavy rain",
            "frost",
        ]

        others = ["others", "others(specify) healthy"]

        conds = [
            (df["problem"].isin(anthro_conds)),
            (df["problem"].isin(bio_conds)),
            (df["problem"].isin(clim_fd)),
            (df["problem"].isin(clim_oth)),
            (df["problem"].isin(others)),
        ]
        options = [
            "Anthropogenic",
            "Biophysical",
            "Climate Flood Drought",
            "Climate Others",
            "Others",
        ]

        df["problem"] = np.select(conds, options, default=df["problem"])

        # cleaning affected and ado_co_me columns

        df["ado_co_me"] = df["ado_co_me"].str.strip()

        adopt_map = {
            "Yes": "adopted",
            "Y": "adopted",
            "No": "not_adopted",
            "N": "not_adopted",
        }

        df["ado_co_me"] = df["ado_co_me"].replace(adopt_map)

        # There are 3 households with misisng ado_co_me. replacing the nan with "adopted"
        conds = [
            (
                df["hh_id"].isin(["IOR14D0001", "IOR14D0009", "IOR14D0034"])
                & df["ado_co_me"].isna()
            )
        ]
        opts = ["adopted"]
        df["ado_co_me"] = np.select(conds, opts, default=df["ado_co_me"])

        # print(df["ado_co_me"].unique())

        # cleaning other coping mechanism string values
        # df['co_mech_m_ot']=df['co_mech_m_ot'].str.strip()
        # print(df['co_mech_m_ot'].unique())

        # strangely, this dataset holds sur_yr as an object but contains values as strings and numbers in it. I checked and I'm mind blown.
        # the below process works with np.where fucntion because sur_yr column holds strings and numbers together. Its a boon indisguise of a curse.

        # cleaning 2010 values for Bihar, Jharkhand and Orissa
        df["hh_id"] = np.where(
            df["sur_yr"] == 2010,
            df["hh_id"].str.replace("IBH11", "IBH10"),
            df["hh_id"],
        )
        df["hh_id"] = np.where(
            df["sur_yr"] == 2010,
            df["hh_id"].str.replace("IJH11", "IJH10"),
            df["hh_id"],
        )
        df["hh_id"] = np.where(
            df["sur_yr"] == 2010,
            df["hh_id"].str.replace("IOR11", "IOR10"),
            df["hh_id"],
        )

        # cleaning 2011 values for Bihar, Jharkhand and Orissa
        df["hh_id"] = np.where(
            df["sur_yr"] == 2011,
            df["hh_id"].str.replace("IBH12", "IBH11"),
            df["hh_id"],
        )
        df["hh_id"] = np.where(
            df["sur_yr"] == 2011,
            df["hh_id"].str.replace("IJH12", "IJH11"),
            df["hh_id"],
        )
        df["hh_id"] = np.where(
            df["sur_yr"] == 2011,
            df["hh_id"].str.replace("IOR12", "IOR11"),
            df["hh_id"],
        )

        # print(df[df['sur_yr']==2010]['hh_id'].unique())
        # print(df[df['sur_yr']==2011]['hh_id'].unique())

        # print(df['sur_yr'].unique())

        # sending the df with clean households through the float maker function to correct all numeric cols
        cols = [
            "loss_prct_inc",
            "co_mech_m1",
            "co_mech_m2",
            "co_mech_m3",
            "co_mech_f2",
            "co_mech_f3",
            "loss_rs",
            "co_mech_f1",
        ]

        df = to_float(df=df, cols=cols)

        # mapping coping mechanisms to categorical values
        cop_mech_map = {
            1: "Selling land",
            2: "Selling domestic animals/birds",
            3: "Selling trees",
            4: "Mortgaging land",
            5: "Mortgaging jewellery & other property",
            6: "Own savings",
            7: "Help from relatives",
            8: "Cash loans",
            9: "Kind loans",
            10: "Govt. Aid/relief",
            11: "Insurance",
            12: "Others",
        }

        cols = [
            "co_mech_m1",
            "co_mech_m2",
            "co_mech_m3",
            "co_mech_f2",
            "co_mech_f3",
            "co_mech_f1",
        ]

        for col in cols:
            df[col] = df[col].replace(cop_mech_map).str.lower()
            # print(df[col].unique())

        # renaming cols
        df.rename(
            columns={
                "loss_prct_inc": "percent_of_income_lost",
                "loss_rs": "losses_in_rupees",
            },
            inplace=True,
        )

        # removing other cop mechs and widening the data
        df.drop(["co_mech_m_ot", "co_mech_f_ot"], axis=1, inplace=True)

        # removing duplicates
        df.drop_duplicates(inplace=True)  # manually verified. removes 26 observations

        ####### DF_COP subset for coping mechanism

        # for the sake of widening we are recreating more cop_mech columns. We faced duplicates when the same household faced two different calamitoes belonging to the same category.
        # adding duplicate-look alike cop_mechs as mech 4, 5, 6 etc
        # so we rae creating a new subset with coping mechanisms and a subset with aggregated loss percentages and losses for each category of calamity
        df_cop = df.melt(
            id_vars=["hh_id", "sur_yr", "ado_co_me", "problem"],
            value_vars=cols,
            var_name="cop",
            value_name="cop_value",
        )

        df_cop["cop"] = df_cop["cop"].str.strip().str.lower()

        # male regex catch
        # male_catch = re.compile("cop_mech_m.\d")
        # female_catch = re.compile("cop_mech_f.\d")

        df_cop["gender"] = np.where(
            df_cop["cop"].str.contains("co_mech_m"),
            "m",
            np.where(df_cop["cop"].str.contains("co_mech_f"), "f", ""),
        )

        df_cop = df_cop.sort_values(by=["hh_id", "ado_co_me", "problem", "cop"])

        df_cop["count"] = (
            df_cop.groupby(
                ["hh_id", "sur_yr", "ado_co_me", "problem", "gender"],
            )["hh_id"].cumcount()
            # .reset_index(drop=True)
        ) + 1  # we add a value 1 to cumulative count because cummulative count starts with 0, and we need it to start from 1

        df_cop["count"] = df_cop["count"].astype(str).str.replace(".0", "")
        df_cop["cop_mech"] = (
            "cop_mech_" + df_cop["gender"] + df_cop["count"]
        )  # here we create a new

        df_cop.drop(["cop", "gender", "count"], axis=1, inplace=True)

        # pivoting the cop_mech column

        df_cop = df_cop.pivot(
            index=["hh_id", "sur_yr", "ado_co_me", "problem"],
            columns="cop_mech",
            values="cop_value",
        ).reset_index()

        # dropping columns with all nan values
        df_cop.dropna(axis=1, how="all", inplace=True)

        check_duplicates(
            df=df_cop,
            index_cols=["hh_id", "ado_co_me", "problem", "cop_mech"],
            master_check=False,
            write_file=True,
        )

        ####### DF_LOSS subset for losses

        df_loss = (
            df.groupby(["hh_id", "sur_yr", "ado_co_me", "problem"])
            .agg({"percent_of_income_lost": "sum", "losses_in_rupees": "sum"})
            .reset_index()
        )

        check_duplicates(
            df=df_loss,
            index_cols=["hh_id", "ado_co_me", "problem"],
            master_check=False,
            write_file=True,
        )

        # merging to arrive at the original data
        df = pd.merge(
            left=df_cop,
            right=df_loss,
            on=["hh_id", "sur_yr", "ado_co_me", "problem"],
            how="outer",
            validate="1:1",
            indicator=False,
        )  # manually verified,  100% match

        # print(df)
        # print(df["_merge"].value_counts())

        # exporting long dataframe
        long_frame(tag=tag, df=df)

        df = widen_frame(df=df, index_cols=["hh_id", "ado_co_me", "problem"])

        # print(df)

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
