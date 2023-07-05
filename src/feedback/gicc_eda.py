"""How many female headed households adopted what coping mechanism for each calamity?"""
from rules_summary.fem_cop_mech import count_fem_hh_cop_mech_yr
from rules_summary.fem_cop_mech import count_fem_hh_cop_mech

count_fem_hh_cop_mech()
count_fem_hh_cop_mech_yr()

"""How many female headed households gave highest rank for information from institutions?"""
"""How many female headed households sought information from institutions for which inputs?"""
from rules_summary.fem_info_ranking import count_fem_hh_inputs
from rules_summary.fem_info_ranking import count_fem_hh_inputs_yr
from rules_summary.fem_info_ranking import count_fem_hh_institutions
from rules_summary.fem_info_ranking import count_fem_hh_institutions_yr

count_fem_hh_inputs()
count_fem_hh_inputs_yr()
count_fem_hh_institutions()
count_fem_hh_institutions_yr()

"""What are the institutions which female headed households trust the most for assisstance during a calamity?"""
from rules_summary.fem_reliab_rank import count_fem_hh_reliab_rank
from rules_summary.fem_reliab_rank import count_fem_hh_reliab_rank_yr

count_fem_hh_reliab_rank()
count_fem_hh_reliab_rank_yr()

"""Does access to information and institutions by the household vary by caste of household head?"""
from rules_summary.info_caste import count_caste_info
from rules_summary.info_caste import count_caste_info_yr

count_caste_info()
count_caste_info_yr()


"""Does households belonging to different castes adopt different coping mechanisms?"""
from rules_summary.caste_cop_mech import caste_cop_mech_all
from rules_summary.caste_cop_mech import caste_cop_mech
from rules_summary.caste_cop_mech import caste_cop_mech_problem
from rules_summary.caste_cop_mech import caste_cop_mech_all_yr
from rules_summary.caste_cop_mech import caste_cop_mech_yr
from rules_summary.caste_cop_mech import caste_cop_mech_problem_yr

caste_cop_mech_all()
caste_cop_mech()
caste_cop_mech_problem()
caste_cop_mech_all_yr()
caste_cop_mech_yr()
caste_cop_mech_problem_yr()


"""Does coping mechanism adopted by a household vary by the features of land owned?"""
from rules_summary.land_owned_cop_mech import count_hh_soil_type
from rules_summary.land_owned_cop_mech import count_hh_soil_type_yr
from rules_summary.land_owned_cop_mech import count_soil_type_cop_mech
from rules_summary.land_owned_cop_mech import count_soil_type_cop_mech_yr

from rules_summary.land_owned_cop_mech import count_hh_own_status
from rules_summary.land_owned_cop_mech import count_hh_own_status_yr
from rules_summary.land_owned_cop_mech import count_own_status_cop_mech
from rules_summary.land_owned_cop_mech import count_own_status_cop_mech_yr

from rules_summary.land_owned_cop_mech import count_hh_irri_source
from rules_summary.land_owned_cop_mech import count_hh_irri_source_yr
from rules_summary.land_owned_cop_mech import count_irri_source_cop_mech
from rules_summary.land_owned_cop_mech import count_irri_source_cop_mech_yr

count_hh_soil_type()
count_hh_soil_type_yr()
count_soil_type_cop_mech()
count_soil_type_cop_mech_yr()

count_hh_own_status()
count_hh_own_status_yr()
count_own_status_cop_mech()
count_own_status_cop_mech_yr()

count_hh_irri_source()
count_hh_irri_source_yr()
count_irri_source_cop_mech()
count_irri_source_cop_mech_yr()

"""How many households were successful?"""
"""How many households were successful in which calamity?"""
"""What coping mechanisms lead to success?"""
from rules_summary.succes_cop_mech import success_count
from rules_summary.succes_cop_mech import success_calamity_count
from rules_summary.succes_cop_mech import success_cop_mech
from rules_summary.succes_cop_mech import success_cop_mech_yr

success_count()
success_calamity_count()
success_cop_mech()
success_cop_mech_yr()


"""How many male and female headed households adopted which coping mechanism and was successful?"""
from rules_summary.success_gender_cop_mech import success_gender_cop_mech_yr
from rules_summary.success_gender_cop_mech import success_gender_cop_mech

success_gender_cop_mech()
success_gender_cop_mech_yr()
