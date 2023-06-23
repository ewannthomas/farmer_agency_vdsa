from pathlib import Path


def dir_values():
    """
    This function sets in place all the dependencies and defines the path structures used in any further functions.
    """

    dir_path = Path(__file__).resolve().parents[3]
    interim_path = dir_path.joinpath("data/interim")
    long_path = dir_path.joinpath("data/interim/tsne/long_data")
    results_folder = dir_path.joinpath("results/feedback")

    return interim_path, long_path, results_folder
