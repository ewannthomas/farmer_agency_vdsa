import pandas as pd
import numpy as np
from pathlib import Path

"""
Thi scsript creates mutliple cross entropy measures and entropy measures for the various sources of assistance items in the reliability ranking file.
We use cross entrop and entropy measures and the ideal one will selected post panel data regression.
Cross entropy will created as distance between a preferred ranking and actual ranking of items. For more info, visit: https://cran.r-project.org/web/packages/RankAggreg/vignettes/RankAggreg.pdf 
"""


#defining directories and path
dir_path=Path.cwd()
interim_path=dir_path.joinpath('data', 'interim')
cleaned_files=interim_path.joinpath('cleaned')
reduced_path=interim_path.joinpath('reduced')
in_file=cleaned_files.joinpath('Reliability_ranking.csv')
temp_file=cleaned_files.joinpath('temp.csv')


#calling in and cleaning the file
df=pd.read_csv(in_file)
df['rank_rel_dro']=df['rank_rel_dro'].str.replace(' ', '')
df['rank_rel_flo']=df['rank_rel_flo'].str.replace(' ', '')
df.to_csv(temp_file,index=False)
df=pd.read_csv(temp_file)
temp_file.unlink()



#creating the preferred ordered list of assisstance based on their frequency distribution
ordered_rank=df['sou_assistance'].value_counts().reset_index().reset_index().drop(labels='sou_assistance',axis=1)

ordered_rank.rename(
    columns={
    'level_0':'preferred_rank',
    'index':'item'
    }, inplace=True
)

#remodifying the rank for 'others(specify) to be the last of all
ordered_rank['preferred_rank']=ordered_rank['preferred_rank']+1
ordered_rank['preferred_rank']=np.where(ordered_rank['preferred_rank']>15,ordered_rank['preferred_rank']-1, ordered_rank['preferred_rank'])
ordered_rank['preferred_rank']=np.where(ordered_rank['item']=='others(specify)',23, ordered_rank['preferred_rank'])

#creating the prefrred ranks dictionary to create cross entropy
rank_dict=dict(zip(ordered_rank['item'],ordered_rank['preferred_rank']))


#mapping rank_dict to actual df and creating ce values
df['preferred_rank']=df['sou_assistance'].map(rank_dict)
df['drought_ce']=abs(df['preferred_rank']-df['rank_rel_dro'])
df['flood_ce']=abs(df['preferred_rank']-df['rank_rel_flo'])

#summarizing by sum of ce
df=df.groupby(['hh_id'])[['drought_ce','flood_ce']].agg(sum)

print(df)