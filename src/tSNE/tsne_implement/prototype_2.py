from utils.tsne.dir_values import dir_values
from utils.tsne.merge_data import merge_data
from utils.tsne.column_reducer import column_reducer
from utils.to_float import to_float
import pandas as pd


interim_path, long_data, processed_path, preprocessed_path = dir_values()
proto_path = preprocessed_path.joinpath("prototype_2")
if not proto_path.exists():
    proto_path.mkdir(parents=True)
final_file = processed_path.joinpath("tsne_prototype_2.csv")


def sub_data_preps():
    """A function to prepare the and store the sub datasets for t-SNE implementation."""

    files = list(interim_path.glob("*.csv"))
    tags = [file.stem for file in files]

    for file in files:
        if file.stem not in ["total_cult_crop", "Govt_dev_progs_benefits"]:
            sub_data_file = proto_path.joinpath(f"{file.stem}.csv")
            if not sub_data_file.exists():
                df = column_reducer(pd.read_csv(file, low_memory=False), tag=file.stem)
                df.to_csv(sub_data_file, index=False)
            else:
                print(f"{file.stem} exists.")


def p2_data_prep():
    """A function to prepare the final data on which t_SNE will be implemented"""

    final_file = processed_path.joinpath("tsne_prototype_2.csv")

    if not final_file.exists():
        # initializing preprocessed data creation from sub_data_preps
        sub_data_preps()

        input_paths = list(preprocessed_path.glob("prototype_2/*.csv"))

        df = merge_data(paths=input_paths)

        # isloating the feature names
        cols_missing = [
            col for col in df.columns if col not in ["hh_id_panel", "sur_yr"]
        ]

        # ensuring all cols are floats
        df = to_float(df=df, cols=cols_missing, error_action="raise")

        print(df)

        df.to_csv(final_file, index=False)

    else:
        print("T-SNE prototype 2 file exists.")
