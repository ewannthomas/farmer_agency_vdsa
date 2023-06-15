import pandas as pd
from utils.dir_values import dir_values

raw_path, interim_path, processed_path, external_path = dir_values()

tag = "Info_ranking"

interim_file = interim_path.joinpath(f"{tag}.csv")


df = pd.read_csv(interim_file)

# print(df.columns)

df = df.melt(
    id_vars=["hh_id", "sur_yr", "hh_id_panel", "inputs"],
    value_vars=[
        "Input Dealer",
        "Seed Company",
        "Other Farmers",
        "NGO",
        "Agriculture/Veterinary Dept",
        "Research Station",
        "Media",
        "Krishi-melas",
        "Others",
    ],
    var_name="institutions",
    value_name="rank",
)

df.to_csv(interim_file, index=False)
