import pandas as pd
from pathlib import Path
import numpy as np
import json


class VdsaMicrotSNE:

    """
    This class covers functions written to clean VDSA Micro Data for the Farmers Response and Erratic Rainfall under BIPP. This class is dedicated towards cleaning data for running the t-SNE visualizations.
    """

    def __init__(self):
        """
        This function sets in place all the dependencies and defines the path structures used in any further functions.
        """

        dir_path = Path.cwd()
        self.raw_path = dir_path.joinpath("data/raw")
        self.interim_path = dir_path.joinpath("data/interim/tsne")
        self.processed_path = dir_path.joinpath("data/processed")
        self.external_path = dir_path.joinpath("data/external")

        # creating the data directories
        if not self.interim_path.exists():
            self.interim_path.mkdir(parents=True)

        if not self.processed_path.exists():
            self.processed_path.mkdir(parents=True)

        if not self.processed_path.exists():
            self.processed_path.mkdir(parents=True)

    def path_values_create(self, region_folder_position: int):
        """
        This function creates a list of iteratble windows paths for the raw data depending on its block position in the VDSA Micro questionnaire.
        Parameters:
        self: Inherits all the path structures defined in __init__.
        region_folder_position: An integer mentioning the folder position of the region folder (eastindia or satindia) in the windows path of the raw data directory. Teh count starts from zero by adhering to the python list convention.
                                Example: 'C:\Work ISB\projects\frer\data\raw\eastindia\2012' has region_folder_poition of 6 (starting from 0). Similarly for linux systems its 8.

        """

        tag_list = [
            "Coping_Mech",
            "Proactive_measure",
            "Drought_Assistance",
            "Gen_info",
            "Fin_assets_liabilities",
            "Plotlist",
            "Family_comp",
            "Landholding",
            "Livestock_inv",
            "Farm_Equipment",
            "Consumer_durables",
            "Stock_inv",
            "Gend_decision_making",
            "Gend_crop_cult",
            "Info_ranking",
            "Reliability_ranking",
            "Govt_assist",
            "Crop_info_op",
            "Cult_ip",
            "Food_item",  # food, non-food and exp_foof_non_food are tags connected with f and nf expenses. They are split into 3 and called seperately for the ease of operation.
            "Non_food_item",
            "Exp_food_non_food",
            "Fin_Trans",
            "Loans",
            "Prod_Sold",
            "Sale_pur",
            "Govt_dev_progs_benefits",
            "Building",
        ]

        self.raw_path_list = []  # creating a lsit for path and dependency dictionary
        self.interim_path_list = []

        for tag in tag_list:
            interim_appended_file_path = self.interim_path.joinpath(f"{tag}.csv")

            if not interim_appended_file_path.exists():
                # print(f"Appending {tag} files for all years")

                if (
                    tag == "Gen_info"
                ):  # this condition will ensure that we collect only household general information from the ges folder
                    patterns = [
                        f"*/*/ges/*.{tag}.xlsx",
                        f"*/*/ges/{tag}.xlsx",
                    ]  # we create multiple patterns to capture different file naming conventins between eastindia and satindia folders

                elif tag == "Fin_assets_liabilities":
                    patterns = ["*/*/*/*.Debt_credit.xlsx", f"*/*/*/{tag}.xlsx"]

                elif tag == "Plotlist":
                    patterns = [
                        f"*/*/plotlist/Plot_List.xlsx",
                        f"*/*/plotlist/plotlist.xlsx",
                        f"*/*/plotlist/plotlist.xls",
                        f"*/*/plotlist/Plot_list.xls",
                    ]

                elif tag == "Family_comp":
                    patterns = [f"*/*/ges/*.House*.xlsx", f"*/*/ges/{tag}.xlsx"]

                elif tag == "Landholding":
                    patterns = [f"*/*/ges/*.{tag}*.xlsx", f"*/*/ges/{tag}*.xlsx"]

                elif tag == "Consumer_durables":
                    patterns = [f"*/*/ges/*.Con_*.xlsx", f"*/*/ges/Con_*.xlsx"]

                elif tag == "Reliability_ranking":
                    patterns = [f"*/*/ges/*.How_reliable*.xlsx", f"*/*/ges/*{tag}.xlsx"]

                elif tag == "Proactive_measure":
                    patterns = [f"*/*/ges/*.Proact*.xlsx", f"*/*/ges/*{tag}.xlsx"]

                elif tag == "Govt_assist":
                    patterns = [f"*/*/ges/*.{tag}*.xlsx"]

                elif tag == "Crop_info_op":
                    patterns = [
                        f"*/*/*/*.{tag}.xlsx",
                        f"*/*/*/{tag}.xlsx",
                        f"*/*/cultivation/Crop_info_2011.xlsx",
                        f"*/*/cultivation/Cult_output.xlsx",
                    ]

                elif tag == "Cult_ip":
                    patterns = [f"*/*/*/*.Cult_i*.xlsx", f"*/*/*/Cult_i*.xlsx"]

                elif tag == "Food_item":
                    patterns = [f"*/*/*/*.{tag}*.xlsx", f"*/*/*/{tag}*.xlsx"]

                elif tag == "Non_food_item":
                    patterns = [f"*/*/*/*.{tag}*.xlsx", f"*/*/*/{tag}*.xlsx"]

                elif tag == "Exp_food_non_food":
                    patterns = [f"*/*/*/*.{tag}*.xlsx", f"*/*/*/{tag}*.xlsx"]

                elif tag == "Fin_Trans":
                    patterns = [f"*/*/tran*/Fin_*.xlsx"]

                elif tag == "Govt_dev_progs_benefits":
                    patterns = [
                        f"*/*/*/govt_dev*.xlsx",
                        f"*/*/*/Ben_govt_*.xlsx",
                        f"*/2013/ges/gov*.xlsx",
                    ]

                elif tag == "Farm_Equipment":
                    patterns = [
                        f"*/*/*/*.{tag}.xlsx",
                        f"*/*/*/Farm_equpment.xlsx",
                        f"*/*/*/{tag}.xlsx",
                        "*/*/*/*.Farm_equipment.xlsx",
                    ]

                else:
                    patterns = [f"*/*/*/*.{tag}.xlsx", f"*/*/*/{tag}.xlsx"]

                for pat in patterns:
                    raw_file_paths = list(self.raw_path.glob(pat))

                    for file in raw_file_paths:
                        # print(file)
                        # if you are windows systems replace "/" by "\\" to get parent folders and region folder position will be 8
                        parent_region = str(file).split("/")[region_folder_position]
                        year = str(file).split("/")[(region_folder_position + 1)]

                        path_dict = {
                            "tag": tag,
                            "path": file,
                            "out_path": interim_appended_file_path,
                            "region": parent_region,
                            "year": year,
                        }

                        self.raw_path_list.append(path_dict)

            else:
                print(f"Files for {tag} exists.")
                path_dict = {"tag": tag, "interim_path": interim_appended_file_path}
                self.interim_path_list.append(path_dict)
                continue

    def to_float(self, df: pd.DataFrame, cols: list):
        """
        This function converts the specified columns which inherited their string character into floats.
        Parameters:
        self: Inherits all the self variables.
        df: A pandas dataframe which contains the columns to be converted to float
        cols: A list of columns which are objects and need to be converted to float
        """

        temp_file = self.interim_path.joinpath("temp.csv")

        df.to_csv(temp_file, index=False)

        df = pd.read_csv(temp_file)

        for col in cols:
            try:
                df[col] = df[col].str.rstrip()
                # .replace(" ", "a")
                # .str.replace("aa", '', regex=True)

            except AttributeError:
                continue

        df.to_csv(temp_file, index=False)

        df = pd.read_csv(temp_file)

        temp_file.unlink()

        return df

    def widen_frame(
        self,
        tag: str,
        df: function | pd.DataFrame,
        index_cols: list,
        wide_cols: list,
        agg_dict: dict,
    ):
        """
        This function converts the entire dataframe into a wider version of itself and writes it to the tSNE folder in the interim data directory. It conducts the Pandas Pivot fucntion to achieve the same, after ensuring the absence of duplicates in the dataframe.

        Parameters:
        self: Inherits all the self variables.

        tag: A string value enabling in identifying the exact location of the file to be wrangled using the path_values_create method defined under the VdsaMicrotSNE class.

        df: A pandas dataframe to be widened. The input can be a fucntion rendering the desired dataframe or a dataframe.

        index_cols: A list of column names which will be used as index of the dataframe to perform duplication check, groupby and widening.

        wide_cols: A list of column names which will be, strictly, converted to float and reduced to statisitcs mentioned in the agg_dict based on the index_cols groups.

        agg_dict: A dictionary which defines the summaryu statistic that should be created for each col in the wide_cols list while performing the groupby operation.
        """

        if not self.interim_path.joinpath(f"{tag}.csv").exists():
            # The first operation is ensure that no duplicates exist across all columns of the original dataset.
            df["dups"] = df.duplicated(keep=False)

    def data_wrangler(
        self,
        tag: str,
        rename_east: dict,
        rename_sat: dict,
        remove_cols: list,
        export_file: bool = True,
    ):
        """
        This function wrangles the data file supplied via path. It performs aset of predefined actions necessary for appending the various files spread across years.
        Parameters:
        self: Inherits all the path structures defined in __init__.

        tag: A string value enabling in identifying the exact location of the file to be wrangled using the path_values_create method defined under the VdsaMicrotSNE class.

        rename_east: A dictionary which will be used for renamimg anmd standardizing the column names in the files pertaining to East India.
                        Key: Old column name
                        Value: New column name

        rename_sat: A dictionary which will be used for renamimg anmd standardizing the column names in the files pertaining to Semi tropical arid (SAT) India.
                        Key: Old column name
                        Value: New column name

        remove_cols: A list of columns names which are to be removed from the file.

        export_file: (default:True) A boolean which determines whether the appended file is exported to the interim directory. It can be turned off if the appended file needs to be wrangled beyond the scope of this fucntion.
        """

        interim_appended_file_path = self.interim_path.joinpath(f"{tag}.csv")

        if not interim_appended_file_path.exists():
            # creating a subset of raw_path_list which isolates the path
            raw_paths_sublist = []
            for x in self.raw_path_list:
                if tag == x["tag"]:
                    raw_paths_sublist.append(x)

            # print(raw_paths_sublist)

            # initiating data wrangle
            raw_data_list = (
                []
            )  # defining an emplty list to hold the raw data before appending

            for file in raw_paths_sublist:
                print(file["path"].stem, file["region"], file["year"])

                # reading in the raw file
                df = pd.read_excel(file["path"])

                # cleaning of column names
                col_list = df.columns
                col_list = [x.lower().replace(" ", "_") for x in col_list]
                df.columns = col_list

                # removing unnecessary columns from the data
                col_list = [x for x in col_list if x not in remove_cols]
                df = df[col_list]

                # renaming the necessary columns. Names will be sourced fronm the function assigned for each tag
                if file["region"] == "eastindia":
                    df.rename(columns=rename_east, inplace=True)

                if file["region"] == "satindia":
                    df.rename(columns=rename_sat, inplace=True)

                if tag == "Building":
                    # adding region value to file
                    df.insert(0, "region", file["region"])

                if tag == "Gen_info":
                    df["sur_yr"] = file["year"]

                # adding year value in satindia file
                try:
                    if file["region"] == "satindia":
                        df.insert(0, "sur_yr", file["year"])
                except ValueError as ex:
                    print(
                        f"Error: Survey year already exists in {file['region']} {file['year']}"
                    )

                raw_data_list.append(df)

            df_appended = pd.concat(raw_data_list, axis=0)
            if export_file == True:
                # writing appended file
                df_appended.to_csv(f"{self.interim_path}/{tag}.csv", index=False)
            elif export_file == False:
                # assigning appended file to self if file is opted out from export
                self.appended_file = df_appended
        else:
            pass

    def gen_info_cleaner(self):
        """
        This function is specifically cleans the Gen_info.xlsx file in each year under the GES questionnaire.
        """

        tag = "Gen_info"

        east_cols = {"vdsid": "hh_id", "the_man_blo": "block"}

        sat_cols = {"vds_id": "hh_id", "teh_man_blo": "block"}

        # unncecessary cols to be removed
        remove_cols = [
            "dt_int",
            "dt_check",
            "sou_hh_no",
            "head_name",
            "son_wife_of",
            "lon_deg",
            "lon_min",
            "lon_sec",
            "lat_deg",
            "lat_min",
            "lat_sec",
            "altitude",
            "inv_name",
            "name_sup",
            "pre_hh_no",
            "old_hh_no",
            "vdsid_hhid",
            "cs_hh_no",
        ]

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=False,
        )

        def string_vals_clean():
            """
            This function cleans the string columns of the data in Gen Info file.
            """

            if not self.interim_path.joinpath(f"{tag}.csv").exists():
                df = pd.DataFrame(self.appended_file)

                # blanet processes for string cols
                col_list = df.columns

                selected_cols = [
                    "village",
                    "block",
                    "district",
                    "state",
                    "country",
                    "market_place",
                    "caste",
                    "sub_caste",
                    "religion",
                    "immi_to_vil",
                    "how_head_ot",
                    "reas_immi",
                ]

                special_cols = ["how_head_ot", "reas_immi"]

                for col in col_list:
                    if df[col].dtype == "object":
                        df[col] = df[col].str.strip()

                    if col in selected_cols:
                        df[col] = df[col].str.title().str.replace(" ", "_")

                temp_file_path = self.interim_path.joinpath("temp.csv")
                df.to_csv(temp_file_path, index=False)
                df = pd.read_csv(temp_file_path)

                temp_file_path.unlink()

                for col in special_cols:
                    df[col] = df[col].str.title().str.replace("_", " ")

                # cleaning religion column
                conds = [
                    df["religion"].isin(
                        ["Hindu", "Hindi", "Hindu24", "Obc", "Sarna", "Saran"]
                    ),
                    df["religion"].isin(
                        [
                            "Christian",
                            "Christion",
                            "Christan",
                            "Christain",
                            "Christians",
                            "1988",
                        ]
                    ),
                    df["religion"].isin(["Boudh", "Boudha"]),
                    df["religion"].isin(["Muslim"]),
                    df["religion"].isin(["Jain"]),
                ]

                options = ["Hinduism", "Christianity", "Buddhism", "Islam", "Jainism"]

                df["religion"] = np.select(conds, options, default=df["religion"])

                # cleaning caste groups column
                df["caste_group"] = df["caste_group"].str.upper()

                conds = [
                    df["caste_group"].isin(["EBC", "SBC"]),
                    df["caste_group"].isin(["BC"]),
                ]

                options = ["SBC/SEBC/EBC", "OBC"]

                df["caste_group"] = np.select(conds, options, default=df["caste_group"])

                df.to_csv(f"{self.interim_path}/{tag}.csv", index=False)

        string_vals_clean()

    def coping_mech_cleaner(self):
        """
        This function is specifically cleans the Coping_Mech.xlsx file in each year under the GES questionnaire.
        """

        tag = "Coping_Mech"

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

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=False,
        )

        def cat_clean():
            """
            This function cleans the categories of various disasters or problems, and other string variables in the coping mech data.
            """

            if not self.interim_path.joinpath(f"{tag}.csv").exists():
                df = pd.DataFrame(self.appended_file)

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

                for col in ["affected", "ado_co_me"]:
                    df[col] = df[col].str.strip()

                    conds = [df[col] == "Y", df[col] == "N"]

                    opts = ["Yes", "No"]

                    df[col] = np.select(conds, opts, default=df[col])

                # cleaning other coping mechanism string values
                # df['co_mech_m_ot']=df['co_mech_m_ot'].str.strip()
                # print(df['co_mech_m_ot'].unique())

                return df

        def hh_id_clean():
            """
            This function is designed specificaaly to deal with the cases of states of Bihar, Jharkhand and Orissa for the years 2010 and 2011. For these years, these states have wrong year indicators int he hh_id.
            Example: For year 2010 in Bihar, the id for household A0006 is IBH11A0006 instead of IBH10A0006.
            """

            if not self.interim_path.joinpath(f"{tag}.csv").exists():
                df = pd.DataFrame(cat_clean())

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

                return df

        def clean_floats():
            """
            This function corrects the numeric variables by stripping off the special characters and empty spaces.
            """

            if not self.interim_path.joinpath(f"{tag}.csv").exists():
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

                df = pd.DataFrame(
                    VdsaMicrotSNE.to_float(self, df=hh_id_clean(), cols=cols)
                )

                # removing other cop mechs and widening the data
                df.drop(["co_mech_m_ot", "co_mech_f_ot"], axis=1, inplace=True)

                df = df.pivot(["sur_yr", "hh_id"], columns="problem").reset_index()

                print(df)

                df.to_csv(f"{self.interim_path}/{tag}.csv", index=False)

        clean_floats()

    def assests_liabs(self):
        """
        This function is specifically cleans the Fin_assets_liabilities.xlsx file in each year under the GES questionnaire.
        """

        tag = "Fin_assets_liabilities"

        east_cols = {"vdsid": "hh_id"}

        sat_cols = {
            "vds_id": "hh_id",
            "category_dr_cr": "category",
            "agency_source": "source",
            "who_used": "who_spent",
            "who_dr_cr": "with_whom",
        }

        # unncecessary cols to be removed
        remove_cols = [
            "remarks",
            "remarks_g",
            "who_dr_cr",
            "with_whom",
            "who_spent",
            "who_used",
            "purpose_ot",
        ]

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=False,
        )

        def widen_vals():
            """
            This function aggregates the assets and liabilities of households to 3 categories in the category column.
            """

            if not self.interim_path.joinpath(f"{tag}.csv").exists():
                df = pd.DataFrame(self.appended_file)

                df["category"] = df["category"].str.strip().str.lower()

                # cleaning inteerest and duration columns which are strings and has a character "DK" in it.
                df = VdsaMicrotSNE.to_float(self, df=df, cols=["interest", "duration"])
                df["interest"] = df["interest"].str.strip().str.replace("DK", "")
                df["duration"] = df["duration"].str.strip().str.replace("DK", "")

                df = VdsaMicrotSNE.to_float(
                    self, df=df, cols=["interest", "duration", "purpose"]
                )
                df["interest"] = df["interest"].astype(float)
                df["duration"] = df["duration"].astype(float)
                df["purpose"] = df["purpose"].astype(str).str.replace(".0", "")

                # cleaning source column categories
                df["source"] = (
                    df["source"].str.strip().str.lower().str.replace(" ", "_")
                )

                conds = [
                    # co-operative banks
                    df["source"].isin(
                        [
                            "others_(society_bank)",
                            "patliputra_bank",
                            "lokmangal_bank",
                            "mohol_nagari_bank",
                            "co-operative_banks",
                            "co-operatives",
                            "co-operative_bank",
                            "association",
                            "b_s_s_sangh",
                            "sangh",
                            "society",
                            "malikarjun_soshai_sang",
                            "mallikarjun_s_sanga",
                        ]
                    ),
                    # commerical banks
                    df["source"].isin(
                        [
                            "other_(commercial_banks)",
                            "other_(sbi)",
                            "commercial_bank-fd",
                            "private_bank(rd)",
                            "private_bank-rd",
                            "sbi_housing_loan",
                            "vijay_shree_bank",
                            "vijaya_shree_bank",
                            "syndicate_bank_pigmi",
                            "private_banks",
                            "ratnakar_bank",
                            "housing_loan",
                            "others_(sbi)",
                            "sbi",
                            "fixed_deposit",
                            "rd",
                            "pnb",
                            "others_(kcc)",
                            "private_bank",
                            "k.c.c.",
                            "commercial_banks",
                            "commercial_bank",
                            "bhuvikas_bank",
                            "others-fd",
                            "fulton_bank",
                        ]
                    ),
                    # grameen banks
                    df["source"].isin(
                        [
                            "grameena_bank_-rd",
                            "grameen_bank",
                            "grameen_bank_(rrb)",
                            "grameen_bank(rrb)",
                            "grameena_bank",
                        ]
                    ),
                    # friends & relatives
                    df["source"].isin(
                        [
                            "others_(friend_&_relatives)",
                            "villagers",
                            "fellow_farmer",
                            "villager",
                            "friends/relatives",
                            "friends_&_relatives",
                        ]
                    ),
                    # finance company
                    df["source"].isin(
                        [
                            "manapuram_private_bank",
                            "pearls_&_gold_schemes",
                            "pearls_scheme",
                            "others_(finance_company)",
                            "micro_finance",
                            "others_(micro_finance)",
                            "other(pearless)",
                            "pearls",
                            "others_(pearless)",
                            "financial_companies",
                            "gold_sukh_scheme",
                            "finance_companies",
                        ]
                    ),
                    # Employer
                    df["source"].isin(
                        [
                            "employer/land_lord",
                            "employer",
                        ]
                    ),
                    # Landlord
                    df["source"].isin(
                        [
                            "landlord",
                        ]
                    ),
                    # shopkeeper
                    df["source"].isin(
                        [
                            "hotel_lending_and_shop",
                            "hotel+shop_lending",
                            "traders",
                            "shop_lending",
                            "milk_dairy",
                            "private_dairy",
                            "dairy",
                            "shopkeeper",
                            "cloth_shop",
                            "flour_mill",
                            "flour_mill_lending",
                            "flour_miller",
                            "milk_centre",
                            "hotel_lending_and_shop",
                            "hotel+shop_lending",
                        ]
                    ),
                    # money lender
                    df["source"].isin(
                        [
                            "others_(specify)_money_lend",
                            "others_(specify)_money_lende",
                            "money_lenders",
                            "money_lender",
                            "moneylender",
                        ]
                    ),
                    # SHG
                    df["source"].isin(
                        [
                            "ngo",
                            "others_(village_association)",
                            "others_(village_commite)",
                            "others_(villager)",
                            "others_(women_association)",
                            "others_(specify)shg",
                            "others_(specify)village_com.",
                            "teachers_edu_society",
                            "teachers_society",
                            "village_committee",
                            "others_(village_committee)",
                            "self_help_groups_(shg)",
                            "self_help_groups",
                            "self_help_groups(shg)",
                        ]
                    ),
                    # commission agent
                    df["source"].isin(
                        [
                            "pawn_brokers",
                            "pawn_broker",
                            "commission_agent",
                            "commission_agent/traders",
                        ]
                    ),
                    # input supplier
                    df["source"].isin(
                        [
                            "input_supplier-dairy",
                            "input_dealer/shopkeeper",
                            "input_supplier",
                        ]
                    ),
                    # Tenants
                    df["source"].isin(
                        [
                            "tenant",
                            "tenants_for_1_month",
                            "tenants",
                        ]
                    ),
                    # Insurance
                    df["source"].isin(
                        [
                            "other(sahara)",
                            "other(tata_aig)",
                            "others(bajaj_allianz)",
                            "others_(_tata_aig)",
                            "lic_loan",
                            "sahara_india",
                            "others_(tata_aig)",
                            "other_(sahara)",
                            "kgrd",  # kgid. from hh in karnataka
                            "others_(sahara)",
                            "sahara",
                            "others_(sahara_india)",
                            "lic",
                            "insurance_(lic,_etc)",
                            "insurance_(lic,_etc.)",
                            "insurance",
                            "insurance_policies",
                        ]
                    ),
                    # Chit funds
                    df["source"].isin(
                        [
                            "chit",
                            "chit_fund",
                            "chit_funds",
                        ]
                    ),
                    # Investments
                    df["source"].isin(
                        [
                            "other(matual_fund)",
                            "other(matule_fund)",
                            "others_(basix)",
                            "shares",
                            "investment-agri.gold",
                            "lic_bond",
                            "share_market",
                            "investment_in_shares,_etc.",
                            "others_(mutual_fund)",
                            "agri.gold",
                            "agri_gold_insurance",
                            "agrigold",
                            "agri_gold",
                            "investment",
                            "fixed_bond",
                        ]
                    ),
                    # GPF PPF etc
                    df["source"].isin(
                        [
                            "others(gpf_etc)",
                            "pension_loan",
                            "service_loan",
                            "gpf/epf/ppf",
                        ]
                    ),
                    # post office
                    df["source"].isin(
                        [
                            "post_office-policy",
                            "post_office_rd",
                            "post_office-rd",
                            "post_offices",
                            "post_office",
                        ]
                    ),
                    # others
                    df["source"].isin(
                        [
                            "cash_in_hand",
                            "cash_on_hand",
                            "central_bank",
                            "dccb",
                            "dharmastala",
                            "gold_loan",
                            "home",
                            "loan_given_to_others",
                            "kwil",
                            "mseb_farm",
                            "others(labour)",
                            "others_(gold_loan)",
                            "others_(gold_lone)",
                            "others_(kwil)",
                            "others-salary_deducted",
                            "owner",
                            "path_swantha",
                            "outsider",
                            "outsiders",
                            "mseb",
                            "pathswantha",
                            "caste_group",
                            "cash_at_home",
                            "others",
                            "other(piperless)",
                        ]
                    ),
                ]

                opts = [
                    "Co_operative banks",
                    "Commercial banks",
                    "Grameen bank",
                    "Friends and relatives",
                    "Finance companies",
                    "Employer",
                    "Landlord",
                    "Shopkeeper",
                    "Moneylender",
                    "Self_help groups",
                    "Commission agent",
                    "Input supplier",
                    "Tenants",
                    "Insurance",
                    "Chit funds",
                    "Derivatives and investments",
                    "GPF_EPF_PPF",
                    "Post office",
                    "Others",
                ]

                source_dict = {
                    "Co_operative banks": 1,
                    "Commercial banks": 2,
                    "Grameen bank": 3,
                    "Friends and relatives": 4,
                    "Finance companies": 5,
                    "Employer": 6,
                    "Landlord": 7,
                    "Shopkeeper": 8,
                    "Moneylender": 9,
                    "Self_help groups": 10,
                    "Commission agent": 11,
                    "Input supplier": 12,
                    "Tenants": 13,
                    "Insurance": 14,
                    "Chit funds": 15,
                    "Derivatives and investments": 16,
                    "GPF_EPF_PPF": 17,
                    "Post office": 18,
                    "Others": 19,
                }

                df["source"] = np.select(conds, opts, default=df["source"])
                df["source"] = df["source"].str.lower().str.replace(" ", "_")

                # df["source"] = df["source"].map(source_dict)

                # print(df["source"].unique())

                # cleaning purpose column

                purpose_dict = {
                    "1": "Agriculture",
                    "2": "Purchase of implements",
                    "3": "Purchase of livestock",
                    "4": "Social functions",
                    "5": "Consumption",
                    "6": "Education",
                    "7": "Medical",
                    "8": " Business",
                    "9": "Repay old debt",
                    "10": "Major repairs",
                    "11": "Purchase of land",
                    "12": "Marriage",
                    "13": " Drill well",
                    "14": "Fisheries",
                    "15": "Others",
                    "nan": "Undefined",
                }

                df["purpose"] = df["purpose"].map(purpose_dict)
                df["purpose"] = (
                    df["purpose"].str.strip().str.lower().str.replace(" ", "_")
                )
                print(df["purpose"].unique())
                print(df["purpose"].dtype)

                # # #pivoting the data and doing necessary cleaning

                # dropping duplicates
                df = df.drop_duplicates(
                    subset=[
                        "hh_id",
                        "category",
                        "source",
                        "amount",
                        "duration",
                        "interest",
                    ]
                )

                # creating a duplicate identifier to isolate funds from same hh from same source and for same purpose
                df["dups"] = df.duplicated(
                    subset=[
                        "hh_id",
                        "category",
                        "source",
                        "purpose"
                        # "amount",
                        # "duration",
                        # "interest",
                    ],
                    keep=False,
                )  # these dups have been manually verified

                # subsetting the dups observation to create a blended rate and agg amount and duration
                df_int = df[df["dups"] == True]
                df = df[df["dups"] == False]
                df_int["interest"] = df_int["amount"] * (df_int["interest"] / 100)

                df_int = (
                    df_int.groupby(["hh_id", "category", "source", "purpose"])
                    .agg({"amount": "sum", "duration": "max", "interest": "sum"})
                    .reset_index()
                )

                df_int["interest"] = (df_int["interest"] / df_int["amount"]) * 100

                # appending both these datasets and dropping dups from df before append

                df.drop("dups", axis=1, inplace=True)

                df = pd.concat([df, df_int], axis=0)

                # df["dups"] = df.duplicated(
                #     subset=[
                #         "hh_id",
                #         "category",
                #         "source",
                #         "purpose"
                #         # "amount",
                #         # "duration",
                #         # "interest",
                #     ],
                #     keep=False,
                # )  # these dups have been manually verified

                # print(df['dups'].value_counts())

                df["id"] = df["category"] + "_" + df["source"] + "_" + df["purpose"]
                df.drop(["category", "source", "purpose"], axis=1, inplace=True)

                df = df.melt(
                    id_vars=["hh_id", "id"],
                    value_vars=["amount", "duration", "interest"],
                    var_name="tag",
                    value_name="value",
                )
                df["id"] = df["id"] + "_" + df["tag"]

                df = df.pivot(
                    index=["hh_id"],
                    columns="id",
                    values="value",
                ).reset_index()
                #     .melt(id_vars="index", value_vars=[])
                # )

                df.to_csv(f"{self.interim_path}/{tag}.csv", index=False)

        widen_vals()

    def plotlist(self):
        """
        This function is specifically cleans the Plotlits.xlsx file in each year under the plotlist questionnaire.
        """

        tag = "Plotlist"

        east_cols = {
            "vdsid": "hh_id_old",
            "plot_code_": "plot_code",
            "plot_name_": "plot_name",
        }

        sat_cols = {"vds_id": "hh_id_old"}

        # unncecessary cols to be removed
        remove_cols = ["crop_6", "vdsid_hhid", "remarks"]

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=False,
        )

        def plot_extra_wrangle():
            if not self.interim_path.joinpath(f"{tag}.csv").exists():
                df = pd.DataFrame(self.appended_file)

                # print(df['hh_no'].apply(np.int64))

                df["hh_no"] = df["hh_no"].fillna(0).astype(int)

                # merging the plot ID and house number to make unique HH ID
                conds = [
                    (df["hh_id_old"].isna()) & (df["hh_no"] < 10),
                    (df["hh_id_old"].isna())
                    & (df["hh_no"] < 100)
                    & (df["hh_no"] >= 10),
                    (df["hh_id_old"].isna())
                    & (df["hh_no"] < 1000)
                    & (df["hh_no"] >= 100),
                    (df["hh_id_old"].isna())
                    & (df["hh_no"] < 10000)
                    & (df["hh_no"] >= 1000),
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
                return df

        def cat_cleaner():
            """
            This function cleans the various categorical variables and creates a new plot subcode identifier.
            """
            if not self.interim_path.joinpath(f"{tag}.csv").exists():
                df = plot_extra_wrangle()

                # #making a new plot code
                # df['plot_code_new']=df['plot_code']+df['sub_plot_code']

                df.drop(["plot_name"], axis=1, inplace=True)

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

                # cleaning crop names
                crop_list = []
                for crop in ["crop_1", "crop_2", "crop_3", "crop_4", "crop_5"]:
                    df[crop] = df[crop].str.strip().str.lower()
                    crop_list.extend(df[crop].unique())

                # print(pd.Series(crop_list).unique())
                # print(pd.Series(crop_list).nunique())

                df = VdsaMicrotSNE.to_float(
                    self,
                    df=df,
                    cols=["plot_area", "crop_area", "irri_area", "rent_rec_paid"],
                )

                df.rename(
                    columns={
                        "ow_stat": "ownership_status_plotlist",
                        "rent_rec_paid": "Plot_rent_received_paid",
                    },
                    inplace=True,
                )

                df.to_csv(f"{self.interim_path}/{tag}.csv", index=False)

        cat_cleaner()

    def family_comp(self):
        """
        This function is specifically cleans the Family composition block file in each year under the GES questionnaire.
        """

        tag = "Family_comp"

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
        ]

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=True,
        )

    def landholding(self):
        """
        This function is specifically cleans the Landholding file in each year under the GES questionnaire.
        """

        tag = "Landholding"

        east_cols = {
            "vdsid": "hh_id",
            "sou_irri1": "sou_irri_1",
            "sou_irri2": "sou_irri_2",
            "dist_sou_irri": "dist_irri_sou",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "sr_no": "sl_no",
            "dist_fr_ho": "dist_from_house",
        }

        # unncecessary cols to be removed
        remove_cols = []

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=False,
        )

        def columns_isolator():
            """This functions helps make the landholdings data a continuation of the plotlist data."""

            if not self.interim_path.joinpath(f"{tag}.csv").exists():
                df = pd.DataFrame(self.appended_file)

                df.drop(
                    [
                        "sl_no",
                        "plot_name",
                        "who_owns",
                        "irri_area",
                        "sou_irri_1",  # need to verify with abhijject whether we need irrigatiomn source in the data
                        "sou_irri_2",
                        "sou_irri_ot",
                        "dist_irri_sou",
                        "remark",
                        "remarks",
                        "remark_b",
                        "soil_type_ot",  # around 500 values but can be ignored since total is 19k +
                        "ch_in_st_ot",
                    ],
                    axis=1,
                    inplace=True,
                )

                df.rename(
                    columns={
                        "ch_in_st": "plot_change_in_status",
                        "ow_stat": "onwership_status_landholding",  # there is a similar variable in plotlist
                    },
                    inplace=True,
                )

                cols = [
                    "plot_change_in_status",
                    "tot_area",
                    "dist_from_house",
                    "soil_type",
                    "soil_depth",
                    "soil_fert",
                    "slope",
                    "soil_degr",
                    "bund_type",
                    "no_of_trees",
                    "plot_val",
                    "revenue",
                    "rental_val",
                    "culti_area",
                    "water_table_depth",
                ]

                df = VdsaMicrotSNE.to_float(self, df=df, cols=cols)

                df.to_csv(f"{self.interim_path}/{tag}.csv", index=False)

        columns_isolator()

    def livestock(self):
        """
        This function is specifically cleans the Livestock inventory file in each year under the GES questionnaire.
        """

        tag = "Livestock_inv"

        east_cols = {"vdsid": "hh_id", "preent_val": "present_val"}

        sat_cols = {
            "vds_id": "hh_id",
        }

        # unncecessary cols to be removed
        remove_cols = ["remarks_c", "mem_owns"]

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=False,
        )

        def cat_cleaner():
            """This functions helps clean the categories of livestock data."""

            if not self.interim_path.joinpath(f"{tag}.csv").exists():
                df = pd.DataFrame(self.appended_file)

                df["livestock_type"] = df["livestock_type"].str.strip().str.lower()

                conds = [
                    df["livestock_type"].isin(
                        [
                            "bullocks(local)",
                            "bullocks(impr.)",
                            "bullock (improved)",
                            "bullock (local)",
                        ]
                    ),
                    df["livestock_type"].isin(
                        [
                            "he buffaloes(local)",
                            "she buffaloes(local)",
                            "she buffaloes(impr.)",
                            "young cattle (buffaloe)",
                            "she buffalo (local)",
                            "he buffalo (local)",
                            "young stock buffalo (<3 years)",
                            "young stock buffallo (<3years)",
                            "she buffalo (improved)",
                            "he buffalo (improved)",
                        ]
                    ),
                    df["livestock_type"].isin(["poultry", "duck", "pigeon"]),
                    df["livestock_type"].isin(
                        [
                            "cows(local)",
                            "cow (local)",
                            "cows(impr./cross bred)",
                            "cow (cross breed)",
                            "cow (crossbreed)",
                            "cow (improved)",
                            "cow (improved/cross breed)",
                            "cow (impr./crossbreed)",
                            "young stock(<3 years)",
                            "young stock",
                            "young stock cattle (<3years)",
                            "young stock cattle (<3 years)",
                            "young stock cattel (<3 years)",
                        ]
                    ),
                ]

                opts = ["bullocks", "buffalo", "poultry", "cow"]

                df["livestock_type"] = np.select(
                    conds, opts, default=df["livestock_type"]
                )

                df = VdsaMicrotSNE.to_float(self, df=df, cols=["present_val"])

                df = (
                    df.groupby(["sur_yr", "hh_id", "livestock_type"])
                    .aggregate({"present_val": "sum", "resource_no": "sum"})
                    .reset_index()
                )

                df.rename(
                    columns={
                        "present_val": "livestock_present_value",
                        "resource_no": "livestock_count",
                    },
                    inplace=True,
                )

                # print(df)

                df.to_csv(f"{self.interim_path}/{tag}.csv", index=False)

        cat_cleaner()

    def farm_equip(self):
        """
        This function is specifically cleans the Farm_Equipment files in each year under the GES questionnaire.
        """

        tag = "Farm_Equipment"

        east_cols = {"vdsid": "hh_id"}

        sat_cols = {"vds_id": "hh_id", "item_no": "item_qty", "item_val": "present_val"}

        # unncecessary cols to be removed
        remove_cols = ["remarks", "remarks_d"]

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=False,
        )

        def string_clean():
            """This functions helps to clean strings columns of farm equipments in the GES questionnaire"""

            if not self.interim_path.joinpath(f"{tag}.csv").exists():
                df = pd.DataFrame(self.appended_file)

                df = VdsaMicrotSNE.to_float(self, df=df, cols=["present_val"])

                # cleaning item name column
                df["item_name"] = df["item_name"].str.strip().str.lower()

                farm_equip_map = "./src/tsne/farm_equip_map.json"

                with open(farm_equip_map, "r") as infile:
                    all_names = dict(json.load(infile))

                df["item_name"] = df["item_name"].map(all_names)

                df["item_name"] = df["item_name"].str.replace(" ", "_").str.lower()
                df["item_name"] = (
                    df["item_name"].str.replace("(", "").str.replace(")", "")
                )

                # cleaning the present value column
                df.rename(
                    columns={"present_val": "farm_equipment_present_value"},
                    inplace=True,
                )

                # converting cols to floats

                df = VdsaMicrotSNE.to_float(
                    self,
                    df=df,
                    cols=["item_qty", "horse_power", "farm_equipment_present_value"],
                )

                return df

        def widen_cols():
            """This functions helps to widen the columns of farm equipments in the GES questionnaire"""

            if not self.interim_path.joinpath(f"{tag}.csv").exists():
                df = string_clean()

                df = (
                    df.groupby(
                        [
                            "hh_id",
                            "item_name",
                        ]
                    )
                    .agg(
                        {
                            "item_qty": "sum",
                            "horse_power": "max",
                            "farm_equipment_present_value": "sum",
                        }
                    )
                    .reset_index()
                )

                # # creating a duplicate identifier
                df["dups"] = df.duplicated(
                    subset=[
                        "hh_id",
                        "item_name",
                    ],
                    keep=False,
                )  # these dups have been manually verified

                df.to_csv(f"{self.interim_path}/{tag}.csv", index=False)

        widen_cols()

    def cons_durab(self):
        """
        This function is specifically cleans the Consumer Durables files in each year under the GES questionnaire.
        """

        tag = "Consumer_durables"

        east_cols = {
            "vdsid": "hh_id",
            "item_durable": "item_name",
            "no_durable": "item_qty",
            "pre_val": "present_value_durable",
            "id_who_owns": "who_owns_durable",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
            "item_con_du": "item_name",
            "no_con_du": "item_qty",
            "val_con_du": "present_value_durable",
            "who_owns_con_du": "who_owns_durable",
            "item_durable": "item_name",
            "no_durable": "item_qty",
            "pre_val": "present_value_durable",
            "id_who_owns": "who_owns_durable",
        }

        # unncecessary cols to be removed
        remove_cols = ["remarks_e_con_du"]

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=True,
        )

    def stock_inv(self):
        """
        This function is specifically cleans the Stock inventory files in each year under the GES questionnaire.
        """

        tag = "Stock_inv"

        east_cols = {
            "vdsid": "hh_id",
            "unit_price": "unit_price_stock",
            "tot_value": "total_value_stock",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
            "unit_pr_stock": "unit_price_stock",
            "tot_val_stock": "total_value_stock",
        }

        # unncecessary cols to be removed
        remove_cols = ["remarks_f"]

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=True,
        )

    def gender_decs_making(self):
        """
        This function is specifically cleans the Gender decision making files in each year under the GES questionnaire.
        """

        tag = "Gend_decision_making"

        east_cols = {
            "vdsid": "hh_id",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
        }

        # unncecessary cols to be removed
        remove_cols = []

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=False,
        )

        def gender_decs_extra_wrangle():
            """
            This function corrects the presence of sperate columns for male and female decsions found in east india files.
            """
            if not self.interim_path.joinpath(f"{tag}.csv").exists():
                df = pd.DataFrame(self.appended_file)

                male_cols = ["ownership_m", "deci_making_m", "who_infl_util_m"]

                female_cols = ["ownership_f", "deci_making_f", "who_infl_util_f"]

                actual_cols = ["ownership", "deci_making", "who_infl_util"]

                col_dict = {
                    "M": "Male",
                    "F": "Female",
                    "B": "Both",
                    "N": np.nan,
                    "NA": np.nan,
                }

                for male, female, actual in zip(male_cols, female_cols, actual_cols):
                    df[male] = df[male].str.strip()
                    df[female] = df[female].str.strip()
                    df[actual] = df[actual].str.strip()
                    # replacing missing valuyes in male columns with values in female columns

                    df[male] = np.where(df[male].isna(), df[female], df[male])
                    df[male] = df[male].map(col_dict)

                    # replacing mapped male cols to the actuals
                    df[actual] = np.where(df[actual].isna(), df[male], df[actual])

                df.drop(female_cols, axis=1, inplace=True)
                df.drop(male_cols, axis=1, inplace=True)

                df.to_csv(self.interim_path.joinpath(f"{tag}.csv"), index=False)

        gender_decs_extra_wrangle()

    def gender_crop_cult(self):
        """
        This function is specifically cleans the Gender crop decision making files in each year under the GES questionnaire.
        """

        tag = "Gend_crop_cult"

        east_cols = {
            "vdsid": "hh_id",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
        }

        # unncecessary cols to be removed
        remove_cols = []

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=False,
        )

        def cat_correct():
            """
            This function corrects the lables of the activity column
            """

            if not self.interim_path.joinpath(f"{tag}.csv").exists():
                df = pd.DataFrame(self.appended_file)

                df["activity"] = (
                    df["activity"].str.strip().str.lower().str.replace(" ", "_")
                )

                conds = [
                    (df["activity"] == "transport_of_fym_&_appl."),
                    (df["activity"] == "chemical_fertilizer_appl."),
                    (df["activity"] == "land_prepration"),
                    (df["activity"] == "seed_selection_ans_storage"),
                ]

                opts = [
                    "transport_of_fym_and_application",
                    "chemical_fertilizer_application",
                    "land_preparation",
                    "seed_selection_and_storage",
                ]

                df["activity"] = np.select(conds, opts, default=df["activity"])

                df.to_csv(f"{self.interim_path}/{tag}.csv", index=False)

        cat_correct()

    def info_ranking(self):
        """
        This function is specifically cleans the Info ranking files in each year under the GES questionnaire.
        """

        tag = "Info_ranking"

        east_cols = {
            "vdsid": "hh_id",
            "item_info": "inputs",
            "input_dealer": "Input Dealer",
            "seed_comp": "Seed Company",
            "farmers": "Other Farmers",
            "ngo": "NGO",
            "govt_dept": "Agriculture/Veterinary Dept",
            "kvk": "Research Station",
            "media": "Media",
            "krishi_melas": "Krishi-melas",
            "others": "Others",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
            "input_dealer": "Input Dealer",
            "seed_comp": "Seed Company",
            "ot_farmers": "Other Farmers",
            "ngo": "NGO",
            "agri_vete_dept": "Agriculture/Veterinary Dept",
            "rese_station": "Research Station",
            "media": "Media",
            "krishi_melas": "Krishi-melas",
            "others": "Others",
        }

        # unncecessary cols to be removed
        remove_cols = []

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=True,
        )

        def info_ranking_pivot():
            """
            This function pivots the various institutions and their rankings as mentioned by subjects
            """

            if not self.interim_path.joinpath(f"{tag}.csv").exists():
                df = pd.DataFrame(self.appended_file)

                df = df.melt(
                    id_vars=["sur_yr", "hh_id", "inputs"],
                    var_name="institution",
                    value_name="ranking",
                )

                df.to_csv(self.interim_path.joinpath(f"{tag}.csv"), index=False)

        info_ranking_pivot()

    def reliab_rank(self):
        """
        This function is specifically cleans the reliability ranking files in each year under the GES questionnaire.
        """

        tag = "Reliability_ranking"

        east_cols = {
            "vdsid": "hh_id",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
        }

        # unncecessary cols to be removed
        remove_cols = []

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=False,
        )

        def clean_cats():
            """
            This cleans reliability ranking categories.
            The pre_defined_categories are the values available from the questionnaire. Remaining values are further categorised and which can't be so segregated are added to 'others(specify)'.
            """

            if not self.interim_path.joinpath(f"{tag}.csv").exists():
                df = pd.DataFrame(self.appended_file)

                df["sou_assistance"] = df["sou_assistance"].str.strip().str.lower()
                df["sou_assistance"] = (
                    df["sou_assistance"]
                    .str.replace("shgs", "shg")
                    .str.replace("ngos", "ngo")
                    .replace("ration shop (pds)", "ration shop(pds)")
                )

                # print(df['sou_assistance'].value_counts()[0:50]
                # )
                # print(df['sou_assistance'].value_counts()[50:100]
                # )
                # print(df['sou_assistance'].value_counts()[100:115]
                # )
                pre_defined_cats = [
                    "kinship and relatives",
                    "friends",
                    "village community",
                    "grameena banks/pacs/commercial banks",
                    "village panchayat",
                    "money lender",
                    "ration shop(pds)",
                    "local group with political affiliations",
                    "shg",
                    "primary health centre",
                    "schools",
                    "private dairy",
                    "ngo",
                    "private companies",
                    "others(specify)",
                ]

                finance_company = [
                    "others(finance company)",
                    "others(micro finance)",
                    "others(finance company micro)",
                    "others(specify)  micro finance",
                    "others(specify)   microfinance",
                    "others(specify) micro finance",
                    "others(specify)  micrto finance",
                    "others (micro finance)",
                    "milano finance",
                    "micro finance",
                    "private companies/chit fund company",
                    "others-chit",
                    "others(specify)micro finance",
                ]  # Micro Finance

                land_lord = [
                    "others(land lords)",
                    "others(land owner)",
                    "landlord",
                    "others(land owner)",
                    "others(landlord)",
                ]  # Land Lord

                employer = [
                    "others(employer)",
                    "employer",
                    "others(specify)employer",
                    "others(employer-oil mill)",
                    "employer-labour contractor",
                    "others-employer",
                    "others-employers",
                    "others (employer)",
                ]

                relatives = ["others(relatives)"]

                labour_work = [
                    "others(specify)  labour",
                    "others(specify)     labour" "others(labour works)",
                    "others(labour work)",
                    "others (labour work)",
                    "others(labour)",
                    "others(specify)   labour work",
                    "others(specify)   labour",
                    "others(specify) labour work",
                    "others(specify)labour",
                    "others(specify)        labour work",
                    "others(specify)    labour work",
                    "others(specify)  labour work",
                ]

                govt = [
                    "others-government",
                    "others(government)",
                    "government",
                    "others(government-tehsildar)",
                    "govt. aid/relief",
                    "others(government tehsildar)",
                    "others(govt.)",
                    "govt dairy",
                    "government dairy",
                    "govt. subsidy",
                    "others-government officials",
                    "others-agricultural department",
                    "others-bsnl department",
                    "others(government of karnataka)",
                ]

                input_dealer = [
                    "others-input dealer",
                    "input dealer",
                    "others(input supplier)",
                    "input supplier",
                    "others(input dealer)",
                    "money lender(input suppliers)",
                ]

                migration = [
                    "others(migration)",
                    "others (migration)",
                    "others(specify)    migeration",
                ]

                merchants = [
                    "others(merchants)",
                    "others(business)",
                    "others(shopkeeper)",
                    "shopkeeper",
                    "others(merchants/shopkeeper)",
                    "others(specify)-shopkeeper",
                    "others-kirana shop",
                ]

                conds = [
                    (df["sou_assistance"].isin(finance_company)),
                    (df["sou_assistance"].isin(land_lord)),
                    (df["sou_assistance"].isin(employer)),
                    (df["sou_assistance"].isin(relatives)),
                    (df["sou_assistance"].isin(govt)),
                    (df["sou_assistance"].isin(input_dealer)),
                    (df["sou_assistance"].isin(migration)),
                    (df["sou_assistance"].isin(merchants)),
                    (df["sou_assistance"].isin(labour_work)),
                    (~df["sou_assistance"].isin(pre_defined_cats)),
                ]

                opts = [
                    "micro finance",
                    "land lord",
                    "employer",
                    "kinship and relatives",
                    "government",
                    "input dealer",
                    "migration",
                    "merchants",
                    "labour work",
                    "others(specify)",
                ]

                df["sou_assistance"] = np.select(
                    conds, opts, default=df["sou_assistance"]
                )

                df.to_csv(self.interim_path.joinpath(f"{tag}.csv"), index=False)

                # print(df['sou_assistance'].value_counts())

        clean_cats()

    def proact_measure(self):
        """
        This function is specifically cleans the proactive measures files in each year under the GES questionnaire.
        """

        tag = "Proactive_measure"

        east_cols = {
            "vdsid": "hh_id",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
        }

        # unncecessary cols to be removed
        remove_cols = []

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=True,
        )

    def govt_assist(self):
        """
        This function is specifically cleans the govt progam assistance files in each year under the GES questionnaire.
        """

        tag = "Govt_assist"

        east_cols = {
            "vdsid": "hh_id",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
        }

        # unncecessary cols to be removed
        remove_cols = ["is_prog_active"]

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=True,
        )

    def crop_info_op(self):
        """
        This function is specifically cleans the Crop_info_op files in each year under the Cultivation questionnaire.
        """

        tag = "Crop_info_op"

        east_cols = {
            "vdsid": "hh_id",
            "cult_id/hhid/vdsid": "hh_id",
            "var_name": "crop_variety_name",
            "var_type": "crop_variety_type",
            "plot_co": "plot_code",
            "remarks": "op_remarks",
            "ow_stat": "plot_ownership_status",
            "op_main_prod__rate": "op_main_prod_rate",
            "rent_for": "rent_tenure",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
            "var_name": "crop_variety_name",
            "var_type": "crop_variety_type",
            "plot_co": "plot_code",
            "remarks": "op_remarks",
            "crop": "crop_name",
        }

        # unncecessary cols to be removed
        remove_cols = ["var_type_ot", "plot_name"]

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=True,
        )

    def cult_inputs(self):
        """
        This function is specifically cleans the cultivation input files in each year under the Cultivation questionnaire.
        """

        tag = "Cult_ip"

        east_cols = {
            "vdsid": "hh_id",
            "cult_id/hhid/vdsid": "hh_id",
            "remarks": "crop_ip_remarks",
            "ip_remarks": "crop_ip_remarks",
            "ow_stat": "plot_ownership_status",
            "rent_for": "rent_tenure",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
            "year_total_income": "hh_id",
            "plot_co": "plot_code",
            "remarks": "crop_ip_remarks",
            "ip_remarks": "crop_ip_remarks",
        }

        # unncecessary cols to be removed
        remove_cols = ["plot_name", "round_no", "village"]

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=True,
        )

    def food_exp(self):
        """
        This function is specifically cleans the food expenditure files in each year under the Transaction questionnaire.
        This function only covers food expenditure of SAT India.
        """

        tag = "Food_item"

        east_cols = {
            "vdsid": "hh_id",
            "cult_id/hhid/vdsid": "hh_id",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
        }

        # unncecessary cols to be removed
        remove_cols = []

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=True,
        )

    def nf_exp(self):
        """
        This function is specifically cleans the non-food expenditure files in each year under the Transaction questionnaire.
        This function only covers Non-Food expenditure of SAT India.
        """

        tag = "Non_food_item"

        east_cols = {
            "vdsid": "hh_id",
            "cult_id/hhid/vdsid": "hh_id",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
        }

        # unncecessary cols to be removed
        remove_cols = []

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=True,
        )

    def f_nf_exp(self):
        """
        This function is specifically cleans the food and non-food expenditure files in each year under the Transaction questionnaire.
        This function covers Foood & Non-Food expenditure of only EAST India.
        """

        tag = "Exp_food_non_food"

        east_cols = {
            "vdsid": "hh_id",
            "cult_id/hhid/vdsid": "hh_id",
            "hhid/vdsid": "hh_id",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
        }

        # unncecessary cols to be removed
        remove_cols = ["who_gave", "wage_ot"]

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=True,
        )

    def fin_trans(self):
        """
        This function is specifically appends the financial transactions files in each year under the Transaction questionnaire.
        """

        tag = "Fin_Trans"

        east_cols = {
            "vdsid": "hh_id",
            "cult_id/hhid/vdsid": "hh_id",
            "hhid/vdsid": "hh_id",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
        }

        # unncecessary cols to be removed
        remove_cols = [
            "from_whom",
            "from_whom_ot",
            "who_sp",
            "purpose",
            "cast_co",
            "cast_co_ot",
        ]

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=True,
        )

    def loans(self):
        """
        This function is specifically appends the loans transactions files in each year under the Transaction questionnaire.
        """

        tag = "Loans"

        east_cols = {
            "vdsid": "hh_id",
            "cult_id/hhid/vdsid": "hh_id",
            "hhid/vdsid": "hh_id",
            "who_did_id": "id_who_did",
        }

        sat_cols = {"vds_id": "hh_id", "vdsid": "hh_id", "who_did_id": "id_who_did"}

        # unncecessary cols to be removed
        remove_cols = ["who_sp_ben"]

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=True,
        )

    def prod_sold(self):
        """
        This function is specifically appends the products sold files in each year under the Transaction questionnaire.
        """

        tag = "Prod_Sold"

        east_cols = {
            "vdsid": "hh_id",
            "cult_id/hhid/vdsid": "hh_id",
            "hhid/vdsid": "hh_id",
        }

        sat_cols = {"vds_id": "hh_id", "vdsid": "hh_id"}

        # unncecessary cols to be removed
        remove_cols = []

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=False,
        )

        def cat_correct():
            """
            This function corrects the lables of the products category column
            """

            if not self.interim_path.joinpath(f"{tag}.csv").exists():
                df = pd.DataFrame(self.appended_file)

                df["crop_lst_prod"] = df["crop_lst_prod"].str.strip().str.title()

                df["crop_lst_prod"] = np.where(
                    df["crop_lst_prod"] != "Crop", "Livestock Products", "Crop"
                )

                df.to_csv(f"{self.interim_path}/{tag}.csv", index=False)

        cat_correct()

    def sale_pur(self):
        """
        This function is specifically appends the sales and purchase files in each year under the Transaction questionnaire.
        """

        tag = "Sale_pur"

        east_cols = {
            "vdsid": "hh_id",
            "cult_id/hhid/vdsid": "hh_id",
            "hhid/vdsid": "hh_id",
        }

        sat_cols = {"vds_id": "hh_id", "vdsid": "hh_id", "pur_dist": "pur_pl_dist"}

        # unncecessary cols to be removed
        remove_cols = []

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=True,
        )

    def govt_dev_prog(self):
        """
        This function is specifically appends the benefits from govt dev programs files in each year under the Transaction questionnaire.
        """
        # This function deviates in terms of usage from others because for years 2011, 2013, 2014 in east and 2014 in sat the amount of benefit
        # from govt is read in as a problematic string which requires two rounds of it being written out as a csv and read again. This fucntion achieves the above
        tag = "Govt_dev_progs_benefits"

        east_cols = {
            "vdsid": "hh_id",
            "cult_id/hhid/vdsid": "hh_id",
            "hhid/vdsid": "hh_id",
            "program": "program_name",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
            "who_ben": "id_who_ben",
            "prog_name": "program_name",
        }

        # unncecessary cols to be removed
        remove_cols = ["is_prog_active"]

        VdsaMicrotSNE.path_values_create(
            self, region_folder_position=8
        )  # region folder position = 6 for windows and 8 for linux

        interim_appended_file_path = self.interim_path.joinpath(f"{tag}.csv")

        if not interim_appended_file_path.exists():
            # creating a subset of raw_path_list which isolates the path
            raw_paths_sublist = []
            for x in self.raw_path_list:
                if tag == x["tag"]:
                    raw_paths_sublist.append(x)

            raw_data_list = (
                []
            )  # defining an emplty list to hold the raw data before appending

            for file in raw_paths_sublist:
                print(file["path"].stem, file["region"], file["year"])

                # reading in the raw file
                df = pd.read_excel(file["path"])

                # cleaning of column names
                col_list = df.columns
                col_list = [x.lower().replace(" ", "_") for x in col_list]
                df.columns = col_list

                # removing unnecessary columns from the data
                col_list = [x for x in col_list if x not in remove_cols]
                df = df[col_list]

                # renaming the necessary columns. Names will be sourced fronm the function assigned for each tag
                if file["region"] == "eastindia":
                    df.rename(columns=east_cols, inplace=True)

                if file["region"] == "satindia":
                    df.rename(columns=sat_cols, inplace=True)

                # Inititating two rounds of write and read sequence for converting string cols with emplty character ('') into float64
                if df["amt_ben"].dtype == object:
                    # print(df['amt_ben'].str.strip().unique())

                    temp_file_path = self.interim_path.joinpath("temp.csv")
                    df.to_csv(temp_file_path, index=False)
                    df = pd.read_csv(temp_file_path)
                    temp_file_path.unlink()
                    # print(df['amt_ben'].dtype)
                    df["amt_ben"] = df["amt_ben"].str.strip()

                    df.to_csv(temp_file_path, index=False)
                    df = pd.read_csv(temp_file_path)
                    temp_file_path.unlink()
                    # print(df['amt_ben'].dtype)

                # Post two step sequential read and write process, we continue to append df list and send out a common file to the interim directory
                # adding year value in satindia file
                try:
                    if file["region"] == "satindia":
                        df.insert(0, "sur_yr", file["year"])
                except ValueError as ex:
                    print(
                        f"Error: Survey year already exists in {file['region']} {file['year']}"
                    )

                raw_data_list.append(df)

            df_appended = pd.concat(raw_data_list, axis=0)

            df_appended.to_csv(f"{self.interim_path}/{tag}.csv", index=False)

        else:
            pass

    def building(self):
        """
        This function is specifically appends the buildings files in each year under the GES questionnaire.
        """

        tag = "Building"

        east_cols = {
            "vdsid": "hh_id",
            "cult_id/hhid/vdsid": "hh_id",
            "hhid/vdsid": "hh_id",
            "val_pre": "building_value",
            "id_who_owns": "who_owns_buil",
        }

        sat_cols = {
            "vds_id": "hh_id",
            "vdsid": "hh_id",
            "item_buil": "item_building",
            "val_buil": "building_value",
        }

        # unncecessary cols to be removed
        remove_cols = ["remarks_e_buil"]

        VdsaMicrotSNE.data_wrangler(
            self,
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
            export_file=False,
        )

        def pivot_east():
            """
            This function melts the data to long specifically for east india
            """

            if not self.interim_path.joinpath(f"{tag}.csv").exists():
                df = pd.DataFrame(self.appended_file)

                # print(df['item_building'].value_counts(dropna=False))

                # cleaning the category values in the item_building column
                df["item_building"] = df["item_building"].str.strip().str.title()

                conds = [
                    (
                        df["item_building"].isin(
                            ["Type Of House", "Type Of House (Code)"]
                        )
                    ),
                    (
                        df["item_building"].isin(
                            [
                                "Cooking Gas (Lpg)",
                                "Cooking Gas(Lpg)",
                                "Cooking Gas (Gobar)",
                            ]
                        )
                    ),
                    (
                        df["item_building"].isin(
                            [
                                "Star Connection",
                                "Star Connection (Cable/Dish)",
                                "Cable Connection",
                            ]
                        )
                    ),
                    (
                        df["item_building"].isin(
                            ["Others", "Others (Specify)", "Others-Motor"]
                        )
                    ),
                    (
                        df["item_building"].isin(
                            ["Area Of Courtyard", "Area Of Courtyard (Sq.Feet)"]
                        )
                    ),
                    (df["item_building"].isin(["Kerosene Stove", "Kerosen Stove"])),
                ]

                opts = [
                    "Type Of House",
                    "Cooking Gas",
                    "Cable TV",
                    "Others",
                    "Area Of Courtyard",
                    "Kerosene Stove",
                ]

                df["item_building"] = np.select(
                    conds, opts, default=df["item_building"]
                )
                # print(df['item_building'].unique())

                # pivoting values for columns specificcaly for eastindia

                conds = [
                    (df["region"] == "eastindia")
                    & (df["item_building"] == "Residential House")
                    & (df["facility"].isna()),
                    (df["region"] == "eastindia")
                    & (df["item_building"] == "Type Of House")
                    & (df["facility"].isna()),
                    (df["region"] == "eastindia")
                    & (df["item_building"] == "Area Of Courtyard")
                    & (df["facility"].isna()),
                    (df["region"] == "eastindia")
                    & (
                        ~df["item_building"].isin(
                            ["Residential House", "Type Of House", "Area Of Courtyard"]
                        )
                    )
                    & (df["facility"].isna()),
                ]

                opts = [
                    df["own_rented"].astype(str),
                    df["house_type"].astype(str),
                    df["courtyard_pre"].astype(str),
                    df["facility_pre"].astype(str),
                ]

                df["facility"] = np.select(conds, opts, default=df["facility"])

                # removing wide columns from east india
                df.drop(
                    ["own_rented", "house_type", "courtyard_pre", "facility_pre"],
                    axis=1,
                    inplace=True,
                )

                df.to_csv(f"{self.interim_path}/{tag}.csv", index=False)

        pivot_east()
