# VDSA DATA WRANGLING DOCUMENTATION

The Village Dymanics Situation Assessment is a yearly panel dataset collected across 9 states in India between 2010 and 2014.

To replicate the results we generated, please clone the [farmer_agency_vdsa](https://shorturl.at/rV178) git repository. Post repository cloning, one may dowanload the necessary data from the [VDSA data portal](https://vdsa.icrisat.org/vdsa-database.aspx).

General Facts:

- The column `hh_id_panel`, across all data products generated, is the household identifier and column `sur_yr` is the year of enquiry. Entries in these columns help uniquely identify each observation at household-year level resolution.

- Each sub dataset will be identified using the `tag` string where the file name of the dataset would be composed as "<tag>.csv". Please refer the `raw_data_wrangle.md` file to understand the components and features of each sub dataset.

## T-SNE - Interim Data Cleaning

### Prototype 1

### Prototype 2

In the interim data clening process, we expect to apply a blanket column reducer function which identifies the columns in the data which have:

- all entries as missing or `NaN`
- more than 60% missing values aka `NaN`

The datasets will be called from the sub-directory "data/interim/tsne" and the output of the process will be send to "data/preprocessed/tsne/prototype_2".

#### Building

- columns before trim:24
- columns dropped with all NaN:0
- columns dropped with NaN beyond 0.6 threshold:6
- columns post reducing:18

#### Consumer_durables

- columns before trim:52
- columns dropped with all NaN:0
- columns dropped with NaN beyond 0.6 threshold:34
- columns post reducing:18

#### consumption_expenditure

- columns before trim:134
- columns dropped with all NaN:0
- columns dropped with NaN beyond 0.6 threshold:24
- columns post reducing:110

#### Coping_Mech

- columns before trim:317
- columns dropped with all NaN:0
- columns dropped with NaN beyond 0.6 threshold:16
- columns post reducing:301

#### Crop_info_op

- columns before trim:7702
- columns dropped with all NaN:1646
- columns dropped with NaN beyond 0.6 threshold:6054
- columns post reducing:2

#### Cult_ip

- columns before trim:43814
- columns dropped with all NaN:0
- columns dropped with NaN beyond 0.6 threshold:43812
- columns post reducing:2

#### Family_comp

- columns before trim:8322
- columns dropped with all NaN:2364
- columns dropped with NaN beyond 0.6 threshold:5896
- columns post reducing:62

#### Farm_Equipment

- columns before trim:110
- columns dropped with all NaN:19
- columns dropped with NaN beyond 0.6 threshold:85
- columns post reducing:6

#### Fin_assets_liabilities

- columns before trim:647
- columns dropped with all NaN:12
- columns dropped with NaN beyond 0.6 threshold:633
- columns post reducing:2

#### Fin_Trans

- columns before trim:338
- columns dropped with all NaN:0
- columns dropped with NaN beyond 0.6 threshold:312
- columns post reducing:26

#### Gend_crop_cult

- columns before trim:50
- columns dropped with all NaN:0
- columns dropped with NaN beyond 0.6 threshold:31
- columns post reducing:19

#### Gend_decision_making

- columns before trim:336
- columns dropped with all NaN:0
- columns dropped with NaN beyond 0.6 threshold:0
- columns post reducing:336

#### Gen_info

- columns before trim:592
- columns dropped with all NaN:0
- columns dropped with NaN beyond 0.6 threshold:18
- columns post reducing:574

#### Info_ranking

- columns before trim:134
- columns dropped with all NaN:0
- columns dropped with NaN beyond 0.6 threshold:97
- columns post reducing:37

#### Landholding

- columns before trim:8078
- columns dropped with all NaN:842
- columns dropped with NaN beyond 0.6 threshold:2081
- columns post reducing:5155

#### Landholding123

- columns before trim:6327
- columns dropped with all NaN:1574
- columns dropped with NaN beyond 0.6 threshold:4718
- columns post reducing:35

#### Livestock_inv

- columns before trim:62
- columns dropped with all NaN:0
- columns dropped with NaN beyond 0.6 threshold:54
- columns post reducing:8

#### Loans

- columns before trim:398
- columns dropped with all NaN:0
- columns dropped with NaN beyond 0.6 threshold:396
- columns post reducing:2

#### Plotlist

- columns before trim:11345
- columns dropped with all NaN:0
- columns dropped with NaN beyond 0.6 threshold:11343
- columns post reducing:2

#### Prod_Sold

- columns before trim:1103
- columns dropped with all NaN:181
- columns dropped with NaN beyond 0.6 threshold:920
- columns post reducing:2

#### Reliability_ranking

- columns before trim:102
- columns dropped with all NaN:16
- columns dropped with NaN beyond 0.6 threshold:69
- columns post reducing:17

#### Sale_pur

- columns before trim:1158
- columns dropped with all NaN:68
- columns dropped with NaN beyond 0.6 threshold:1088
- columns post reducing:2

#### Stock_inv

- columns before trim:26
- columns dropped with all NaN:0
- columns dropped with NaN beyond 0.6 threshold:6
- columns post reducing:20

#### total_cult_yr

- columns before trim:5
- columns dropped with all NaN:0
- columns dropped with NaN beyond 0.6 threshold:1
- columns post reducing:4
