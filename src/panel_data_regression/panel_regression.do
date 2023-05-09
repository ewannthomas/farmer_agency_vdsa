clear


*Defining directories
	local dir "C:\Work ISB\projects\frer"
	
	local processed_folder "`dir'\data\processed"
	local result_folder "`dir'\results\panel_data_regression"
	local results_file "`result_folder'\phase1_panel_reg.rtf"

	
	local data_cleaning_script "`dir'\src\panel_data_regression\panel_data_cleaning.do"
	
	
*Calling in the panel data cleaning script
	do "`data_cleaning_script'"
	
	
*Panel Setting the Data
	xtset hh_id_encoded sur_yr
	
*Definging indeps and running Fixed Effects regression
	global base_vars male_cop_mech_index female_cop_mech_index farm_equipment_present_value net_financial_position reliab_ranking total_value_stock govt_ben_prog_amount_received
	
	global base_controls i.caste_group i.religion family_size building_index i.hh_type_of_house consumer_durables_present_value
	
	*Panel regression without hh controls
		xtreg total_production $base_vars, fe vce(r)
		outreg2 using "`results_file'", word title("Phase 1 Results") ///
		ct("Total Farm Production") ///
		adjr2 ///
		addstat(R-squared within model,`e(r2_w)', ///
				R-squared overall model, `e(r2_o)', ///             
				R-squared between model, `e(r2_b)') ///
		addtext(Household Controls, NO, Household Fixed Effects, YES, Time Fixed Effects, YES) ///
		addn("Notes: Household controls include caste, religion, type of housing, household facilities and family size") ///
		drop(i.caste_group i.religion family_size building_index i.hh_type_of_house i.caste_group==5 i.caste_group==6 i.religion==3) ///
		label append 
	
	
	*Panel regression with hh controls
		xtreg total_production $base_vars $base_controls, fe vce(r)
		outreg2 using "`results_file'", word title("Phase 1 Results") ///
		ct("Total Farm Production") ///
		adjr2 ///
		addstat(R-squared within model,`e(r2_w)', ///
				R-squared overall model, `e(r2_o)', ///             
				R-squared between model, `e(r2_b)') ///
		addtext(Household Controls, NO, Household Fixed Effects, YES, Time Fixed Effects, YES) ///
		addn("Notes: Household controls include caste, religion, type of housing, household facilities and family size") ///
		drop(i.caste_group i.religion family_size building_index i.hh_type_of_house i.caste_group==5 i.religion) ///
		label append 
