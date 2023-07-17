import pandas as pd

pd.set_option("mode.chained_assignment", None)  # setting chained assignment warning off


def column_reducer(df: pd.DataFrame, tag: str, threshold: float = 0.6):
    """A function to clean wide interim data columns. This fucntion will remove columns with all missing entries, columns which have missing entires more than a defined threshold of the data"""
    if tag not in ["total_cult_yr"]:
        print(f"#### {tag}")
        print(f"- columns before trim:{len(df.columns)}")

        # removing all columns with only nan
        initial_count = len(df.columns)
        df = df.dropna(axis=1, how="all")
        second_count = initial_count - len(df.columns)
        print(f"- columns dropped with all NaN:{second_count}")
        post_all_nan_col_len = len(df.columns)

        # removing columns with more than 70 percent data
        cols = []
        for col in df.columns:
            miss_percent = round(df[col].isna().sum() / len(df), 2)

            if miss_percent > threshold:
                # print(col, miss_percent)
                cols.append(col)

        df.drop(labels=cols, axis=1, inplace=True)

        third_count = post_all_nan_col_len - len(df.columns)
        print(f"- columns dropped with NaN beyond {threshold} threshold:{third_count}")

        print(f"- columns post reducing:{len(df.columns)}")

        # print(df)

    return df
