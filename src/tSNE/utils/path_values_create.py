from pathlib import Path
from utils.dir_values import dir_values


def path_values_create(tag: str, region_folder_position: int):
    """
    This function creates a list of iteratble windows paths for the raw data depending on its block position in the VDSA Micro questionnaire.
    Parameters:
    region_folder_position: An integer mentioning the folder position of the region folder (eastindia or satindia) in the windows path of the raw data directory. The count starts from zero by adhering to the python list convention.
                            Example: 'C:\Work ISB\projects\frer\data\raw\eastindia\2012' has region_folder_poition of 6 (starting from 0). Similarly for linux systems its 8.

    """

    # tag_list = [
    #     "Coping_Mech",
    #     "Proactive_measure",
    #     "Drought_Assistance",
    #     "Gen_info",
    #     "Fin_assets_liabilities",
    #     "Plotlist",
    #     "Family_comp",
    #     "Landholding",
    #     "Livestock_inv",
    #     "Farm_Equipment",
    #     "Consumer_durables",
    #     "Stock_inv",
    #     "Gend_decision_making",
    #     "Gend_crop_cult",
    #     "Info_ranking",
    #     "Reliability_ranking",
    #     "Govt_assist",
    #     "Crop_info_op",
    #     "Cult_ip",
    #     "Food_item",  # food, non-food and exp_foof_non_food are tags connected with f and nf expenses. They are split into 3 and called seperately for the ease of operation.
    #     "Non_food_item",
    #     "Exp_food_non_food",
    #     "Fin_Trans",
    #     "Loans",
    #     "Prod_Sold",
    #     "Sale_pur",
    #     "Govt_dev_progs_benefits",
    #     "Building",
    # ]

    path_list = []  # creating a list for path and dependency dictionary

    raw_path, interim_path, processed_path, external_path = dir_values()

    if tag == "Gen_info":
        # this condition will ensure that we collect only household general information from the ges folder
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
        patterns = [
            f"*/*/ges/*.Con_*.xlsx",
            f"*/*/ges/Con_*.xlsx",
            f"*/*/ges/Consumer_durabale.xlsx",
        ]

    elif tag == "Reliability_ranking":
        patterns = [f"*/*/ges/*.How_reliable*.xlsx", f"*/*/ges/*{tag}.xlsx"]

    elif tag == "Proactive_measure":
        patterns = [f"*/*/ges/*.Proact*.xlsx", f"*/*/ges/*{tag}.xlsx"]

    elif tag == "Govt_assist":
        patterns = [f"*/*/ges/*.{tag}*.xlsx", f"*/*/ges/Drought*.xlsx"]

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
            f"*/*/ges/Govt_dev*.xlsx",
            f"*/*/*/Ben_govt_*.xlsx",
            f"*/2013/ges/Gov*.xlsx",
        ]

    elif tag == "Farm_Equipment":
        patterns = [
            f"*/*/*/*.{tag}.xlsx",
            f"*/*/*/Farm_equpment.xlsx",
            f"*/*/*/{tag}.xlsx",
            "*/*/*/*.Farm_equipment.xlsx",
        ]
    elif tag == "Prod_Sold":
        patterns = [
            f"*/*/*/*.{tag}.xlsx",
            f"*/*/*/{tag}.xlsx",
            "*/*/*/Prod_Sold-10.xlsx",
        ]

    else:
        patterns = [f"*/*/*/*.{tag}.xlsx", f"*/*/*/{tag}.xlsx"]

    for pat in patterns:
        raw_file_paths = list(raw_path.glob(pat))

        for file in raw_file_paths:
            # if you are windows systems replace "/" by "\\" to get parent folders and region folder position will be 8
            parent_region = str(file).split("/")[region_folder_position]
            year = str(file).split("/")[(region_folder_position + 1)]

            path_dict = {
                "tag": tag,
                "path": file,
                "region": parent_region,
                "year": year,
            }

            path_list.append(path_dict)

    # else:
    #     print(f"Files for {tag} exists.")
    #     path_dict = {"tag": tag, "interim_path": interim_appended_file_path}
    #     path_list.append(path_dict)
    #     # continue

    return path_list
