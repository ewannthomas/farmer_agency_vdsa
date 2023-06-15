
clear


*Defining directories

	local dir "D:\work_isb\projects\frer"

	local interim_folder "`dir'\data\interim"

	local stata_files "`interim_folder'\stata_files"

	local long_folder "`interim_folder'\tsne\long_data"

	local src "`dir'\src\feedback"

	local include_script "`src'\include.do"

	local result_folder "`dir'\results\feedback"
	
	local gicc "`stata_files'\gicc.csv"

	
	
	*importing the GIC-C csv file
	
	import delimited "`gicc'"