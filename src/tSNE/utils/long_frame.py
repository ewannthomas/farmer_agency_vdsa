import pandas as pd
from utils.to_float import to_float
from utils.dir_values import dir_values
from utils.hh_id_create import hh_id_create


def long_frame(df: pd.DataFrame, tag: str, cols: list = None, hh_id: bool = True):
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

    if hh_id:
        df = hh_id_create(df=df)

    df.to_csv(interim_file, index=False)
