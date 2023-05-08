

*##############################Creating Coefficients based Ranks for Reliability ranking##################

*adding the directories

clear

	local dir "C:\Work ISB\projects\frer"
	local interim_folder "`dir'\data\interim"
	local cleaned_folder "`interim_folder'\cleaned"
	local reduced_folder "`interim_folder'\reduced"
	local output_folder "`interim_folder'\stata_files"

*importing reliab_ranking file
	import delimited "`cleaned_folder'\Reliability_ranking.csv", numericc(4 5)
	save "`output_folder'\Reliability_ranking.dta", replace
	clear
	
	
*importing reliab_ranking file
	import delimited "`reduced_folder'\Crop_info_op.csv"
	save "`output_folder'\Crop_info_op.dta", replace

	
*Merging relibaility ranking file to cultivation file
	merge 1:m hh_id using "`output_folder'\Reliability_ranking"
	
	reg total_production i.rank_rel_dro
	
	
	
