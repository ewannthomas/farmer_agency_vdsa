import pandas as pd
from functools import reduce
from utils.to_float import to_float


def widen_frame(
    df: pd.DataFrame,
    index_cols: list,
    wide_cols: list,
    agg_dict: dict,
):
    """
    This function converts the entire dataframe into a wider version of itself and writes it to the tSNE folder in the interim data directory. It conducts the Pandas Pivot fucntion to achieve the same, after ensuring the absence of duplicates in the dataframe.

    Parameters:

    df: A pandas dataframe to be widened. The input can be a fucntion rendering the desired dataframe or a dataframe.

    index_cols: A list of column names which will be used as index of the dataframe to perform duplication check, groupby and widening.

    wide_cols: A list of column names which will be, strictly, converted to float and reduced to statisitcs mentioned in the agg_dict based on the index_cols groups.

    agg_dict: A dictionary which defines the summaryu statistic that should be created for each col in the wide_cols list while performing the groupby operation.
    """

    try:
        # converting expected wide required cols to float
        df = to_float(df, cols=wide_cols)

        for col in wide_cols:
            if df[col].dtype == "object":
                raise TypeError

        # checking for duplicates
        # df["dups"] = df.duplicated(keep=False)
        # dup_count = df["dups"].value_counts()[True]
        # print(dup_count)
        # if dup_count > 0:
        #     raise TabError

        # creating groups using index cols and creating summary stats based on agg_dict
        df = df.groupby(index_cols).agg(agg_dict).reset_index()

        final_wide_cols = []
        for col in index_cols:
            if col != "hh_id":
                final_wide_cols.append(col)
                # df[col] = df[col].astype(str).fillna("undefined")

        # widening the columns
        df = df.pivot(index="hh_id", columns=final_wide_cols, values=wide_cols)

        # renamimg the Multiindex
        level_names = df.columns
        col_names = ["_".join(x) for x in level_names]
        df.columns = col_names
        df.reset_index(inplace=True)

        # df['id']=reduce(lambda df[a],df[b] df[a]+"_"+df[b], wide_cols )

    except TypeError:
        print(f"string object in {col}")

    except TabError:
        print("Duplicates in data. Halting Process.")

    except KeyError:
        pass

    return df
