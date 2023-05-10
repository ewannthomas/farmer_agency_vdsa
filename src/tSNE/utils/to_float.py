import pandas as pd
from pathlib import Path
from utils.dir_values import dir_values


def to_float(df: pd.DataFrame, cols: list, error_action="ignore"):
    """
    This function converts the specified columns which inherited their string character into floats.
    Parameters:
    df: A pandas dataframe which contains the columns to be converted to float
    cols: A list of columns which are objects and need to be converted to float
    error_action: (default:ignore) An action analogous to IgnoreRaise. Accepted values are ignore and raise.
    """

    raw_path, interim_path, processed_path, external_path = dir_values()

    temp_file = interim_path.joinpath("temp.csv")

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

    # rechecking presence of string columns in the converted file
    if error_action == "raise":
        for col in cols:
            try:
                if df[col].dtype == "object":
                    raise TypeError

            except TypeError:
                print(
                    f"string objects in {col}. Cannot convert all the values to float."
                )
                print(f"Unique values in {col} are :")
                print(df[col].unique())
    elif error_action == "ignore":
        pass

    return df
