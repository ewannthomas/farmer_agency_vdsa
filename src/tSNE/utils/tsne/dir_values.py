from pathlib import Path


def dir_values():
    """
    This function sets in place all the dependencies and defines the path structures used in any further functions.
    """

    dir_path = Path(__file__).resolve().parents[4]
    interim_path = dir_path.joinpath("data/interim/tsne")
    long_path = dir_path.joinpath("data/interim/tsne/long_data")
    processed_path = dir_path.joinpath("data/processed/tsne")
    prepocessed_path = dir_path.joinpath("data/preprocessed/tsne")

    # creating the data directories
    if not interim_path.exists():
        interim_path.mkdir(parents=True)

    if not processed_path.exists():
        processed_path.mkdir(parents=True)

    if not prepocessed_path.exists():
        prepocessed_path.mkdir(parents=True)

    return interim_path, long_path, processed_path, prepocessed_path
