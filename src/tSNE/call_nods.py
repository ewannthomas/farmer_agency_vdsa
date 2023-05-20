from raw_data_clean.gen_info import gen_info_cleaner
from raw_data_clean.assests_liabs import assests_liabs
from raw_data_clean.farm_equip import farm_equip
from raw_data_clean.plotlist import plotlist
from raw_data_clean.family import family_comp
from raw_data_clean.landholding import landholding
from raw_data_clean.livestock import livestock
from raw_data_clean.consumer_durables import cons_durab
from raw_data_clean.stock_inv import stock_inv
from raw_data_clean.gender_decs_making import gender_decs_making
from raw_data_clean.gender_crop_cult import gender_crop_cult
from raw_data_clean.info_ranking import info_ranking
from raw_data_clean.reliab_rank import reliab_rank
from raw_data_clean.proact_measures import proact_measures
from raw_data_clean.govt_assist import govt_assist
from raw_data_clean.crop_info_op import crop_info_op


gen_info_cleaner()
assests_liabs()
farm_equip()
plotlist()
family_comp()
landholding()
livestock()
cons_durab()
stock_inv()
gender_decs_making()
gender_crop_cult()
info_ranking()
reliab_rank()
# proact_measures()
# govt_assist()
crop_info_op()
