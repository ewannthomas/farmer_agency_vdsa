"""How many female headed households adopted what coping mechanism for each calamity?"""
from rules_summary.fem_cop_mech import count_fem_hh_cop_mech_yr
from rules_summary.fem_cop_mech import count_fem_hh_cop_mech

"""How many female headed households gave highest rank for information from institutions?"""
"""How many female headed households sought information from institutions for which inputs?"""
from rules_summary.fem_info_ranking import count_fem_hh_inputs
from rules_summary.fem_info_ranking import count_fem_hh_inputs_yr
from rules_summary.fem_info_ranking import count_fem_hh_institutions
from rules_summary.fem_info_ranking import count_fem_hh_institutions_yr

"""What are the institutions which female headed households trust the most for assisstance during a calamity?"""
from rules_summary.fem_reliab_rank import count_fem_hh_reliab_rank
from rules_summary.fem_reliab_rank import count_fem_hh_reliab_rank_yr

"""Does access to information and institutions by the household vary by caste of household head?"""
from rules_summary.info_caste import count_caste_info
from rules_summary.info_caste import count_caste_info_yr

"""Does households belonging to different castes adopt different coping mechanisms?"""
from rules_summary.caste_cop_mech import caste_cop_mech_all
from rules_summary.caste_cop_mech import caste_cop_mech
from rules_summary.caste_cop_mech import caste_cop_mech_problem
from rules_summary.caste_cop_mech import caste_cop_mech_all_yr
from rules_summary.caste_cop_mech import caste_cop_mech_yr
from rules_summary.caste_cop_mech import caste_cop_mech_problem_yr

"""Does coping mechanism adopted by a household vary by the features of land owned?"""
from rules_summary.land_owned_cop_mech import soil_type

#########################################################################################################################


##Calling the fucntions

"""How many female headed households adopted what coping mechanism for each calamity?"""
count_fem_hh_cop_mech()
count_fem_hh_cop_mech_yr()

"""How many female headed households gave highest rank for assistances from institutions, during flood and drought?"""
count_fem_hh_inputs()
count_fem_hh_inputs_yr()
count_fem_hh_institutions()
count_fem_hh_institutions_yr()

"""What are the institutions which female headed households trust the most for assisstance during a calamity?"""
count_fem_hh_reliab_rank()
count_fem_hh_reliab_rank_yr()

"""Does access to information and institutions by the household vary by caste of household head?"""
count_caste_info()
count_caste_info_yr()


"""Does households belonging to different castes adopt different coping mechanisms?"""
caste_cop_mech_all()
caste_cop_mech()
caste_cop_mech_problem()
caste_cop_mech_all_yr()
caste_cop_mech_yr()
caste_cop_mech_problem_yr()


"""Does coping mechanism adopted by a household vary by the features of land owned?"""
soil_type()
