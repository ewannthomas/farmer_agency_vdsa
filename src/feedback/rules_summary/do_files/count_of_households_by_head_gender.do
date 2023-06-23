
clear


*Defining directories

local dir "D:\work_isb\projects\frer"

local interim_folder "`dir'\data\interim"

local long_folder "`interim_folder'\tsne\long_data"

local src "`dir'\src\feedback"

local include_script "`src'\include.do"

local result_folder "`dir'\results\feedback"




*Calling in the panel data cleaning script

	local data_1 "`long_folder'\Family_comp.csv"

	local data_2 "`long_folder'\Gen_info.csv"
	
	

	import delimited using "`data_1'", numericc(5)
	
	
		******Summary statistcis for Writeup
	
			foreach yr in 2010 2011 2012 2013 2014{
			
				local results_file "`result_folder'\count_female_head.xls"
				
				tabout female if relation==1 & sur_yr==`yr' ///
					using "`results_file'", oneway append ///
					c(freq col cum) f(0c 2p 2p) clab(Frequency Percentage Cumulative_Percentage)
			
			}
			
			
		
		
		
		

	
	
