import pandas as pd
from pathlib import Path
from utils.dir_values import dir_values
from utils.path_values_create import path_values_create


def data_wrangler(
    tag: str,
    rename_east: dict,
    rename_sat: dict,
    remove_cols: list,
):
    """
    This function wrangles the data file supplied via path. It performs a set of predefined actions necessary for appending the various files spread across years.
    Parameters:

    tag: A string value enabling in identifying the exact location of the file to be wrangled using the path_values_create method defined under the VdsaMicrotSNE class.

    rename_east: A dictionary which will be used for renamimg anmd standardizing the column names in the files pertaining to East India.
                    Key: Old column name
                    Value: New column name

    rename_sat: A dictionary which will be used for renamimg anmd standardizing the column names in the files pertaining to Semi tropical arid (SAT) India.
                    Key: Old column name
                    Value: New column name

    remove_cols: A list of columns names which are to be removed from the file.

    """

    # adopting list of raw file paths
    raw_paths_list = path_values_create(region_folder_position=8, tag=tag)

    if len(raw_paths_list) < 10:
        print(f"Files missing from {tag}. Available are:")
        for file in raw_paths_list:
            print(file["path"].stem, file["region"], file["year"])
        print("Halting Process")

    elif len(raw_paths_list) >= 10:
        raw_data_list = []

        for file in raw_paths_list:
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

            # print(tag)
            # print(df.columns)

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

        return df_appended
