
clear


*Defining directories

	local dir "D:\work_isb\projects\frer"

	local interim_folder "`dir'\data\interim"

	local stata_files "`interim_folder'\stata_files"

	local long_folder "`interim_folder'\tsne\long_data"

	local src "`dir'\src\feedback"

	local include_script "`src'\include.do"

	local result_folder "`dir'\results\feedback"


*****************************DATA IMPORT AND PARK********************************************************

*Calling in the panel data cleaning script

	local data_1 "`long_folder'\Info_ranking.csv"

	local data_2 "`long_folder'\Family_comp.csv"
	
	
	
*import and save info_ranking
	import delimited using "`data_1'"
	
	local info_out_file "`stata_files'\Info_ranking.dta"
	
	keep if sur_yr ==2010
	
// 	unique hh_id_panel, by ( sur_yr)
	
	save "`info_out_file'", replace 
	
	clear
	
	
	
	
*importing coping mechanism

	local data_3 "`long_folder'\Coping_Mech.csv"
	
	import delimited using "`data_3'"

	local cop_mech_out_file "`stata_files'\Coping_Mech.dta"
	
	keep if sur_yr ==2010
	
// 	unique hh_id_panel, by ( sur_yr)
	
	save "`cop_mech_out_file'", replace 
	
	clear
	
******************************************************************************************************************************************************************************************************	





	*importing Family comp data
	
 	import delimited using "`data_2'", numericc(5)

 	*filtering of only members who are household heads
 	keep if relation==1
	keep if female ==1
	keep if sur_yr==2010
	
	tab female

	
*Merging both data to find instituions used by female and male 
		
	merge 1:m hh_id using "`info_out_file'"
	keep if _merge==3
	drop _merge
	
*making tables of input frequency
	local results_file "`result_folder'\count_info_ranking_inputs_frequency.xls"
	tabout inputs using "`results_file'", oneway append ///
	c(freq col cum) f(0c 2p 2p) clab(Frequency Percentage Cumulative_Percentage)
			

*identifying the most reliable instituions
	preserve
	keep sur_yr hh_id hh_id_panel inputs institutions rank
	drop if rank != 1
	tab institutions, sort missing
	
	tab2 inputs institutions
	restore
	

*Merging both cop_mech to find mechanisms adopted by female and male 
		
	merge m:m hh_id using "`cop_mech_out_file'"
	keep if _merge==3
	
	sort hh_id inputs institutions 
	br hh_id inputs institutions problem if hh_id=="IAP10A0048"




	

	
	
	