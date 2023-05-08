import pandas as pd
import numpy as np
from pathlib import Path
from functools import reduce
from reducer import VdsaMicroReducer


#defining directories and path
dir_path=Path.cwd()
interim_path=dir_path.joinpath('data', 'interim')
reduced_path=interim_path.joinpath('reduced')
processed_path=dir_path.joinpath('data', 'processed')
out_file=processed_path.joinpath("panel_regression.csv")

files=list(reduced_path.glob('*.csv'))

data_list=[]

for file in files:
    df=pd.read_csv(file)

    df['hh_id_panel']=df['hh_id_panel'].str.strip()
    df['hh_id']=df['hh_id'].str.strip()

    vdsa=VdsaMicroReducer()
    vdsa.data_validator(df=df, tag=file.stem)

    data_list.append(df)

merged_data=reduce(lambda left, right: pd.merge(left,
                                                right,
                                                on=['sur_yr','hh_id', 'hh_id_panel'],
                                                how='outer',
                                                validate='1:1'), data_list)

vdsa.data_validator(df=merged_data, tag='merged')
#merged_data['dups']=merged_data.duplicated(subset=['sur_yr', 'hh_id_panel'], keep=False)

merged_data.to_csv(out_file, index=False)
