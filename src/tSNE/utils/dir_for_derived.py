from pathlib import Path


def dir_values():
    """
    This function sets in place all the dependencies and defines the path structures used in any further functions.
    """

    dir_path = Path(__file__).resolve().parents[3]
    interim_path = dir_path.joinpath("data/interim/tsne")
    results_path = dir_path.joinpath("results/tsne")
    long_data_path = dir_path.joinpath("data/interim/tsne/long_data")

    # creating the data directories
    if not results_path.exists():
        results_path.mkdir(parents=True)

    return interim_path, results_path, long_data_path
