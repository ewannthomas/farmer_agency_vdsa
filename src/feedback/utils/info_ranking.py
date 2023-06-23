import pandas as pd
from utils.dir_values import dir_values

interim_path, long_path, results_folder = dir_values()


def info_ranking():
    """A function to convert info ranking dataset in long_data folder to further long along columns mentioned in the script"""
    """This function doesn't alter the data at source and requires to be called everytime when the long form of the info ranking dataset is required."""

    tag = "Info_ranking"

    interim_file = long_path.joinpath(f"{tag}.csv")

    df = pd.read_csv(interim_file)

    # print(df.columns)

    df = df.melt(
        id_vars=["hh_id", "sur_yr", "hh_id_panel", "inputs"],
        value_vars=[
            "Input Dealer",
            "Seed Company",
            "Other Farmers",
            "NGO",
            "Agriculture/Veterinary Dept",
            "Research Station",
            "Media",
            "Krishi-melas",
            "Others",
        ],
        var_name="institutions",
        value_name="rank",
    )

    return df
