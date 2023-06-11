clear


*Defining directories
	local dir "D:\work_isb\projects\frer"
	local interim_folder "`dir'\data\interim"
	local cleaned_folder "`interim_folder'\cleaned"
	local reduced_folder "`interim_folder'\reduced"
	local output_folder "`interim_folder'\stata_files"
	local processed_folder "`dir'\data\processed"

	
	
*importing reliab_ranking file
	import delimited "`processed_folder'\panel_regression.csv", numericc(3)

*dropping unnecessary vars after verifying frequency distribution
	drop dry_rate when_head_dry irri_rate val_resi_plot	
	drop no_animals when_head_irri
	drop val_animals val_farm_impl val_ot_assets cash_rec loan_rec
	drop distance main_occp subs_occp how_head how_head_ot when_head

*Renamimg and labelling necessary varibales
	label var male_cop_mech_index "Male Coping Mechanism Index"
	label var female_cop_mech_index "Female Coping Mechanism Index"
	label var farm_equipment_present_value "Present Value of Farm Equipments"
	label var net_financial_position "Net Financial Position of HH"
	label var reliab_ranking "Reliabilty Ranking Index"
	label var total_value_stock "Total Value of Farm Inventory"
	label var govt_ben_prog_amount_received "Benefit Received from Govt"
	label var caste_group "Caste Group"
	label var religion "Religion"
	label var family_size "Family Size"
	label var building_index "Household Facilities Index"
	label var hh_type_of_house "Type of House"
	label var consumer_durables_present_value "Present Value of Consumer Durables Owned"


	
*encoding the hh_id_panel for xtsetting becuase it wont take strings
	encode hh_id_panel, gen(hh_id_encoded)
	label var hh_id_encoded "Unique Households"
	
*encoding string varibales into categoricals to be used in the regression
	local vars village caste_group religion
	foreach var in `vars'{
		encode(`var'), gen(`var'_encoded)
		drop `var'
		rename `var'_encoded `var'
	}
	
	
*reordering dataset
	order sur_yr hh_id hh_id_panel country state district block village caste sub_caste ///
	caste_group religion family_size
	
*assigning 0 in hh_type_of_houe as 1
	replace hh_type_of_house=1 if hh_type_of_house==0
