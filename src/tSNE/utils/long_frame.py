import pandas as pd
from utils.to_float import to_float
from utils.dir_values import dir_values


def long_frame(df: pd.DataFrame, tag: str, cols=None):
    """
    This function retains the long format of the data frame and exports a copy of the same to sub directory in the interim directory

    Paramerters:
    df: A pandas dataframe to be widened.

    cols: A list of column names which will be, strictly, converted to float.
    """
    raw_path, interim_path, processed_path, external_path = dir_values()

    long_folder = interim_path.joinpath("long_data")

    if not long_folder.exists():
        long_folder.mkdir(parents=True)

    interim_file = long_folder.joinpath(f"{tag}.csv")

    if cols != None:
        df = to_float(df=df, cols=cols, error_action="raise")

    df.to_csv(interim_file, index=False)
