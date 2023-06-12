from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.widen_frame import widen_frame
from utils.long_frame import long_frame
import pandas as pd
import numpy as np


def assests_liabs():
    """
    This function is specifically cleans the Fin_assets_liabilities.xlsx file in each year under the GES questionnaire.
    """
    raw_path, interim_path, processed_path, external_path = dir_values()

    tag = "Fin_assets_liabilities"

    interim_file = interim_path.joinpath(f"{tag}.csv")

    if not interim_file.exists():
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

        df = data_wrangler(
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
        )

        df["category"] = df["category"].str.strip().str.lower()

        # cleaning inteerest and duration columns which are strings and has a character "DK" in it.
        df = to_float(df=df, cols=["interest", "duration"])
        df["interest"] = df["interest"].str.strip().str.replace("DK", "")
        df["duration"] = df["duration"].str.strip().str.replace("DK", "")

        df = to_float(df=df, cols=["interest", "duration", "purpose"])
        df["interest"] = df["interest"].astype(float)
        df["duration"] = df["duration"].astype(float)
        df["purpose"] = df["purpose"].astype(str).str.replace(".0", "")

        # cleaning source column categories
        df["source"] = df["source"].str.strip().str.lower().str.replace(" ", "_")

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
        df["purpose"] = df["purpose"].str.strip().str.lower().str.replace(" ", "_")
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
            df_int.groupby(["hh_id", "sur_yr", "category", "source", "purpose"])
            .agg({"amount": "sum", "duration": "max", "interest": "sum"})
            .reset_index()
        )

        df_int["interest"] = (df_int["interest"] / df_int["amount"]) * 100

        # appending both these datasets and dropping dups from df before append

        df.drop("dups", axis=1, inplace=True)

        df = pd.concat([df, df_int], axis=0)

        # exporting long dataframe
        long_frame(
            tag=tag,
            df=df,
            cols=[
                "amount",
                "duration",
                "interest",
            ],
        )

        df = widen_frame(
            df=df,
            index_cols=["hh_id", "category", "source", "purpose"],
            wide_cols=[
                "amount",
                "duration",
                "interest",
            ],
        )

        # print(df)

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
