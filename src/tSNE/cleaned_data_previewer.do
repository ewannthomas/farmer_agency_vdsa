clear


*Defining directories
	local dir "C:\Work ISB\projects\frer"
	local interim_folder "`dir'\data\interim"
	local cleaned_folder "`interim_folder'\cleaned"
	local processed_folder "`interim_folder'\tsne"

	
	
*importing reliab_ranking file
	local tag "Gen_info"
	import delimited using "`processed_folder'\Coping_Mech.csv"
	
	*import delimited using "`processed_folder'\Coping_Mech.csv"


	
	duplicates tag, gen(dups)
tab dups
br if dups>0	