from utils.dir_values import dir_values
from utils.data_wrangler import data_wrangler
from utils.to_float import to_float
from utils.check_duplicates import check_duplicates
from utils.widen_frame import widen_frame
from utils.long_frame import long_frame
import pandas as pd
import numpy as np


def landholding():
    """
    This function is specifically cleans the Landholding file in each year under the GES questionnaire.
    """

    tag = "Landholding"

    raw_path, interim_path, processed_path, external_path = dir_values()

    interim_file = interim_path.joinpath(f"{tag}.csv")

    if not interim_file.exists():
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
        remove_cols = [
            "remarks",
            "remark_b",
            "remark",
            "ch_in_st_ot",
            "plot_name",
            "sou_irri_ot",
            "bund_type_ot",
            "soil_type_ot",
            "soil_degr_ot",
        ]

        df = data_wrangler(
            tag=tag,
            rename_east=east_cols,
            rename_sat=sat_cols,
            remove_cols=remove_cols,
        )
        # df.drop(
        #     [
        #         "soil_type_ot",
        #         "soil_degr_ot",
        #         "bund_type_ot",
        #     ],
        #     axis=1,
        #     inplace=True,
        # )

        # converting all cloumns with numbers to float
        cols = [
            "ch_in_st",
            "tot_area",
            "dist_from_house",
            "irri_area",
            "sou_irri_1",
            "sou_irri_2",
            "dist_irri_sou",
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

        df = to_float(df=df, cols=cols)

        ###MAKE THESE CHANGES AFTER APPROVAL FROM ABHIJEET##########################################################################
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

        # mapping sources of irrigation
        irri_source_map = {
            1: "Open well",
            2: "Borewell",
            3: "Tank/pond",
            4: "Canal",
            5: "River",
            6: "Others",
        }

        for col in ["sou_irri_1", "sou_irri_2"]:
            df[col] = df[col].replace(irri_source_map)

        # mapping status code
        status_dict = {
            0: "Presently operating",
            1: "Sold",
            2: "Given out as gift",
            3: "Given out due to family division",
            4: "Leased-in land given back to land owner",
            5: "Part of the plot sold/gifted out/given to family members",
            6: "Leased-out",
            7: "Loss of plot due to other reasons",
            8: "Purchased",
            9: "Received as gift",
            10: "Received due to family division",
            11: "Leased-out land taken back from the tenant",
            12: "Leased-in",
            13: "Received plot due to other reasons",
        }

        df["ch_in_st"] = df["ch_in_st"].replace(status_dict)

        # mapping soil type
        soil_types = {
            1: "Red",
            2: "Shallow black/Murrum",
            3: "Medium Black",
            4: "Deep Black",
            5: "Sandy",
            6: "Loam",
            7: "Sandy loam",
            8: "Clay",
            9: "Clay loam",
            10: "Problematic soils (Saline/ alkaline, etc.)",
            11: "Others",
        }

        df["soil_type"] = df["soil_type"].replace(soil_types)

        # mapping soil fertility
        soil_fertility_map = {1: "Very poor", 2: "Poor", 3: "Good", 4: "Very good"}

        df["soil_fert"] = df["soil_fert"].replace(soil_fertility_map)

        # mapping slope

        slope_dict = {
            1: "Levelled 0-1%",
            2: "Slight slope 1-3%",
            3: "Medium slope 3-10%",
            4: "High slope >10%",
        }

        df["slope"] = df["slope"].replace(slope_dict)

        # mapping soil degradation
        soil_degradation = {
            1: "No problem",
            2: "Soil erosion",
            3: "Nutrient depletion",
            4: "Waterlogging",
            5: "Salinity/Acidity",
            6: "Others",
        }

        df["soil_degr"] = df["soil_degr"].replace(soil_degradation)

        # mapping bunding
        bund_map = {"Y": "Yes", "N": "No"}
        df["bunding"] = df["bunding"].replace(bund_map)

        # mapping bunding type
        bunding_dict = {
            1: "Bunds within field",
            2: "Soil conservation bunds",
            3: "Property bunds around the plot",
            4: "Others",
        }
        df["bund_type"] = df["bund_type"].replace(bunding_dict)

        ############################################################################################################

        # # Cleaning Duplicates ####################################################################################

        # # Reassigning plot code for hh IOR12D0055
        # conds : (
        #     (df["hh_id"] := "IOR12D0055")
        #     & (df["sl_no"] == 9)
        #     & (df["plot_code"] == "I")
        # )

        # df["plot_code"] = np.where(conds, "J", df["plot_code"])
        # ##########################################################################################################

        df.rename(
            columns={
                "ch_in_st": "plot_change_in_status",
                "ow_stat": "onwership_status_landholding",  # there is a similar variable in plotlist
            },
            inplace=True,
        )

        # checking duplicates
        check_duplicates(
            df=df,
            index_cols=["hh_id", "sl_no", "plot_code"],
            master_check=False,
            write_file=True,
        )

        # exporting long dataframe
        long_frame(tag=tag, df=df)

        df = widen_frame(df=df, index_cols=["hh_id", "sl_no", "plot_code"])

        df.to_csv(interim_file, index=False)

    else:
        print(f"{tag} interim file exists")
