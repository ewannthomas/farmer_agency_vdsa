import pandas as pd
from utils.dir_values import dir_values

raw_path, interim_path, long_path, processed_path, external_path = dir_values()

tag = "Family_comp"

interim_file = long_path.joinpath(f"{tag}.csv")


df = pd.read_csv(interim_file)

for i in df.groupby("hh_id"):
    if 1.0 not in i[1]["relation"].to_list():
        print(i[1]["hh_id"].unique())
