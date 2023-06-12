from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
from utils.long_frame import long_frame
import pandas as pd
import numpy as np
import json


def consum_expend():
    """
    This function is specifically cleans the food expenditure files in each year under the Transaction questionnaire.
    This function only covers food expenditure of SAT India.
    """

    tags = ["Food_item", "Non_food_item", "Exp_food_non_food"]

    data_holder_list = []  # defining an empty list to hold the datasets

    raw_path, interim_path, processed_path, external_path = dir_values()

    interim_file = interim_path.joinpath(f"consumption_expenditure.csv")

    if not interim_file.exists():
        for tag in tags:
            east_cols = {
                "vdsid": "hh_id",
                "cult_id/hhid/vdsid": "hh_id",
                "vdsid": "hh_id",
                "cult_id/hhid/vdsid": "hh_id",
                "hhid/vdsid": "hh_id",
            }

            sat_cols = {
                "vds_id": "hh_id",
                "vdsid": "hh_id",
            }

            # unncecessary cols to be removed
            remove_cols = ["remarks", "remarks", "nf_remarks", "who_gave", "wage_ot"]

            df = data_wrangler(
                tag=tag,
                rename_east=east_cols,
                rename_sat=sat_cols,
                remove_cols=remove_cols,
            )

            # making the date column correct
            df["sur_mon_yr"] = pd.to_datetime(df["sur_mon_yr"], format="%m/%y")

            # Wrangler for Food Items
            if tag == "Food_item":
                # cleaning food item type column
                df["item_type"] = df["item_type"].str.strip().str.lower()

                food_item_map = {
                    "milk & milk prod.": "dairy products",
                    "milk and milk products": "dairy products",
                    "leafy vegetables": "vegetables",
                    "non-veg (meat and eggs)": "meat products",
                    "sea food": "meat products",
                }
                df["item_type"] = df["item_type"].replace(food_item_map)

                # recoding all the fruits in "all fruits and vegetables" to fruits. 28,297 obs were recoded.
                df["item_type"] = np.where(
                    (df["item_type"] == "all fruits and vegetables")
                    & (df["item_name"].str.contains("fruits")),
                    "fruits",
                    df["item_type"],
                )  # this operation was verified using value counts

                # recoding "all fruits and vegetables" as vegetables.
                df["item_type"] = df["item_type"].replace(
                    {"all fruits and vegetables": "vegetables"}
                )

                # converting total value of expenditure to float
                df["tot_val"] = np.where(df["tot_val"].str.isdigit(), df["tot_val"], "")
                df = to_float(df=df, cols=["tot_val"], error_action="raise")

                # renaming tot_val of expenses
                df.rename(columns={"tot_val": "total_expense"}, inplace=True)

                # removing dups across all columns
                df.drop_duplicates(
                    inplace=True
                )  # we drop 215 obs which were manually checked and verified

                check_duplicates(
                    df=df,
                    index_cols=["hh_id", "sur_mon_yr", "item_type"],
                    master_check=True,
                    write_file=True,
                )

                # groupng and aggregating the data
                df = (
                    df.groupby(
                        [
                            "hh_id",
                            "sur_mon_yr",
                            "item_type",
                        ]
                    )["total_expense"]
                    .agg(sum)
                    .reset_index()
                )

            elif tag == "Non_food_item":
                df.drop_duplicates(
                    inplace=True
                )  # manually verified. 41 obs will be removed.

                check_duplicates(
                    df=df,
                    index_cols=["hh_id", "sur_mon_yr", "nf_item_name"],
                    master_check=True,
                    write_file=True,
                )

                # converting nf_tot_val to float
                df["nf_tot_val"] = np.where(
                    df["nf_tot_val"].str.isdigit(), df["nf_tot_val"], ""
                )
                df = to_float(df=df, cols=["nf_tot_val"], error_action="raise")

                # grouping across household and month to get total non-food cons expense
                df = (
                    df.groupby(
                        [
                            "hh_id",
                            "sur_yr",
                            "sur_mon_yr",
                        ]
                    )["nf_tot_val"]
                    .agg(sum)
                    .reset_index()
                )

                # renaming nf_total_val
                df.rename(columns={"nf_tot_val": "total_expense"}, inplace=True)

                # creating the item_type column
                df["item_type"] = "non food expenditure"

            elif tag == "Exp_food_non_food":
                # cleaning item cols
                for col in ["item_category", "item_type", "item_name"]:
                    df[col] = df[col].str.strip().str.lower()

                df["item_type"] = np.where(
                    (df["item_category"] == "non-food") & (df["item_type"].isna()),
                    "non-food expenditure",
                    df["item_type"],
                )  # there are cases where non-food items have misisng item  types. This has been corrected.

                # replacing rogue values in item_type column
                item_map = {
                    "non-veg (meat and eggs)": "meat products",
                    "meat, egg and fish": "meat products",
                    "meat egg and fish": "meat products",
                    "meat, egg & fish": "meat products",
                    "sea food": "meat products",
                    "milk and milk products": "dairy products",
                    "milk and milk prod.": "dairy products",
                    "milk & milk prod.": "dairy products",
                    "others:beverages": "other food items",
                    "others: spices": "other food items",
                    "others food items": "other food items",
                    "beverages": "other food items",
                    "fresh fruits": "fruits",
                    "vegetable": "vegetables",
                }
                df["item_type"] = df["item_type"].replace(item_map)

                # replacing fruits and dry fruits in "all fruits and vegetables" under item_type. SO we find values in item_name by name and replace item_type based on these names
                fruits_list = [
                    "apple",
                    "banana",
                    "mango",
                    "jackfruit: green",
                    "orange",
                    "mausami",
                    "papaya: green",
                    "guava",
                    "lemon",
                    "papaya",
                    "bitter gourd",
                    "musk melon",
                    "watermelon",
                    "grapes",
                    "pear, naspati",
                    "other fresh fruits",
                    "berries",
                    "other fresh fruits (ghurama)",
                    "other fresh fruits (pomegranate)",
                    "pineapple",
                    "pomogranate",
                    "camot",
                    "other fresh fruits (black berry)",
                    "other fresh fruits (srikhand)",
                    "other fresh fruits (kendu)",
                    "other fresh fruits (char)",
                    "other fresh fruits (palm fruit)",
                    "other fresh fruits (palm)",
                    "other fresh fruits (peanut)",
                    "muskmelon",
                    "other fresh fruits (custard apple)",
                    "other fresh fruits (sappodilla)",
                ]

                dry_fruits_list = [
                    "raisin",
                    "kishmish",
                    "monacca",
                    "dry dates",
                    "other dry fruits (sago)",
                    "cashewnut",
                    "other dry fruits",
                    "other dry fruits (mixed)",
                    "other dry fruits (peanuts)",
                    "foxnut",
                ]

                df["item_type"] = np.where(
                    df["item_name"].isin(fruits_list), "fruits", df["item_type"]
                )
                df["item_type"] = np.where(
                    df["item_name"].isin(dry_fruits_list), "dry fruits", df["item_type"]
                )
                # print(df["item_type"].unique())
                # print(df["item_type"].nunique())

                # after isolating all_fruits_vegatables, recoding it as vegatbles
                df["item_type"] = df["item_type"].replace(
                    {"all fruits and vegetables": "vegetables"}
                )

                # removing duplicates across all columns
                df.drop_duplicates(
                    inplace=True
                )  # manually verified. 2925 obs will be removed.

                # converting tot_val to float
                df["tot_val"] = np.where(df["tot_val"].str.isdigit(), df["tot_val"], "")
                df = to_float(df=df, cols=["tot_val"], error_action="raise")

                df.rename(columns={"tot_val": "total_expense"}, inplace=True)

                check_duplicates(
                    df=df,
                    index_cols=["hh_id", "sur_mon_yr", "item_type"],
                    master_check=True,
                    write_file=True,
                )

                # grouping and aggregating the data
                df = (
                    df.groupby(
                        [
                            "hh_id",
                            "sur_yr",
                            "sur_mon_yr",
                            "item_type",
                        ]
                    )["total_expense"]
                    .agg(sum)
                    .reset_index()
                )

            data_holder_list.append(df)

        # concatenating the datasets
        df = pd.concat(data_holder_list, axis=0)

        # exporting long dataframe
        long_frame(tag="consumption_expenditure", df=df)

        df = widen_frame(
            df=df,
            index_cols=["hh_id", "sur_mon_yr", "item_type"],
        )

        print(df)
        print(df.shape)

        df.to_csv(interim_file, index=False)

    else:
        print(f"consumption_expenditure interim file exists")
