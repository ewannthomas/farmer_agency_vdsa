import pandas as pd


def merger_info(df: pd.DataFrame):
    """ "
    This function identifies the unique number of households which merged from the right and left files used for merging
    """

    left_only = df[df["_merge"] == "left_only"]["hh_id_panel"].unique()
    right_only = df[df["_merge"] == "right_only"]["hh_id_panel"].unique()
    both = df[df["_merge"] == "both"]["hh_id_panel"].unique()

    print(len(left_only))
    print(len(right_only))

    left_only = [x for x in left_only if x not in both]
    right_only = [x for x in right_only if x not in both]

    df.drop("_merge", axis=1, inplace=True)

    print("Unmerged HH in left:", len(left_only))
    print("Unmerged HH in right:", len(right_only))
    print("Merged HH:", len(both))

    print(df.shape)

    return df
