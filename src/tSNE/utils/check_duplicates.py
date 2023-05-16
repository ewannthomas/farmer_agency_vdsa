import pandas as pd
from utils.dir_values import dir_values


def check_duplicates(
    df: pd.DataFrame, index_cols: list, master_check=False, write_file=False
):
    """
    This fucntion checks for duplicate values within the dataset.
    Parameters:
    df: A pandas dataframe to be subjected to duplication check.

    index_cols: A list of column names which will be used as index of the dataframe to perform duplication check.

    master_check: (default: False) A boolean, if True,  will check duplication on all the columns and ignores subset of column mentioned in index_cols.

    write_file: (default: False) A boolean, if True, will write the existing dataframe to the interim directory and includes the duplicates identifier column.
    """

    raw_path, interim_path, processed_path, external_path = dir_values()

    df_proxy = df.copy()

    dup_file = interim_path.joinpath("dups.csv")
    try:
        dup_file.unlink()
    except FileNotFoundError:
        print()

    if master_check == True:
        try:
            df_proxy["dups"] = df_proxy.duplicated(keep=False)

            dup_count = df_proxy["dups"].value_counts()[True]
            if dup_count > 0:
                raise TabError

        except TabError:
            if write_file == True:
                print(
                    f"{dup_count} duplicates across all columns. Halting process and writing file to interim directory."
                )
                df_proxy[df_proxy["dups"] == True].to_csv(dup_file, index=False)
            else:
                print(f"{dup_count} duplicates across all columns. Halting process.")

        except KeyError:
            print("No duplicates across all columns of the dataframe")

    else:
        try:
            df_proxy["dups"] = df_proxy.duplicated(subset=index_cols, keep=False)

            dup_count = df_proxy["dups"].value_counts()[True]
            if dup_count > 0:
                raise TabError

        except TabError:
            if write_file == True:
                df_proxy.sort_values(index_cols, inplace=True)
                print(
                    f"{dup_count} duplicates across index columns. Halting process and writing file to interim directory."
                )
                df_proxy[df_proxy["dups"] == True].to_csv(dup_file, index=False)
            else:
                print(f"{dup_count} duplicates across index columns. Halting process.")

        except KeyError:
            print("No duplicates across index columns of the dataframe")
