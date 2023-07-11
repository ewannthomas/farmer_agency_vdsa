import functools
import pandas as pd
from utils.tsne.dir_values import dir_values


interim_path, processed_path, external_path = dir_values()


def special_data_cases():
    """A function to process special datasets befor merging for t-SNE implemetation"""

    dfs = []

    def success():
        tag = "total_cult_yr"

        interim_file = interim_path.joinpath(f"{tag}.csv")

        df = pd.read_csv(interim_file)

        df = (
            df[(df["success"].notna())]
            .drop("sur_yr", axis=1)
            .drop_duplicates(subset="hh_id_panel")
        )  # manually verifed. We have 181 hh

        return df

    dfs.append(success())

    return dfs


def merge_data(tags: list):
    """A function to input a list of wide data tags, merged into a single dataset, to be subjected for t-SNE and DL operations.

    Parameters:

    tags: A list of data tags which are present in the 'data/interim/tsne' directory"""

    input_paths = list(interim_path.glob("*.csv"))
    input_paths = [
        path for path in input_paths if path.stem in tags
    ]  # and path.stem != "total_cult_yr"

    print(input_paths)

    dfs = [pd.read_csv(path) for path in input_paths]
    # dfs.extend(special_data_cases())

    df = functools.reduce(
        lambda left_df, right_df: pd.merge(
            left=left_df,
            right=right_df,
            how="outer",
            on=["hh_id_panel", "sur_yr"],
            validate="1:1",
        ),
        dfs,
    )

    return df
