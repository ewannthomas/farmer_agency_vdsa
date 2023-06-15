import pandas as pd


def merger_info(df: pd.DataFrame):
    """ "
    This function identifies the unique number of households which merged from the right and left files used for merging
    """

    df_merge = df.groupby("_merge")["hh_id_panel"].nunique()

    print(df_merge)
    print(df.shape)
