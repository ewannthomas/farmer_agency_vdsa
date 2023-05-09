import pandas as pd
import numpy as np
from pathlib import Path
from raw_data_compile import VdsaMicroCompiler



class VdsaMicroReducer(VdsaMicroCompiler):

    """
    This class covers methods created to reduce the dimesionality of datasets to Household ID and Year.
    """

    def __init__(self):
        dir_path=Path.cwd()
        interim_path=dir_path.joinpath('data','interim')

        interim_files_path=interim_path.joinpath('cleaned')

        self.interim_reduced_path=interim_path.joinpath("reduced")

        if not self.interim_reduced_path.exists():
            self.interim_reduced_path.mkdir(parents=True)

        self.files_path=list(interim_files_path.glob("*.csv"))

        self.id_cols=['sur_yr', 'hh_id']
        self.hh_id_cols=['hh_id']

    def path_create(self, tag:str):

        for file in self.files_path:
            if tag==file.stem:
                out_file=self.interim_reduced_path.joinpath(f"{tag}.csv")
                paths_dict={
                    'in_file':file,
                    'out_file':out_file
                }
                return paths_dict
  
    def data_validator(self, df:pd.DataFrame, tag:str):  

        data=pd.DataFrame(df)

        # print(data.columns)
        # print(data.dtypes)


        data = data.set_index(self.hh_id_cols)
        if data.index.is_unique:
            data = data.reset_index()
            print(f"{tag} is ISID")
        else:
            print(f"{tag} Not ISID")
            print("Checking for missing values in the coulmns")

            data = data.reset_index()

            for i in self.hh_id_cols:  # checking presence of missing values in the concerend columns
                if data[i].isna().value_counts()[False] == len(data[i]):
                    print(f"No missing values in {i}")
                else:
                    print(f"Missing values found in {i}")  # didnt find any missing vals until now. If present add fucntion to deal with it

    def id_creator(self, df:pd.DataFrame):

        """
        This method creates the household ID for which is invariable across years. This new ID will enable 'xtset' functionalities in STATA for panel data regression. 
        
        Parameters:
        
        self: Inherits all the path structures defined in __init__.
        df: A pandas dataframe which contains the column hh_id.
        """

        df=pd.DataFrame(df)

        df['hh_id_panel']=df['hh_id'].str.slice(0,3) + df['hh_id'].str.slice(5,10)

        return df

    def tab_values(df:pd.DataFrame, cols:list):

        df=pd.DataFrame(df)

        for col in cols:
            print(f"{col}*******************************")

            print(df[col].value_counts(dropna=False))

    def to_float(self, df:pd.DataFrame, cols:list):

        """
        This function converts the specified columns which inherited their string character into floats.
        Parameters:
        self: Inherits all the self variables.
        df: A pandas dataframe which contains the columns to be converted to float
        cols: A list of columns which are objects and need to be converted to float
        """

        temp_file=self.interim_reduced_path.joinpath('temp.csv')

        for col in cols:

            try:
                    df[col]=df[col].str.replace(" ", "alpha").str.replace("a.*", '', regex=True)
            
            except AttributeError:
                continue

        df.to_csv(temp_file, index=False)

        df=pd.read_csv(temp_file)

        temp_file.unlink()


        return df
     
    def cultivation(self):
        tag="Crop_info_op"

        temp_file=self.interim_reduced_path.joinpath('temp.csv')

        paths_dict=VdsaMicroReducer.path_create(self, tag=tag)

        if not paths_dict['out_file'].exists():

            df=pd.read_csv(paths_dict['in_file'])

            print(df.columns)

            cols=['op_by_prod_qty', 'op_by_prod_rate','op_main_prod_qty', 'op_main_prod_rate', 'op_ot_prod_qty','op_ot_prod_rate']

            for col in cols:

                try:
                        df[col]=df[col].str.replace(" ", "alpha").str.replace("a.*", '', regex=True)
                
                except AttributeError:
                    continue

            df.to_csv(temp_file, index=False)

            df=pd.read_csv(temp_file)


            for col in cols:
                df[col]=df[col].astype(float)

            df['main_prod_value']=df['op_main_prod_qty'] * df['op_main_prod_rate']
            df['by_prod_value']=df['op_by_prod_qty'] * df['op_by_prod_rate']
            df['ot_prod_value']=df['op_ot_prod_qty'] * df['op_ot_prod_rate']

            df['total_production']= df[['main_prod_value','by_prod_value','ot_prod_value']].sum(axis=1, skipna=True)

            # print(df['total_production'].describe())
            # print(df['main_prod_value'].describe())
            # print(df['by_prod_value'].describe())

            # subsetting and aggregating prodcution at yr and hh_id

            df=df.groupby(self.id_cols)['total_production'].sum().reset_index()

            # print(df)

            VdsaMicroReducer.data_validator(self, df=df, tag=tag)

            df=VdsaMicroReducer.id_creator(self, df=df)

            df.to_csv(paths_dict['out_file'], index=False)

            temp_file.unlink()

    def gen_info(self):

        tag="Gen_info"

        paths_dict=VdsaMicroReducer.path_create(self, tag=tag)

        if not paths_dict['out_file'].exists():

            df=pd.read_csv(paths_dict['in_file'])
      
            VdsaMicroReducer.data_validator(self, df=df, tag=tag)

            # cols=['val_resi_plot', 
            # 'no_animals', 
            # 'val_animals', 
            # 'val_farm_impl',
            # 'val_ot_assets', 
            # 'cash_rec', 
            # 'loan_rec', 
            # 'immi_to_vil', 
            # 'place',
            # 'distance']

            # VdsaMicroReducer.tab_values(df=df, cols=cols)

            df=VdsaMicroReducer.id_creator(self, df=df)

            print(df)

            df.to_csv(paths_dict['out_file'], index=False)

    def family_comp(self):
        tag="Family_comp"

        paths_dict=VdsaMicroReducer.path_create(self, tag=tag)

        if not paths_dict['out_file'].exists():

            df=pd.read_csv(paths_dict['in_file'])

            # print(df['hh_id'].nunique())


            cols=[
                'edu_level', 'yrs_edu'
            ]
            # VdsaMicroReducer.tab_values(df=df,cols=cols)

            df=VdsaMicroReducer.to_float(self, df=df, cols=cols)

            # VdsaMicroReducer.tab_values(df=df,cols=cols)


            #creating education level of head of family
            df['head_edu_level']=np.where(df['relation']=='1', df['edu_level'], np.nan)

            #reducing data
            df=df[(df['relation']=='1')][['sur_yr', 'hh_id','head_edu_level']]

            VdsaMicroReducer.data_validator(self,df=df, tag=tag)

            df=VdsaMicroReducer.id_creator(self, df=df)

            df.to_csv(paths_dict['out_file'], index=False)

    def building(self):

        tag="Building"

        paths_dict=VdsaMicroReducer.path_create(self, tag=tag)

        if not paths_dict['out_file'].exists():

            df=pd.read_csv(paths_dict['in_file'])

            df.drop(['region', 'who_owns_buil','remarks'], axis=1, inplace=True)

            #We have a duplicate item in 2010	IBH10A0043	Residential House	OWN. Removing the same   
            df.drop_duplicates(subset=['sur_yr','hh_id', 'item_building'],inplace=True)

            #pivoting the data and doing necessary cleaning
            df=df.pivot(index=['sur_yr','hh_id', ],columns=['item_building'], values='facility').reset_index()

            col_list=list(df.columns)
            col_list_index_subset=col_list[0:2]
            col_list_subset=[str("hh_" + x.lower().replace(" ", "_")) for x in col_list if x not in col_list_index_subset]
            col_list_new=col_list_index_subset + col_list_subset
            df.columns=col_list_new


            #mapping yes, no, 1, 2 answers ina subset of columns to dummmy
            col_list_subset=col_list_subset[1:16]
            print(col_list_subset)
            dummy_map_dict={
                'yes':1,
                'no':0,
                '1':1,
                '2':0,
                '1.0':1,
                '2.0':0
            }
            for col in col_list_subset:

                if col !='hh_residential_house':

                    df[col]=df[col].str.strip().str.lower()
                    # print(df[col].value_counts(dropna=False))
                    df[col]=df[col].map(dummy_map_dict)
                    # print(df[col].value_counts(dropna=False))
                    # print("********************************************")

            #dropping vars with only one valid obs
            df.drop(['hh_telephone', 'hh_radios', 'hh_television', 'hh_cattle_shed'], axis=1, inplace=True)

            #cleaning hh_residential_house column
            df['hh_residential_house']=df['hh_residential_house'].str.strip().str.title()

            #cleaning hh_type_of_house column
            df['hh_type_of_house']=df['hh_type_of_house'].str.strip().str.replace(".0","", regex=False)


            #defining the final buliding index whicvh acts as household control
            
            df=VdsaMicroReducer.to_float(self, df=df, cols=['hh_area_of_courtyard','hh_type_of_house'])

            cols=[ # these values make up the basic facilities and will act as the control for building and welfare or living standard of the household
                'hh_bathroom',
                'hh_cable_tv',
                'hh_cooking_gas',
                'hh_drinking_water_well',
                'hh_electrified',
                'hh_internet_connection',
                'hh_tap_water_connection',
                'hh_toilet'
            ]
            df['building_index']=df[cols].sum(axis=1, skipna=True)

            # #we are trying to add  the type of hh's building. But its categorically arranged such that 1 is better and 5 is bad.
            # #so we are deducting it from
            # df['building_index']=df['building_index']-df['hh_type_of_house']
            # # print(df['building_index'])



            VdsaMicroReducer.data_validator(self, df=df, tag=tag)
            df=VdsaMicroReducer.id_creator(self, df=df)

            # for col in df.columns:
            #     print(col)
            #     print(df[col].unique())

            df.to_csv(paths_dict['out_file'], index=False)

    def cons_durabs(self):

        tag="Consumer_durables"

        paths_dict=VdsaMicroReducer.path_create(self, tag=tag)

        if not paths_dict['out_file'].exists():

            df=pd.read_csv(paths_dict['in_file'])

            df=df.groupby(self.id_cols)['present_value_durable'].sum().reset_index()

            df.rename(columns={
               'present_value_durable':'consumer_durables_present_value'
            }, inplace=True)

            VdsaMicroReducer.data_validator(self,df=df, tag=tag)
            df=VdsaMicroReducer.id_creator(self, df=df)

            df.to_csv(paths_dict['out_file'], index=False)

    def farm_equip(self):

        tag="Farm_Equipment"

        paths_dict=VdsaMicroReducer.path_create(self, tag=tag)

        if not paths_dict['out_file'].exists():

            df=pd.read_csv(paths_dict['in_file'])

            cols=[
               'present_val'
            ]
            # VdsaMicroReducer.tab_values(df=df,cols=cols)

            df=VdsaMicroReducer.to_float(self, df=df, cols=cols)

            df=df.groupby(self.id_cols)['present_val'].sum().reset_index()

            df.rename(columns={
               'present_val':'farm_equipment_present_value'
            }, inplace=True)

            VdsaMicroReducer.data_validator(self,df=df, tag=tag)
            df=VdsaMicroReducer.id_creator(self, df=df)

            df.to_csv(paths_dict['out_file'], index=False)
          
    def fin_assest_liabs(self):

        tag="Fin_assets_liabilities"

        paths_dict=VdsaMicroReducer.path_create(self, tag=tag)

        if not paths_dict['out_file'].exists():

            df=pd.read_csv(paths_dict['in_file'])

            df['category']=df['category'].str.strip().str.lower()

            df=df.groupby(['sur_yr','hh_id','category'])['amount'].sum().reset_index()

            # #pivoting the data and doing necessary cleaning
            df=df.pivot(index=['sur_yr','hh_id', ],columns=['category'], values='amount').reset_index()
            df['total_save']=df[['savings','lendings']].sum(axis=1,skipna=True)
            df['net_financial_position']=df['total_save'].subtract(df['borrowings'], fill_value=0)
            print(df)

            df=df.groupby(self.id_cols)['net_financial_position'].sum().reset_index()

            print(df)

            VdsaMicroReducer.data_validator(self,df=df, tag=tag)
            df=VdsaMicroReducer.id_creator(self, df=df)

            df.to_csv(paths_dict['out_file'], index=False)

    def gender_crop_cult(self):

        """
        This fucntion widens the gender crop cult file to make activity done by each gender a column with the necessary gender as value.
        """
        tag="Gend_crop_cult"

        paths_dict=VdsaMicroReducer.path_create(self, tag=tag)

        if not paths_dict['out_file'].exists():

            df=pd.read_csv(paths_dict['in_file'])

            df=df.melt(id_vars=['sur_yr','hh_id', 'activity'],
                        value_vars=['men', 'women', 'men_women'],
                        var_name='gender',
                        value_name='value')

            df['gender']=np.where(df['gender']=='men_women', "both", df['gender'])
            df['value']=np.where(df['value']!="*","", df['value'])

            df=VdsaMicroReducer.to_float(self, df=df,cols=['value'])

            # print(df['value'].value_counts(dropna=False))
            df.dropna(axis=0, how='any', inplace=True)

            df.drop('value', axis=1, inplace=True)

            df.drop_duplicates(subset=['sur_yr','hh_id', 'activity'], inplace=True)
            df=df.pivot(index=['sur_yr','hh_id'], columns='activity', values='gender').reset_index()

            col_list=list(df.columns)
            col_list_index_subset=col_list[0:2]
            col_list_subset=[str("gend_dec_" + x.strip().lower().replace(" ", "_")) for x in col_list if x not in col_list_index_subset]
            col_list_new=col_list_index_subset + col_list_subset
            df.columns=col_list_new


            VdsaMicroReducer.data_validator(self, df=df, tag=tag)

            df=VdsaMicroReducer.id_creator(self, df=df)

            df.to_csv(paths_dict['out_file'], index=False)

    def govt_dev_progs(self):

        """
        This fucntion aggregates the benefit amount received from the govt.
        """

        #The initial idea was to identify the specific govt transfer programs but becuase of the wide variety of unique programs, we are
        #going ahead with a simple aggregation benefit amount
        tag="Govt_dev_progs_benefits"

        paths_dict=VdsaMicroReducer.path_create(self, tag=tag)

        if not paths_dict['out_file'].exists():

            df=pd.read_csv(paths_dict['in_file'])

            df.rename(columns={
                'amt_ben':'govt_ben_prog_amount_received'
            },inplace=True)


            df=df.groupby(self.id_cols)['govt_ben_prog_amount_received'].sum().reset_index()

            VdsaMicroReducer.data_validator(self, df=df, tag=tag)
            df=VdsaMicroReducer.id_creator(self, df=df)

            df.to_csv(paths_dict['out_file'], index=False)

    def stock_in(self):
        """
        This fucntion aggregates the farm inventory with the household.
        """

        tag="Stock_inv"

        paths_dict=VdsaMicroReducer.path_create(self, tag=tag)

        if not paths_dict['out_file'].exists():

            df=pd.read_csv(paths_dict['in_file'])

            #print(df)

            df=VdsaMicroReducer.to_float(self, df=df, cols=['total_value_stock'])

            df=df.groupby(self.id_cols)['total_value_stock'].sum().reset_index()

            VdsaMicroReducer.data_validator(self, df=df, tag=tag)

            # print(df)

            df=VdsaMicroReducer.id_creator(self, df=df)

            df.to_csv(paths_dict['out_file'], index=False)

    def reliab_ranking(self):
        """
        This fucntion aggregates the reliability rankings provided by the household. Please refer the documentation to understand the contstant value used to reduced the dataset.
        """

        tag="Reliability_ranking"

        paths_dict=VdsaMicroReducer.path_create(self, tag=tag)

        if not paths_dict['out_file'].exists():

            df=pd.read_csv(paths_dict['in_file'])

            df=df.groupby(['sur_yr','hh_id'])['sou_assistance'].count().reset_index()

            df['reliab_ranking']=df['sou_assistance']*(1/23)

            print(df['reliab_ranking'].unique())

            VdsaMicroReducer.data_validator(self, df=df, tag=tag)

            df=VdsaMicroReducer.id_creator(self, df=df)

            df.to_csv(paths_dict['out_file'], index=False)

    def coping_mech(self):
        """
        This fucntion cleans the coping mechanism file for regression.
        """

        tag="Coping_Mech"

        paths_dict=VdsaMicroReducer.path_create(self, tag=tag)

        if not paths_dict['out_file'].exists():

            df=pd.read_csv(paths_dict['in_file'])

            #bringing coping mecjanism from wide to long format
            #the cop_mechs with "other" tag i sommitted for its is random staring
            df_cop_mech=df.melt(id_vars=['sur_yr', 'hh_id', 'problem'],
                        value_vars=["co_mech_m1", "co_mech_m2", "co_mech_m3",
                                    "co_mech_f1", "co_mech_f2", "co_mech_f3"],
                        var_name="cop_mech",
                        value_name='cop_value')
            
            #generating gender identifiers
            conds=[
                df_cop_mech['cop_mech'].isin(["co_mech_m1", "co_mech_m2", "co_mech_m3"]),
                df_cop_mech['cop_mech'].isin(["co_mech_f1", "co_mech_f2", "co_mech_f3"])
            ]

            options=[
                "Male",
                "Female"
            ]

            df_cop_mech['gender']=np.select(conds,options)

            #Process to generate singular values for copping mechanism

            df_cop_mech['cop_value']=df_cop_mech['cop_value'].str.strip().str.replace("-", "")

            df_cop_mech=VdsaMicroReducer.to_float(self, df=df_cop_mech, cols=['cop_value'])

            # #certain duplicates are verified and remived
            # df_cop_mech.drop_duplicates(subset=['sur_yr', 'hh_id','problem'], inplace=True)

            #dropping obs with NaN in cop_value
            df_cop_mech.dropna(subset=['cop_value'],axis=0, inplace=True)

            male_weight_dict={
            	6:0.347666,
                7:0.206869,
                8:0.232564,
                10:0.081542,
                11:0.062926,
                12:0.068432
            }

            female_weight_dict={
                6:0.372003,
                7:0.215489,
                8:0.199611,
                10:0.063189,
                11:0.08814,
                12:0.061568
            }

            df_cop_mech['weights']=np.where(df_cop_mech['gender']=='Male', df_cop_mech['cop_value'].map(male_weight_dict), df_cop_mech['cop_value'].map(female_weight_dict))

            df_cop_mech['weights_product']=df_cop_mech['cop_value']*df_cop_mech['weights']

            df_cop_mech=df_cop_mech.groupby(['sur_yr','hh_id', 'gender']).agg({'cop_mech':'count',
                                                                                     'weights_product':'sum'}).reset_index()

            df_cop_mech['cop_mech_index']=df_cop_mech['cop_mech']*df_cop_mech['weights_product']

            df_cop_mech=df_cop_mech.pivot(index=['sur_yr','hh_id'],
                              columns='gender',
                              values='cop_mech_index').reset_index().rename(columns={
                                                                                        'Female':'female_cop_mech_index',
                                                                                        'Male':'male_cop_mech_index'
                              })

            df=df_cop_mech

            #coping mech contains duplicates at hh_id level. These have been identified and verified to be duplicates and hecne removing
            df=df.drop_duplicates(subset='hh_id')
            
            VdsaMicroReducer.data_validator(self, df=df, tag=tag)     

            df=VdsaMicroReducer.id_creator(self, df=df)

            #print(df[df['sur_yr']==2010]['hh_id'].unique())

            df.to_csv(paths_dict['out_file'], index=False)

           
def main():

    reduce_data=VdsaMicroReducer()
    reduce_data.cultivation()
    reduce_data.gen_info()
    reduce_data.family_comp()
    reduce_data.building()
    reduce_data.cons_durabs()
    reduce_data.farm_equip()
    reduce_data.fin_assest_liabs()
    reduce_data.gender_crop_cult()
    reduce_data.govt_dev_progs()
    reduce_data.stock_in()
    reduce_data.reliab_ranking()
    reduce_data.coping_mech()

if __name__=="__main__":
    main() 


