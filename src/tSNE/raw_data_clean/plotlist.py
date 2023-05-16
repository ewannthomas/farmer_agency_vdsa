from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
import pandas as pd
import numpy as np
import json


def plotlist():
    """
    This function specifically cleans the Plotlist.xlsx file in each year under the plotlist questionnaire.
    """

    tag = "Plotlist"

    raw_path, interim_path, processed_path, external_path = dir_values()

    interim_file = interim_path.joinpath(f"{tag}.csv")

    if not interim_file.exists():
        east_cols = {
            "vdsid": "hh_id_old",
            "plot_code_": "plot_code",
            "plot_name_": "plot_name",
        }

        sat_cols = {"vds_id": "hh_id_old"}

        # unncecessary cols to be removed
        remove_cols = ["crop_6", "vdsid_hhid", "remarks"]

        df = data_wrangler(
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
        )

        # merging the plot ID and house number to make unique HH ID

        df["hh_no"] = df["hh_no"].fillna(0).astype(int)

        conds = [
            (df["hh_id_old"].isna()) & (df["hh_no"] < 10),
            (df["hh_id_old"].isna()) & (df["hh_no"] < 100) & (df["hh_no"] >= 10),
            (df["hh_id_old"].isna()) & (df["hh_no"] < 1000) & (df["hh_no"] >= 100),
            (df["hh_id_old"].isna()) & (df["hh_no"] < 10000) & (df["hh_no"] >= 1000),
        ]

        opts = [
            df["pl_id"] + "000" + df["hh_no"].round(0).astype(str),
            df["pl_id"] + "00" + df["hh_no"].round(0).astype(str),
            df["pl_id"] + "0" + df["hh_no"].round(0).astype(str),
            df["pl_id"] + df["hh_no"].round(0).astype(str),
        ]

        df["hh_id"] = np.select(conds, opts, default=df["hh_id_old"])

        # replacing 2014 sat india unique HH ID with plot iD becuase it's already corect.

        conds = [(df["sur_yr"] == "2014") & (df["hh_id_old"].isna())]

        opts = [df["pl_id"].astype(str)]

        df["hh_id"] = np.select(conds, opts, default=df["hh_id"])

        df.drop(["pl_id", "hh_no", "hh_id_old"], axis=1, inplace=True)

        # cleaning ownership status
        conds = [
            df["ow_stat"] == "OW",
            df["ow_stat"] == "SI",
            df["ow_stat"] == "LI",
            df["ow_stat"] == "MI",
            df["ow_stat"] == "SO",
            df["ow_stat"] == "LO",
            df["ow_stat"] == "MO",
        ]

        opts = [
            "Own land",
            "Leased-in on crop share",
            "Leased-in on fixed rent",
            "Mortgaged-in",
            "Leased-out on crop share",
            "Leased-out on fixed rent",
            "Mortgaged-out",
        ]
        df["ow_stat"] = np.select(conds, opts, default=df["ow_stat"])

        # cleaning season
        df["season"] = df["season"].str.strip().str.lower()
        conds = [
            df["season"].isin(["perennial", "perenial", "pereminal"]),
            df["season"].isin(["annaul", "annual"]),
            df["season"] == "kharif",
            df["season"] == "rabi",
            df["season"] == "summer",
        ]

        opts = [
            "Perennial",
            "Annual",
            "Rainy (Kharif)",
            "Post rainy (Rabi)",
            "Summer",
        ]
        df["season"] = np.select(conds, opts, default=df["season"])

        # cleaning numeric values
        df = to_float(
            df=df,
            cols=["plot_area", "crop_area", "irri_area", "rent_rec_paid"],
            error_action="raise",
        )

        df.rename(
            columns={
                "ow_stat": "ownership_status_plotlist",
                "rent_rec_paid": "plot_rent_received_paid",
            },
            inplace=True,
        )

        # cleaning plotcode and subplot code
        for col in ["plot_code", "sub_plot_code"]:
            # print(df[col].isna().value_counts())
            df[col] = df[col].str.strip()
            # print(df[col].isna().value_counts())

        ##CLEANING DUPLICATES ##########################################

        # cleaning duplicates is more complicated here. So we are going to manually pull it together.
        df.drop_duplicates(
            inplace=True
        )  # have manually checked these values. will remove around 43 obs which are exact replica of another.

        # cleaning duplicates for sub plots where plot rent is missing
        # Create a list of tuples containing the reference values for matching
        ref_values = [
            ("I", np.nan, "IBH12B0047"),
            ("D", "D", "IBH14A0031"),
            ("E", "E", "IBH14A0031"),
            ("E", "E", "IBH14A0033"),
            ("H", "H", "IBH14A0033"),
            ("G", "G", "IBH14A0033"),
            ("D", "D", "IBH14A0034"),
            ("E", "E", "IBH14A0034"),
            ("E", "E", "IBH14A0040"),
            ("I", "I", "IBH14A0040"),
            ("H", "H", "IBH14A0044"),
            ("C", "C", "IBH14A0047"),
            ("G", "G", "IBH14A0050"),
            ("J", "J", "IBH14A0052"),
            ("K", "K", "IBH14A0052"),
            ("G", "G", "IBH14A0054"),
            ("Q", "Q", "IBH14A0055"),
            ("R", "R", "IBH14A0055"),
            ("S", "S", "IBH14A0055"),
            ("J", "J", "IBH14A0057"),
            ("H", "H", "IBH14A0080"),
            ("I", "I", "IBH14A0080"),
            ("C", "C", "IBH14C0041"),
        ]

        # Create a new column "dups" and set its default value to False
        df["dups"] = False

        # Loop through each row in the DataFrame
        for i, row in df.iterrows():
            # Check if the household with plot code and subplot code matches any of the reference values
            if (row["plot_code"], row["sub_plot_code"], row["hh_id"]) in ref_values:
                # If it does, check if the "Plot_rent_received_paid" value is NaN
                if pd.isna(row["plot_rent_received_paid"]):
                    # If it is, mark the "dups" column as True
                    df.at[i, "dups"] = True

        df = df[df["dups"] == False]
        df.drop("dups", axis=1, inplace=True)

        # Removing specific household rows based on manual inspection.
        # IBH12A0033
        df = df[
            ~(
                (df["hh_id"] == "IBH12A0033")
                & (df["plot_code"] == "H")
                & (df["irri_area"].isna())
            )
        ]

        df = df[
            ~(
                (df["hh_id"] == "IBH12A0034")
                & (df["plot_code"] == "E")
                & (df["crop_area"].isna())
            )
        ]
        df = df[
            ~(
                (df["hh_id"] == "IGJ13B0046")
                & (df["plot_code"] == "C")
                & (df["irri_area"] == 0)
            )
        ]

        df = df[
            ~(
                (df["hh_id"] == "IJH11D0044")
                & (df["plot_code"] == "L")
                & (df["crop_area"].isna())
            )
        ]

        # Reassigning plot rent value based on sum of duplicates for hh's 57 and 56
        conds = [
            (df["hh_id"] == "IAP10D0057") & (df["sub_plot_code"] == "FA"),
            (df["hh_id"] == "IBH14D0056") & (df["sub_plot_code"] == "H"),
        ]

        opts = [2334, 5250]
        df["plot_rent_received_paid"] = np.select(
            conds, opts, default=df["plot_rent_received_paid"]
        )

        # Reassigning plot rent value based on sum of duplicates for hh's 40
        conds = [
            (df["hh_id"] == "IBH10C0040") & (df["plot_code"] == "A"),
        ]

        opts = [0.18]
        df["crop_area"] = np.select(conds, opts, default=df["crop_area"])

        # cleaning duplicates is more complicated here. So we are going to manually pull it together.
        df.drop_duplicates(
            subset=[
                "hh_id",
                "plot_name",
                "plot_code",
                "sub_plot_code",
                "ownership_status_plotlist",
                "season",
                "crop_1",
                "crop_2",
                "crop_3",
                "crop_4",
                "crop_5",
            ],
            inplace=True,
        )  # have manually checked these values. will remove around 43 obs which are exact replica of another.

        ############################################################################################

        # cleaning crop_5 column off digits
        df["plot_rent_received_paid"] = np.where(
            df["crop_5"].str.isdigit(), df["crop_5"], df["plot_rent_received_paid"]
        )

        df["crop_5"] = np.where(df["crop_5"].str.isdigit(), np.NaN, df["crop_5"])

        # importing the json mapper of crop names
        crop_name_map = "./src/tSNE/raw_data_clean/crop_names_map.json"
        with open(crop_name_map, "r") as in_file:
            crop_map = dict(json.load(in_file))

        crop_type_map = "./src/tSNE/raw_data_clean/crop_type_map.json"
        with open(crop_type_map, "r") as in_file:
            crop_map_type = dict(json.load(in_file))

        crop_names_list = []
        for crop in ["crop_1", "crop_2", "crop_3", "crop_4", "crop_5"]:
            df[crop] = df[crop].str.lower().str.strip()
            df[crop] = df[crop].replace(crop_map)
            df[str(crop + "_" + "type")] = df[crop].replace(crop_map_type)
            crop_names_list.extend(df[crop].unique())

        # print(pd.Series(crop_names_list).unique())
        # print(pd.Series(crop_names_list).nunique())

        ##CLEANING DUPLICATES ##########################################
        # cleaning duplicates post crop type imposition.
        df.drop_duplicates(
            inplace=True
        )  # have manually checked these values. will remove around 12 obs which are exact replica of another.

        # Removing specific household rows based on manual inspection.
        # IBH12C0059
        df = df[
            ~(
                (df["hh_id"] == "IBH12C0059")
                & (df["plot_code"] == "F")
                & (df["irri_area"] == 0.1)
            )
        ]

        # IBH14B0036
        df = df[
            ~(
                (df["hh_id"] == "IBH14B0036")
                & (df["plot_code"] == "E")
                & (df["irri_area"].isna())
            )
        ]

        # IBH14B0059
        df = df[
            ~(
                (df["hh_id"] == "IBH14B0059")
                & (df["plot_code"] == "E")
                & (df["irri_area"].isna())
            )
        ]

        # IBH14B0043
        df = df[
            ~(
                (df["hh_id"] == "IBH14B0043")
                & (df["plot_code"] == "D")
                & (df["irri_area"].isna())
            )
        ]
        # IBH14B0045
        df = df[
            ~(
                (df["hh_id"] == "IBH14B0045")
                & (df["plot_code"] == "D")
                & (df["irri_area"].isna())
            )
        ]
        # IBH14C0054
        df = df[
            ~(
                (df["hh_id"] == "IBH14C0054")
                & (df["plot_code"] == "I")
                & (df["irri_area"] == 0.06)
            )
        ]
        # IOR13B0203
        df = df[
            ~(
                (df["hh_id"] == "IOR13B0203")
                & (df["plot_code"] == "A")
                & (df["crop_area"] == 1)
            )
        ]
        # IBH14C0038
        df = df[
            ~(
                (df["hh_id"] == "IBH14C0038")
                & (df["plot_code"] == "F")
                & (df["crop_1"] == "Other")
            )
        ]

        df = df[
            ~(
                (df["hh_id"] == "IBH14C0034")
                & (df["plot_code"] == "F")
                & (df["irri_area"] == 0.05)
            )
        ]

        df = df[
            ~(
                (df["hh_id"] == "IBH14C0039")
                & (df["plot_code"] == "F")
                & (df["irri_area"] == 0.1)
            )
        ]

        df = df[
            ~(
                (df["hh_id"] == "IBH14C0043")
                & (df["plot_code"] == "A")
                & (df["irri_area"] == 0.35)
            )
        ]

        df = df[
            ~(
                (df["hh_id"] == "IBH14C0047")
                & (df["plot_code"] == "H")
                & (df["irri_area"] == 0.12)
            )
        ]

        df = df[
            ~(
                (df["hh_id"] == "IBH14C0058")
                & (df["plot_code"] == "K")
                & (df["irri_area"] == 0.2)
            )
        ]

        df = df[
            ~(
                (df["hh_id"] == "IBH14C0200")
                & (df["plot_code"] == "G")
                & (df["irri_area"] == 0.15)
            )
        ]

        df = df[
            ~(
                (df["hh_id"] == "IBH14C0201")
                & (df["plot_code"] == "C")
                & (df["irri_area"] == 0.03)
            )
        ]

        df = df[
            ~(
                (df["hh_id"] == "IBH14C0202")
                & (df["plot_code"] == "C")
                & (df["irri_area"] == 0.04)
            )
        ]
        df = df.drop_duplicates(
            subset=[
                "hh_id",
                "plot_name",
                "plot_code",
                "sub_plot_code",
                "ownership_status_plotlist",
                "season",
                "crop_1_type",
                "crop_2_type",
                "crop_3_type",
                "crop_4_type",
                "crop_5_type",
            ]
        )
        ###########################################################################################

        index_cols = [
            "hh_id",
            "plot_code",
            "sub_plot_code",
            "ownership_status_plotlist",
            "season",
            "crop_1_type",
            "crop_2_type",
            "crop_3_type",
            "crop_4_type",
            "crop_5_type",
        ]

        # widening the data based on plot code

        # before widening the columns, we are removing plot_name by groupby agg across all other string vals

        df = (
            df.groupby(index_cols)
            .agg(
                {
                    "plot_area": "sum",
                    "crop_area": "sum",
                    "irri_area": "sum",
                }
            )
            .reset_index()
        )

        # checking for duplicates
        check_duplicates(
            df,
            index_cols=index_cols,
            # master_check=True,
            write_file=True,
        )

        df["plot_code"].dropna(
            inplace=True
        )  # removing nan values in plot code. These values are all null across columns. Manually verified.

        df = widen_frame(
            df=df,
            index_cols=index_cols,
            wide_cols=["plot_area", "crop_area", "irri_area"],
            agg_dict={
                "plot_area": "sum",
                "crop_area": "sum",
                "irri_area": "sum",
            },
        )

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
