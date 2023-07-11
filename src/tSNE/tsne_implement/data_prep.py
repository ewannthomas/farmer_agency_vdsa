from utils.tsne.dir_values import dir_values
from utils.tsne.merge_data import merge_data


interim_path, processed_path, external_path = dir_values()
final_file = processed_path.joinpath("tsne.csv")


def tsne_data_prep():
    """A function to prepare the final data on which t_SNE will be implemented"""

    if not final_file.exists():
        tags = ["Gen_info", "total_cult_yr"]

        df = merge_data(tags)

        print(df)

        df.to_csv(final_file, index=False)

    else:
        print("T-SNE processed file exists.")
