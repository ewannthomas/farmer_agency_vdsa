import pandas as pd
from utils.to_float import to_float


def widen_frame(
    df: pd.DataFrame,
    index_cols: list,
    wide_cols: list = None,
    agg_dict: dict = None,
):
    """
    This function converts the entire dataframe into a wider version of itself and writes it to the tSNE folder in the interim data directory. It conducts the Pandas Pivot fucntion to achieve the same, after ensuring the absence of duplicates in the dataframe.

    Parameters:

    df: A pandas dataframe to be widened.

    index_cols: A list of column names which will be used as index of the dataframe to perform duplication check, groupby and widening.

    wide_cols: A list of column names which will be, strictly, converted to float and reduced to statisitcs mentioned in the agg_dict based on the index_cols groups.

    agg_dict: A dictionary which defines the summary statistic that should be created for each col in the wide_cols list while performing the groupby operation.
    """
    if agg_dict != None:
        try:
            # converting expected wide required cols to float
            df = to_float(df, cols=wide_cols)

            for col in wide_cols:
                if df[col].dtype == "object":
                    raise TypeError

            # creating groups using index cols and creating summary stats based on agg_dict
            if agg_dict != None:
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

    else:
        final_wide_cols = []
        for col in index_cols:
            if col != "hh_id":
                final_wide_cols.append(col)
                # df[col] = df[col].astype(str).fillna("undefined")

        # now since columns to be widened are not specified, we need to remove sur_yr from the columns
        index_cols.append("sur_yr")

        wide_cols = [x for x in df.columns if x not in index_cols]

        # widening the columns
        df = df.pivot(index="hh_id", columns=final_wide_cols, values=wide_cols)

        # renamimg the Multiindex
        level_names = df.columns

        col_names = ["_".join(list(map(str, x))) for x in level_names]
        df.columns = col_names
        df.reset_index(inplace=True)

        return df
