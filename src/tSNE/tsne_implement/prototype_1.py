from utils.tsne.dir_values import dir_values
from utils.tsne.merge_data import merge_data


interim_path, long_data, processed_path, preprocessed_path = dir_values()
final_file = processed_path.joinpath("tsne_prototype_1.csv")


def data_prep():
    """A function to prepare the final data on which t_SNE will be implemented"""

    if not final_file.exists():
        tags = ["Gen_info", "total_cult_yr"]

        input_paths = list(interim_path.glob("*.csv"))
        input_paths = [path for path in input_paths if path.stem in tags]

        df = merge_data(paths=input_paths)

        print(df)

        df.to_csv(final_file, index=False)

    else:
        print("T-SNE prototype 1 file exists.")
