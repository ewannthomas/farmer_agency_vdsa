# VDSA DATA WRANGLING DOCUMENTATION

The Village Dymanics Situation Assessment is a yearly panel dataset collected across 9 states in India between 2010 and 2014.

To replicate the results we generated, please clone the [farmer_agency_vdsa](https://shorturl.at/rV178) git repository. Post repository cloning, one may dowanload the necessary data from the [VDSA data portal](https://vdsa.icrisat.org/vdsa-database.aspx).

General Facts:

- The column `hh_id`, across all data products generated, is a combination of the household identifier and survey year. Entries in this column uniquely identifies the data atg household year level resolution.

## Panel Data Regression

## tSNE and Deep Learning

Basic wrangling exercises include:

- There are mutiple files stemming from east india and sat india folders. These files are concatenated into a single file for each sub dataset. Each sub dataset being data obtained from source belonging to specific schdeules of the questionnaire.

- Ensuring presence uniform column names for compatible datasets stemming from east-india and sat-india folders.

- Removing columns with all the entires as missing values.

### 1. General Endowments Schedule (GES)

#### Household Information

In this section of the GES schedule, the enumerators collect information which provides an overview of the household, such as location, land owned, lamnd irrigated, demographics, asset position etc. 

After exercising the basic wrangling measures, we identified all the numeric columns which had empty string vlues  like trailing spaces, unencessary spaces among characters or digits. Owing to the presence of these non numeric values, these columns were initially identified and read as string columns by the Pandas `read_excel`fucntion. These columns were converetd to floats. 

Similarly, the string columns were identified and cleansed of trailing spaces and other non alpha numeric values whcih rendered them difficult to interpret. 

The columns `caste, religion` were recoded contained rogue strings, which were either created by errors at the time of information entry by the enumerator while on field or other unidentified sources. These rogue values are problematic when present in string columns which are essentially categorical and as per the schedule, they have fixed set of values which are considered valid. Hence, these rogue string values, whcih sometimes are directly relatable or not, have to mapped to the values or categories mentioned in the schedule. This is achieved either by creating a Python dictionary with the rogue value as the `key` and its corresponding match from the schedule as the `value`. When the numder of rogue strings are relatively low, we define the dictionary within the script itself. However, when the count of rogue strings are large and may possibly wreck the script, a separate JSON file with a suitable name is craeted and called in as a dictionary to perform the mapping exercise. 

#### 1.1 Household Member Schedule (VDSA – C)

The household member schdeule enquires about the dempohgraphic, socio-economic and health features of the members of each agricultural household. The schedule covers, questions on education, occupation, BMR, migration status etc.

After exercising the basic wrangling processes, we checked for duplicates across all columns and removed rows which were exact replica of another. Adding the snapshot of duplicates and their corresponding twins:

| sur_yr | hh_id      | sl_no | ch_stat | ch_stat_ot | relation | relation_ot | gender | age | old_mem_id | pre_mem_id | spouse_m_id | spouse_f_id | child_m_id | child_f_id | mari_stat | mari_stat_ot | marriage_yr | edu_level | edu_level_ot | yrs_edu | yr_edu_ter | rea_stop_edu | rea_stop_edu_ot | main_occp | main_occp_ot | subs_occp | subs_occp_ot | deg_ab | liv_wf_os | os_place  | os_dist | freq_visits | os_purpose | mem_org_name | height | weight | arm_circum | dups |
| ------ | ---------- | ----- | ------- | ---------- | -------- | ----------- | ------ | --- | ---------- | ---------- | ----------- | ----------- | ---------- | ---------- | --------- | ------------ | ----------- | --------- | ------------ | ------- | ---------- | ------------ | --------------- | --------- | ------------ | --------- | ------------ | ------ | --------- | --------- | ------- | ----------- | ---------- | ------------ | ------ | ------ | ---------- | ---- |
| 2012   | IOR12C0038 | 6     | 4       |            | 2        |             | M      | 64  | 6          | 6          |             | 7           |            |            | 1         |              | 1976        | 1         |              | 3       | 1956       | 1            |                 | 11        |              |           |              | 6      | Family    |           |         |             |            |              | 104    | 14.3   |            | TRUE |
| 2012   | IOR12C0038 | 6     | 4       |            | 2        |             | M      | 64  | 6          | 6          |             | 7           |            |            | 1         |              | 1976        | 1         |              | 3       | 1956       | 1            |                 | 11        |              |           |              | 6      | Family    |           |         |             |            |              | 104    | 14.3   |            | TRUE |
| 2014   | IBH14D0058 | 9     | 9       |            |          |             |        |     |            |            |             |             |            |            |           |              |             |           |              |         |            |              |                 |           |              |           |              |        |           |           |         |             |            |              |        |        |            | TRUE |
| 2014   | IBH14D0058 | 10    | 9       |            |          |             |        |     |            |            |             |             |            |            |           |              |             |           |              |         |            |              |                 |           |              |           |              |        |           |           |         |             |            |              |        |        |            | TRUE |
| 2014   | IBH14D0058 | 9     | 9       |            |          |             |        |     |            |            |             |             |            |            |           |              |             |           |              |         |            |              |                 |           |              |           |              |        |           |           |         |             |            |              |        |        |            | TRUE |
| 2014   | IBH14D0058 | 10    | 9       |            |          |             |        |     |            |            |             |             |            |            |           |              |             |           |              |         |            |              |                 |           |              |           |              |        |           |           |         |             |            |              |        |        |            | TRUE |
| 2014   | IBH14D0090 | 7     | 0       |            | 9        |             | M      | 7   | 503        | 503        |             |             | 500        | 501        | 2         |              |             | 1         |              | 2       |            |              |                 | 9         |              |           |              | 5      | Outside   | FARIDABAD | 1500    | 5           | Occasion   |              |        |        |            | TRUE |
| 2014   | IBH14D0090 | 7     | 0       |            | 9        |             | M      | 7   | 503        | 503        |             |             | 500        | 501        | 2         |              |             | 1         |              | 2       |            |              |                 | 9         |              |           |              | 5      | Outside   | FARIDABAD | 1500    | 5           | Occasion   |              |        |        |            | TRUE |

Later, we have identified that in this dataframe, the columns `hh_id`, `sl_no` and `ch_stat` should uniquely identify the rows where the second \(`sl_no`\) identifies the household member and third identifies any chnages in housheold status of the same member defined by the second. On the basis of the above columns we were able to identify the following duplicate entries in the data:
| sur_yr | hh_id | sl_no | ch_stat | ch_stat_ot | relation | relation_ot | gender | age | old_mem_id | pre_mem_id | spouse_m_id | spouse_f_id | child_m_id | child_f_id | mari_stat | mari_stat_ot | marriage_yr | edu_level | edu_level_ot | yrs_edu | yr_edu_ter | rea_stop_edu | rea_stop_edu_ot | main_occp | main_occp_ot | subs_occp | subs_occp_ot | deg_ab | liv_wf_os | os_place | os_dist | freq_visits | os_purpose | mem_org_name | height | weight | arm_circum | dups |
|--------|------------|-------|---------|------------|----------|----------------------|--------|-----|------------|------------|-------------|-------------|------------|------------|-----------|--------------|-------------|-----------|----------------------|---------|------------|--------------|----------------------|-----------|----------------------|-----------|----------------------|--------|-----------|-----------------|---------|-------------|----------------------|--------------------------------|--------|--------|------------|------|
| 2012 | IBH12C0046 | 5 | 0 | | 10 | | F | 2 | 5 | 5 | | | 3 | 4 | 2 | | | 0 | | 0 | | | | 11 | | | | 6 | Family | | | | | | | | | TRUE |
| 2012 | IBH12C0046 | 5 | 0 | | 10 | | F | 3 | 5 | 5 | | | 3 | 4 | 2 | | | 0 | | 0 | | | | 11 | | | | 6 | Family | | | | | | | | | TRUE |
| 2014 | IBH14C0057 | 5 | 1 | | | | F | | | | | | 1 | 2 | 2 | | | | | | | | | | | | | | | | | | | | | | | TRUE |
| 2014 | IBH14C0057 | 5 | 1 | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | TRUE |
| 2014 | IBH14D0010 | 3 | 1 | | | | F | | | | | | | 2 | 2 | | | | | | | | | | | | | | | | | | | | | | | TRUE |
| 2014 | IBH14D0010 | 3 | 1 | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | TRUE |
| 2011 | IJH11C0004 | 1 | 0 | | 4 | | M | 46 | | 1 | | 2 | | | 1 | | 1990 | 0 | | 0 | | | | 1 | | 3 | | 1 | Family | | | | | | | | | TRUE |
| 2011 | IJH11C0004 | 1 | 0 | | 1 | | F | 41 | 2 | 2 | | | | | 3 | | 1987 | 0 | | 0 | | | | 3 | | 10 | | 1 | Family | | | | | | 143.8 | 39.8 | 24 | TRUE |
| 2012 | IOR12C0042 | 3 | 0 | | 10 | | F | 15 | 3 | 3 | | | | 2 | 2 | | | 3 | | 10 | 2012 | 1 | | 10 | | | | 3 | Family | | | | | | 156 | 50.8 | 23.8 | TRUE |
| 2013 | IOR12C0042 | 3 | 0 | | 10 | | F | 16 | 3 | 3 | | | | 2 | 2 | | | 3 | | 10 | 2012 | 1 | | 10 | | | | 3 | Family | | | | | | 156 | 50.8 | 23.8 | TRUE |
| 2012 | IOR13B0202 | 3 | 0 | | 5 | | M | 1 | 3 | 3 | | | 1 | 2 | 2 | | | 0 | | 0 | | | | 11 | | | | 6 | Family | | | | | | | | | TRUE |
| 2013 | IOR13B0202 | 3 | 0 | | 5 | | M | 2 | 3 | 3 | | | 1 | 2 | 2 | | | 0 | | 0 | | | | 11 | | | | 6 | Family | | | | | | | | | TRUE |

It is observed that households `IBH14C0057` and `IBH14D0010` have information repeating but in the second row, majoprity of the columns are missing. Hence retaining row 1 for both the households. For households, `IBH12C0046`,`IOR12C0042` and `IOR13B0202` one may notice two things, all information is similar except for age, where age in row is incremented by 1 in row 2. Assuming that this is a data entry issue, we will be retaining the latest age level information. All these households were inspected to see if the entries were indeed duplicates or an error to the enumerator in filling same `sl_no` value to two seperate individuals in the household. An enquiry in the same lines brings us to our last and final duplicate entry in household `IJH11C0004`. In this household `sl_no` value 1 was given to two seperate individuals, a male and female member of the same family. They exhibit different values in different columns. Hence the male member was recoded as `sl_no` 4.

The column `gender` was recoded to a dummy variable where all male entries were recoded to 0 and female entires to 1. The column was later renamed to `female`. Similarly the column `liv_wit_oth` has been recoded to make the string `family` to say `with_family`.

#### 1.2 Landholding information (VDSA – D)

The landholding information schedule of the GES questionnaire enquires about information on who owns the land and unique identifiers for the plots. It identifies the various sources from whcih each plot is irrigated, soil depth, soil type, revenue from the land etc. The schdeule provides very exhaustive information on the soil conditions and land type of the plot. The identifiers used, `plot_code` is equivalent to the identifier used in the Plotlist and Cropping Patterns questionnaire of VDSA. So, the values are comparable.

The duplicates were checked on columns `hh_id`, `sl_no`, and `plot_code`. There were no duplicates.
Later, all columns which had numeric values were converted to float data type. Teh column `plot_name` was removed because `plot_code` enabled identification of the rows uniquely. Columns on ownership status, change of ownership status, source of irrigation, soil type, fertility and degradation, bunding and bunding type were reassigned to their corrsponding string based vategory values as in the questionnaire. Columns which housed values beyond any defined category of any column was enetered as col_name_others. Such other column which had string values were removed fromthe datastet. e.g.: bund_type_others

#### 1.3 Animal inventory of the Household (VDSA – E)

The animal inventory schedule of the GES questionnaire collects details about the kind, count, mode of acquisition and present value of livestock inventory owned by the household.

After exercising the basic wrangling measures, we inspected for duplicates across all columns in the dataset and found 2 entries,
| sur_yr | hh_id | livestock_type | livestock_count | no_of_rea | no_pur | no_rec_gift | no_sha_rea | livestock_present_value | remarks | dups |
|--------|------------|----------------|-----------------|-----------|--------|-------------|------------|-------------------------|---------|------|
| 2011 | IJH11C0037 | goats | 2 | 2 | | | | 1200 | | TRUE |
| 2011 | IJH11C0037 | goats | 2 | 2 | | | | 1200 | | TRUE |

One entry was removed to ensure unique identification of dataframe. Necessary column name renaming was done to make better sense of the column names.

The column `livestock_type` holding categories of livestock types had rogue string values which were recoded to reflect the categories mentioned in the questionnaire. Post mapping of categorical string values, the dataframe was grouped on the basis of household and livestock type columns \(`hh_id, livestock_type`\) and a sum of the subsequent count columns of livestock were obtained. Prior to grouping and summing all columns with numeric values `present_val, on_farm_reared_count, purchased_count, received_gift_count, shared_rearing_count` were necessarily converted to float data type.

#### 1.4 Farm implements owned by the household (VDSA – F)

The farm implements block of the GES questionnaiore is dedicated towards understanding the quantity, scale and use of various farm implements used by the household in its agricultural activities.

The basic wrangling measures were followed by recoding of the `item_name` column which lists the name of the farm equipment owned by the household. The following are the major categories of farm equipments:

- Desi plough
- Modern plough
- Blade harrow
- Blade hoe
- Seed drill
- Sprinkler set
- Drip irrigation
- Manual sprayers dusters
- Power sprayer duster
- Chaff cutter
- Sugarcane crusher
- Rice huller
- Flour mill
- Power-tiller
- Tractor
- Submersible pump
- Bullock cart
- Truck
- Other minor implements
- Other heavy implements
- Mechanical thresher
- Electric motor
- Diesel pump
- Pipeline in feet
- Combined harvester cum thresher
- Implements used for caste occupation
- Implements used for handy- craft
- Groundnut opener
- Bore-well or Open-well
- Others

However, the data contained around 237 rogue categories whcih varied widely in terms of string, spellings etc. All such rogue values were carefully checked and mapped to one of the values in the above list. The mapper employed to achive the recode of these values is available at [farm_equip_map.json]()

The category mapping was followed by widening of the dataset. There are multiple households which own many number of the same equipment, some fully owned by the household and some shared at a percent of stake, as reported in the `prct_share` column. So these multiple number of the equipments at different stake act as duplicates of eachother. To resolve this we can make use of the `farm_equipment_present_value` column which, as per the documnetation, is the reported value of the implement as per the stake in the ownership. So to widen the dataset, the `prct_share` column can be ignored and the same equipments can be aggregated in terms of the number and its present value. For the column, `horse_power` recorded only for major machinery like tractor, thresher, and pumpset, we take the maximum value within the `item_name` category.

#### 1.5 Building & consumer durables (VDSA – G)

The Building and consumer durables schedule under the GES questionnaire collects information on the building type owned by the household and details about the facilities available in the house. The facilities included the house involves the durables owned by the household. Data cleaning pertaining to this schedule has been, for ease of work, split into:

- Consumer Durables: Deals specifically with the count, present value of the durables owned by the household.
- Buildings: Deals specifically with the details of the house owned, the type of house and amenities built into the house.

##### 1.5.1 Consumer Durables

The basic wrangling exercises were implemented and the column names were renamed for clarity.

While checking for duplicate entires in the dataset by considering all columns in the dataset, we observed that 2308 values were tagged as duplicates. A sub sample of 50 observations from this duplicate sare presented here for reference:

| sur_yr | hh_id      | item_name        | item_qty | present_value_durable | who_owns_durable | dups |
| ------ | ---------- | ---------------- | -------- | --------------------- | ---------------- | ---- |
| 2014   | IAP14C0059 | Furniture        |          | 2400                  |                  | TRUE |
| 2014   | IAP14C0059 | Furniture        |          | 2400                  |                  | TRUE |
| 2012   | IOR12A0001 | Cattle Shed      | 1        | 3000                  | 1                | TRUE |
| 2012   | IOR12A0001 | Cooking Utensils |          | 6000                  |                  | TRUE |
| 2012   | IOR12A0001 | Furniture        |          | 23000                 |                  | TRUE |
| 2012   | IOR12A0001 | Bicycle          | 1        | 1500                  |                  | TRUE |
| 2012   | IOR12A0001 | Cattle Shed      | 1        | 3000                  | 1                | TRUE |
| 2012   | IOR12A0001 | Cooking Utensils |          | 6000                  |                  | TRUE |
| 2012   | IOR12A0001 | Furniture        |          | 23000                 |                  | TRUE |
| 2012   | IOR12A0001 | Bicycle          | 1        | 1500                  |                  | TRUE |
| 2012   | IOR12A0002 | Cattle Shed      | 1        | 500                   | 1                | TRUE |
| 2012   | IOR12A0002 | Cooking Utensils |          | 1000                  |                  | TRUE |
| 2012   | IOR12A0002 | Cattle Shed      | 1        | 500                   | 1                | TRUE |
| 2012   | IOR12A0002 | Cooking Utensils |          | 1000                  |                  | TRUE |
| 2012   | IOR12A0003 | Cattle Shed      | 1        | 5000                  | 1                | TRUE |
| 2012   | IOR12A0003 | Television       | 1        | 3000                  |                  | TRUE |
| 2012   | IOR12A0003 | Cooking Utensils |          | 7000                  |                  | TRUE |
| 2012   | IOR12A0003 | Furniture        |          | 300                   |                  | TRUE |
| 2012   | IOR12A0003 | Fan              | 1        | 1000                  |                  | TRUE |
| 2012   | IOR12A0003 | Bicycle          | 1        | 2000                  |                  | TRUE |
| 2012   | IOR12A0003 | Cattle Shed      | 1        | 5000                  | 1                | TRUE |
| 2012   | IOR12A0003 | Television       | 1        | 3000                  |                  | TRUE |
| 2012   | IOR12A0003 | Cooking Utensils |          | 7000                  |                  | TRUE |
| 2012   | IOR12A0003 | Furniture        |          | 300                   |                  | TRUE |
| 2012   | IOR12A0003 | Fan              | 1        | 1000                  |                  | TRUE |
| 2012   | IOR12A0003 | Bicycle          | 1        | 2000                  |                  | TRUE |
| 2012   | IOR12A0004 | Cooking Utensils |          | 3000                  |                  | TRUE |
| 2012   | IOR12A0004 | Furniture        |          | 15000                 |                  | TRUE |
| 2012   | IOR12A0004 | Bicycle          | 1        | 1500                  |                  | TRUE |
| 2012   | IOR12A0004 | Cooking Utensils |          | 3000                  |                  | TRUE |
| 2012   | IOR12A0004 | Furniture        |          | 15000                 |                  | TRUE |
| 2012   | IOR12A0004 | Bicycle          | 1        | 1500                  |                  | TRUE |
| 2012   | IOR12A0005 | Cooking Utensils |          | 500                   |                  | TRUE |
| 2012   | IOR12A0005 | Furniture        |          | 2000                  |                  | TRUE |
| 2012   | IOR12A0005 | Cooking Utensils |          | 500                   |                  | TRUE |
| 2012   | IOR12A0005 | Furniture        |          | 2000                  |                  | TRUE |
| 2012   | IOR12A0006 | Cooking Utensils |          | 1000                  |                  | TRUE |
| 2012   | IOR12A0006 | Furniture        |          | 4500                  |                  | TRUE |
| 2012   | IOR12A0006 | Bicycle          | 1        | 1500                  |                  | TRUE |
| 2012   | IOR12A0006 | Cooking Utensils |          | 1000                  |                  | TRUE |
| 2012   | IOR12A0006 | Furniture        |          | 4500                  |                  | TRUE |
| 2012   | IOR12A0006 | Bicycle          | 1        | 1500                  |                  | TRUE |
| 2012   | IOR12A0007 | Cooking Utensils |          | 1300                  |                  | TRUE |
| 2012   | IOR12A0007 | Furniture        |          | 600                   |                  | TRUE |
| 2012   | IOR12A0007 | Cooking Utensils |          | 1300                  |                  | TRUE |
| 2012   | IOR12A0007 | Furniture        |          | 600                   |                  | TRUE |
| 2012   | IOR12A0008 | Cattle Shed      | 1        | 2000                  | 1                | TRUE |
| 2012   | IOR12A0008 | Cooking Utensils |          | 3000                  |                  | TRUE |
| 2012   | IOR12A0008 | `Furniture       |          | 6000                  |                  | TRUE |
| 2012   | IOR12A0008 | Watches          | 1        | 100                   |                  | TRUE |

After inspecting multiple values amongst the duplicate rows, we tend to believe that its difficult conclude that these values are duplicates becuase teh same household can necessarily two different items with the same value that they can assign to a general category, for example, like "Furniture". So the approach is consider these observations as valid entries and sum them up at household and item name level.

Inorder to groupby and sum over `hh_id` and `item_name`, the categorical values in `item_name` were cleanned. There were around 177 rogue string values. These values have been recoded to reflect the values provided in the questionnaire. The mapper file used ia available at [consumer_durables_name_map.json]()

Post name mapping, the values were grouped, aggregated and widened to give the final dataset.

##### 1.5.2 Buildings

In the buildings data, SAT and East India have different layouts. SAT India follows the long format where the features of the household is mentioned undeer the column `item_building` and the its presence or value or ownership (depending on the amenity) is mentioned in the `facility` column. However, for East India, the columns are in wide format with values across columns `facility_pre,	own_rented, house_type, courtyard_pre`. Inorder to make both the datasets compatible to eachother, we undertook the following measures after performing the basic wrangling:

- Cleaned and made the strings in column `item_building` unique.
- Isolated the values of above mentioned columns in east India, pivotted the same and assigned it to the `facility` column. This will make both SAT and East India data look identical.
- Now both sets are in long form and this was achieved without splitting the data into two but by making use of a region identifier column `region` which was only created temporarily for only buildings data.
- The columns from East India data was then removed from the final data to avoid duplication of information.

Similarly, the value of the building was also provided as a column. We have to add this column into the `item_building` column and its value to the `facility` column because when we widen the dataframe, all the categories of `item_building` will become column and their repsective values in `facility` will be pivotted at column values. So it is imperativ ethat building be also added as category under `item_building`. This was achioeve dby isolating the households its respective building value into a new datatset and appending the same to the existing dataset. Post which, the `building_value` column of the appended dataset was removed to avoid the above mentioned issue with data widening.

Moreover, there were no duplicates across all the columns. But when checked across columns `hh_id, item_building` we found the following duplicate amd was removed:
| sur_yr | hh_id | item_building | facility | dups |
|--------|------------|-------------------|----------|------|
| 2010 | IBH10A0043 | Residential House | OWN | TRUE |
| 2010 | IBH10A0043 | Residential House | OWN | TRUE |

The data was then widened for further prcessing.

#### 1.6 Stock inventory (VDSA – N)

The stock inventory schedule of the GES questionnaire enquires about the quantity, unit price and total value of the inventory kept with the household. The inventory is split into the follwoing broader categories: Cereals, Pulses, Oilseeds, Other items, Fodders, Cattle Feed, Cooking Fuel and Inputs.

Afte performing the basic wrangling measures, we check for duplicates in the within the dataset. We found 10 observations with dupllicates and the necessary acxtion has been taken to remove them. Adding duplicates here for reference:
| sur_yr | hh_id | stock_category | item_stock | unit_stock | qty_stock | unit_price_stock | total_value_stock | dups |
|--------|------------|--------------------|----------------------------|------------|-----------|------------------|-------------------|------|
| 2012 | IAP12C0007 | Cereals | Finger millet | Kg | 50 | 15 | 750 | TRUE |
| 2012 | IAP12C0007 | Cereals | Rice | Kg | 160 | 26 | 4160 | TRUE |
| 2012 | IAP12C0007 | Cereals | Finger millet | Kg | 50 | 15 | 750 | TRUE |
| 2012 | IAP12C0007 | Cereals | Rice | Kg | 160 | 26 | 4160 | TRUE |
| 2013 | IBH13A0034 | Oil seeds | Refined Oil/Vanaspati Ghee | Kg | 1 | 90 | 90 | TRUE |
| 2013 | IBH13A0034 | Oil seeds | Refined Oil/Vanaspati Ghee | Kg | 1 | 90 | 90 | TRUE |
| 2013 | IJH13D0010 | Pulses | Lentil (Masoor) | Kg | 0.5 | 50 | 25 | TRUE |
| 2013 | IJH13D0010 | Pulses | Lentil (Masoor) | Kg | 0.5 | 50 | 25 | TRUE |
| 2014 | IBH14B0003 | Cooking | Dung cake | Kg | 100 | 3 | 300 | TRUE |
| 2014 | IBH14B0003 | Cooking | Dung cake | Kg | 100 | 3 | 300 | TRUE |

We will not consider the name of each item, instead will try to redue the data to the previously mentioned broad categories of items. Hence `stock_category` column was remapped to match the categories, mentioned earlier, in the questionnaire \(respective mapper is available in the script\). The columns `qty_stock, unit_price_stock, total_value_stock` whcih contained numeric values were converted to float data type. Then the dataset was converted to wide data form for further processing.

#### 1.7 Debt and Credit Schedule (VDSA – P)

After performing the basic wrangling, the categoies of the `source` column has been identified to be 176. These rogue categories have been recoded into the categories as per the questionnaire \(respective mapper is available in the script\). They are:

- Co-operative banks
- Commercial banks
- Grameen bank (RRB)
- Friends & relatives
- Finance companies
- Employer
- Landlord
- Shopkeeper
- Moneylender
- Self-help groups
- Commission agent
- Input supplier
- Others

Similarly the `purpose` column was numeric. We have extracted the corresponding string values from the questionnaire and mapped them.

After mapping the categories, we identified certain cases where the same household was taking as loan or saving different amounts from the same source for the same purpose. There were 555 such entries in the data and they were grouped at a household, source and purpose level. Such grouped cases were aggregated (intra group) after estimating a blended interest for the respective amounts. Regarding the duration of such entries, the maximum duration, within group, of saving or loan among such entires were extrapolated.

#### 1.8 Role of gender

The role of gender schedule of the GES questionnaire collects information from both women and men of the household abou their involvement in the decision making process of the household. It's divided into two sub sections:

##### 1.8.1 Resource ownership and decision-making

Under this section, men and women of the household responds to questions about who owns the assets of the household, who makes the collective decision of the household and who influences the utilization and management of the assets and resources of the household.

After exercising the basic wrangling measures, there exists 2 problems with the data:

- Issue 1: While concatenating multiple sub datasets from east india and sat india folders, some datasets have information split into the following columns \(actuals\): `ownership, deci_making, who_infl_util`. These column have values as `Male`, `Female` and `Both`. However, some other subsets hold their information in columns \(suffix columns\):`ownership_m,	ownership_f,	deci_making_f, who_infl_util_m, who_infl_util_f` where the same information \(pertaining various other states\) is split into male, and female based results, indicated by the suffix \_m and \_f in the column names. Since, the suffix columns and actuals belong to different states, they are mutually exclusive. Hence, steps where taken to ensure that responses indicated in these columns are compiled together in 3 separate columns mentioned as actuals.

- Issue 2: Notice the suffix splitting responses into male and female responses. In all the cases, these responses are the same in both male and female column. Also, there are cases where male column will be empty but female column will have a valid resposnes. So we extrapolated the response in the female column to the male column. Post resolving Issue 2, which Issue 1 was resolved.

After resolving both of these issues, the male and female columns were removed for all distinct repsonses in those columns were mapped to the actuals which will carry the entire weight of the dataset.

Then the column `resources` were cleaned off of rogue string values to reflect the categories provided in the questionnaire. Now that the string values are cleansed, a duplicate check on the data across columns `hh_id, reso_category, resource`, the later two corresoponding to the resource category and resource ownded by the household found 37 duplicate observations. Those are:
| sur_yr | hh_id | reso_category | resource | ownership | deci_making | who_infl_util | dups |
|--------|------------|---------------|---------------------------------|-----------|-------------|---------------|------|
| 2012 | IJH12A0058 | assets | land | Male | Both | Both | TRUE |
| 2012 | IJH12A0058 | assets | land | Male | Both | Both | TRUE |
| 2012 | IBH12D0057 | assets | land | Male | Male | Male | TRUE |
| 2012 | IBH12D0057 | assets | land | Male | Male | Male | TRUE |
| 2014 | IOR14C0010 | assets | machinery | | | | TRUE |
| 2014 | IOR14C0010 | assets | investment | | | | TRUE |
| 2014 | IOR14C0010 | inputs | fertilizers | | | | TRUE |
| 2014 | IOR14C0010 | inputs | pesticides | | | | TRUE |
| 2014 | IOR14C0010 | others | women stepping out of the house | | Female | Female | TRUE |
| 2014 | IOR14B0010 | assets | land | Male | Male | Male | TRUE |
| 2014 | IOR14B0010 | assets | livestock | | | | TRUE |
| 2014 | IOR14B0010 | assets | credit | Male | Male | Male | TRUE |
| 2014 | IOR14B0010 | assets | investment | Male | Male | Male | TRUE |
| 2014 | IOR14B0010 | outputs | crop main production | Male | Male | Male | TRUE |
| 2014 | IOR14B0010 | outputs | sale quantity | Male | Male | Male | TRUE |
| 2014 | IOR14B0010 | assets | land | Male | Male | Male | TRUE |
| 2014 | IOR14B0010 | assets | livestock | | | | TRUE |
| 2014 | IOR14B0010 | assets | credit | Male | Male | Male | TRUE |
| 2014 | IOR14D0010 | inputs | seeds | Male | Male | Male | TRUE |
| 2014 | IOR14D0010 | inputs | fertilizers | Male | Male | Male | TRUE |
| 2014 | IOR14D0010 | inputs | seeds | Male | Male | Male | TRUE |
| 2014 | IOR14D0010 | inputs | fertilizers | Male | Male | Male | TRUE |
| 2014 | IOR14A0010 | others | household maintenance | | Both | Both | TRUE |
| 2014 | IOR14A0010 | others | whom to give vote | | Male | Male | TRUE |
| 2014 | IOR14C0010 | assets | machinery | | | | TRUE |
| 2014 | IOR14C0010 | assets | investment | | | | TRUE |
| 2014 | IOR14C0010 | inputs | fertilizers | | | | TRUE |
| 2014 | IOR14C0010 | inputs | pesticides | | | | TRUE |
| 2014 | IOR14C0010 | others | women stepping out of the house | | Female | Female | TRUE |
| 2014 | IOR14B0010 | assets | land | Male | Male | Male | TRUE |
| 2014 | IOR14B0010 | assets | livestock | | | | TRUE |
| 2014 | IOR14B0010 | assets | credit | Male | Male | Male | TRUE |
| 2014 | IOR14B0010 | assets | investment | Male | Male | Male | TRUE |
| 2014 | IOR14B0010 | outputs | crop main production | Male | Male | Male | TRUE |
| 2014 | IOR14B0010 | outputs | sale quantity | Male | Male | Male | TRUE |
| 2014 | IOR14A0010 | others | household maintenance | | Both | Both | TRUE |
| 2014 | IOR14A0010 | others | whom to give vote | | Male | Male | TRUE |

From the table above, we observe 33 values stemming from the household `IOR14C0010`. Every alternate entry is a duplicate of the entry before it. Hence, these duplicates were removed and the dataset was widened for further processing.

##### 1.8.2 Role of gender in crop cultivation

Under this section, men and women of the household responds to questions about who conducts activities related to cultivation and post cultivation of crops. The schedule identifies activities done solely and jointly by men and women.

After conducting the basic data wrangling, one may notice that the resposnes of housheolds to each activity is marked by an \* in the columns `men, women, men_women` to identify as to who conducts the same.

Before reassigning the \*, the `activity` describing the activity undertaken by the household was cleaned to better reflect the categories mentioned in the questionnaire. In the duplication check across all columns, the following 84 entires were identifed:
| sur*yr | hh_id | activity | men | women | men_women | dups |
|--------|------------|----------------------------------|-----|-------|-----------|------|
| 2014 | IBH14B0090 | selection_of_crop | * | | | TRUE |
| 2014 | IBH14B0090 | selection*of_crop | * | | | TRUE |
| 2014 | IBH14D0200 | selection*of_crop | | | * | TRUE |
| 2014 | IBH14D0200 | selection*of_crop | | | * | TRUE |
| 2014 | IOR14D0054 | harvesting | _ | | | TRUE |
| 2014 | IOR14D0054 | harvesting | _ | | | TRUE |
| 2014 | IOR14D0054 | marketing | _ | | | TRUE |
| 2014 | IOR14D0054 | marketing | _ | | | TRUE |
| 2014 | IOR14D0054 | threshing | _ | | | TRUE |
| 2014 | IOR14D0054 | threshing | _ | | | TRUE |
| 2014 | IOR14D0055 | harvesting | _ | | | TRUE |
| 2014 | IOR14D0055 | harvesting | _ | | | TRUE |
| 2014 | IOR14D0055 | interculture | _ | | | TRUE |
| 2014 | IOR14D0055 | interculture | _ | | | TRUE |
| 2014 | IOR14D0055 | marketing | _ | | | TRUE |
| 2014 | IOR14D0055 | marketing | _ | | | TRUE |
| 2014 | IOR14D0055 | threshing | _ | | | TRUE |
| 2014 | IOR14D0055 | threshing | _ | | | TRUE |
| 2014 | IOR14D0055 | watching | _ | | | TRUE |
| 2014 | IOR14D0055 | watching | _ | | | TRUE |
| 2014 | IOR14D0056 | irrigation | _ | | | TRUE |
| 2014 | IOR14D0056 | irrigation | _ | | | TRUE |
| 2014 | IOR14D0056 | land*preparation | * | | | TRUE |
| 2014 | IOR14D0056 | land*preparation | * | | | TRUE |
| 2014 | IOR14D0056 | transplanting | _ | | | TRUE |
| 2014 | IOR14D0056 | transplanting | _ | | | TRUE |
| 2014 | IOR14D0057 | chemical*fertilizer_application | * | | | TRUE |
| 2014 | IOR14D0057 | chemical*fertilizer_application | * | | | TRUE |
| 2014 | IOR14D0057 | hand*weeding | * | | | TRUE |
| 2014 | IOR14D0057 | hand*weeding | * | | | TRUE |
| 2014 | IOR14D0057 | harvesting | _ | | | TRUE |
| 2014 | IOR14D0057 | harvesting | _ | | | TRUE |
| 2014 | IOR14D0057 | interculture | _ | | | TRUE |
| 2014 | IOR14D0057 | interculture | _ | | | TRUE |
| 2014 | IOR14D0057 | irrigation | _ | | | TRUE |
| 2014 | IOR14D0057 | irrigation | _ | | | TRUE |
| 2014 | IOR14D0057 | land*preparation | * | | | TRUE |
| 2014 | IOR14D0057 | land*preparation | * | | | TRUE |
| 2014 | IOR14D0057 | marketing | _ | | | TRUE |
| 2014 | IOR14D0057 | marketing | _ | | | TRUE |
| 2014 | IOR14D0057 | plant*protection_measures | * | | | TRUE |
| 2014 | IOR14D0057 | plant*protection_measures | * | | | TRUE |
| 2014 | IOR14D0057 | selection*of_crop | * | | | TRUE |
| 2014 | IOR14D0057 | selection*of_crop | * | | | TRUE |
| 2014 | IOR14D0057 | selection*of_variety | * | | | TRUE |
| 2014 | IOR14D0057 | selection*of_variety | * | | | TRUE |
| 2014 | IOR14D0057 | sowing*seed | * | | | TRUE |
| 2014 | IOR14D0057 | sowing*seed | * | | | TRUE |
| 2014 | IOR14D0057 | threshing | _ | | | TRUE |
| 2014 | IOR14D0057 | threshing | _ | | | TRUE |
| 2014 | IOR14D0057 | transplanting | _ | | | TRUE |
| 2014 | IOR14D0057 | transplanting | _ | | | TRUE |
| 2014 | IOR14D0057 | transport*of_fym_and_application | * | | | TRUE |
| 2014 | IOR14D0057 | transport*of_fym_and_application | * | | | TRUE |
| 2014 | IOR14D0057 | watching | _ | | | TRUE |
| 2014 | IOR14D0057 | watching | _ | | | TRUE |
| 2014 | IOR14D0058 | chemical*fertilizer_application | * | | | TRUE |
| 2014 | IOR14D0058 | chemical*fertilizer_application | * | | | TRUE |
| 2014 | IOR14D0058 | hand*weeding | * | | | TRUE |
| 2014 | IOR14D0058 | hand*weeding | * | | | TRUE |
| 2014 | IOR14D0058 | harvesting | _ | | | TRUE |
| 2014 | IOR14D0058 | harvesting | _ | | | TRUE |
| 2014 | IOR14D0058 | interculture | _ | | | TRUE |
| 2014 | IOR14D0058 | interculture | _ | | | TRUE |
| 2014 | IOR14D0058 | irrigation | _ | | | TRUE |
| 2014 | IOR14D0058 | irrigation | _ | | | TRUE |
| 2014 | IOR14D0058 | land*preparation | * | | | TRUE |
| 2014 | IOR14D0058 | land*preparation | * | | | TRUE |
| 2014 | IOR14D0058 | marketing | _ | | | TRUE |
| 2014 | IOR14D0058 | marketing | _ | | | TRUE |
| 2014 | IOR14D0058 | plant*protection_measures | * | | | TRUE |
| 2014 | IOR14D0058 | plant*protection_measures | * | | | TRUE |
| 2014 | IOR14D0058 | selection*of_crop | * | | | TRUE |
| 2014 | IOR14D0058 | selection*of_crop | * | | | TRUE |
| 2014 | IOR14D0058 | selection*of_variety | * | | | TRUE |
| 2014 | IOR14D0058 | selection*of_variety | * | | | TRUE |
| 2014 | IOR14D0058 | sowing*seed | * | | | TRUE |
| 2014 | IOR14D0058 | sowing*seed | * | | | TRUE |
| 2014 | IOR14D0058 | transplanting | _ | | | TRUE |
| 2014 | IOR14D0058 | transplanting | _ | | | TRUE |
| 2014 | IOR14D0058 | transport*of_fym_and_application | * | | | TRUE |
| 2014 | IOR14D0058 | transport*of_fym_and_application | * | | | TRUE |
| 2014 | IOR14D0058 | watching | _ | | | TRUE |
| 2014 | IOR14D0058 | watching | _ | | | TRUE |

These observations were checked thoroughly and every alternate row is a duplicate of the one above it. So, necessary action was taken to remove these rows. Interestingly, we see a lot of duplicate entries stemming from households `IOR14D0054, IOR14D0055, IOR14D0056, IOR14D0057, IOR14D0058`. Now that duplicates, across all columns are removed, we checked the same for columns `hh_id, activity` where the previously mentioned households display a peculiar phenomenon. We identified 56 duplicate entries across `hh_id, activity` and they duplicate because each activity, in the first row marks as being done by men and repeats to say that its being done by both men and women. The flagged entires are being added here for reference:

| sur_yr | hh_id      | activity                         | men | women | men_women | dups |
| ------ | ---------- | -------------------------------- | --- | ----- | --------- | ---- |
| 2014   | IOR14D0054 | seed_selection_and_storage       |     |       | \*        | TRUE |
| 2014   | IOR14D0054 | seed_selection_and_storage       | \*  |       |           | TRUE |
| 2014   | IOR14D0054 | watching                         | \*  |       |           | TRUE |
| 2014   | IOR14D0054 | watching                         |     |       | \*        | TRUE |
| 2014   | IOR14D0055 | chemical_fertilizer_application  | \*  |       |           | TRUE |
| 2014   | IOR14D0055 | chemical_fertilizer_application  |     |       | \*        | TRUE |
| 2014   | IOR14D0055 | hand_weeding                     | \*  |       |           | TRUE |
| 2014   | IOR14D0055 | hand_weeding                     |     |       | \*        | TRUE |
| 2014   | IOR14D0055 | irrigation                       | \*  |       |           | TRUE |
| 2014   | IOR14D0055 | irrigation                       |     |       | \*        | TRUE |
| 2014   | IOR14D0055 | land_preparation                 | \*  |       |           | TRUE |
| 2014   | IOR14D0055 | land_preparation                 |     |       | \*        | TRUE |
| 2014   | IOR14D0055 | plant_protection_measures        | \*  |       |           | TRUE |
| 2014   | IOR14D0055 | plant_protection_measures        |     |       | \*        | TRUE |
| 2014   | IOR14D0055 | seed_selection_and_storage       |     |       | \*        | TRUE |
| 2014   | IOR14D0055 | seed_selection_and_storage       | \*  |       |           | TRUE |
| 2014   | IOR14D0055 | selection_of_crop                | \*  |       |           | TRUE |
| 2014   | IOR14D0055 | selection_of_crop                |     |       | \*        | TRUE |
| 2014   | IOR14D0055 | selection_of_variety             | \*  |       |           | TRUE |
| 2014   | IOR14D0055 | selection_of_variety             |     |       | \*        | TRUE |
| 2014   | IOR14D0055 | sowing_seed                      | \*  |       |           | TRUE |
| 2014   | IOR14D0055 | sowing_seed                      |     |       | \*        | TRUE |
| 2014   | IOR14D0055 | transplanting                    | \*  |       |           | TRUE |
| 2014   | IOR14D0055 | transplanting                    |     |       | \*        | TRUE |
| 2014   | IOR14D0055 | transport_of_fym_and_application | \*  |       |           | TRUE |
| 2014   | IOR14D0055 | transport_of_fym_and_application |     |       | \*        | TRUE |
| 2014   | IOR14D0056 | chemical_fertilizer_application  | \*  |       |           | TRUE |
| 2014   | IOR14D0056 | chemical_fertilizer_application  |     |       | \*        | TRUE |
| 2014   | IOR14D0056 | hand_weeding                     | \*  |       |           | TRUE |
| 2014   | IOR14D0056 | hand_weeding                     |     |       | \*        | TRUE |
| 2014   | IOR14D0056 | harvesting                       | \*  |       |           | TRUE |
| 2014   | IOR14D0056 | harvesting                       |     |       | \*        | TRUE |
| 2014   | IOR14D0056 | interculture                     | \*  |       |           | TRUE |
| 2014   | IOR14D0056 | interculture                     |     |       | \*        | TRUE |
| 2014   | IOR14D0056 | marketing                        | \*  |       |           | TRUE |
| 2014   | IOR14D0056 | marketing                        |     |       | \*        | TRUE |
| 2014   | IOR14D0056 | plant_protection_measures        | \*  |       |           | TRUE |
| 2014   | IOR14D0056 | plant_protection_measures        |     |       | \*        | TRUE |
| 2014   | IOR14D0056 | selection_of_crop                | \*  |       |           | TRUE |
| 2014   | IOR14D0056 | selection_of_crop                |     |       | \*        | TRUE |
| 2014   | IOR14D0056 | selection_of_variety             | \*  |       |           | TRUE |
| 2014   | IOR14D0056 | selection_of_variety             |     |       | \*        | TRUE |
| 2014   | IOR14D0056 | sowing_seed                      | \*  |       |           | TRUE |
| 2014   | IOR14D0056 | sowing_seed                      |     |       | \*        | TRUE |
| 2014   | IOR14D0056 | threshing                        | \*  |       |           | TRUE |
| 2014   | IOR14D0056 | threshing                        |     |       | \*        | TRUE |
| 2014   | IOR14D0056 | transport_of_fym_and_application | \*  |       |           | TRUE |
| 2014   | IOR14D0056 | transport_of_fym_and_application |     |       | \*        | TRUE |
| 2014   | IOR14D0056 | watching                         | \*  |       |           | TRUE |
| 2014   | IOR14D0056 | watching                         |     |       | \*        | TRUE |
| 2014   | IOR14D0057 | seed_selection_and_storage       |     |       | \*        | TRUE |
| 2014   | IOR14D0057 | seed_selection_and_storage       | \*  |       |           | TRUE |
| 2014   | IOR14D0058 | seed_selection_and_storage       |     |       | \*        | TRUE |
| 2014   | IOR14D0058 | seed_selection_and_storage       | \*  |       |           | TRUE |
| 2014   | IOR14D0058 | threshing                        |     |       | \*        | TRUE |
| 2014   | IOR14D0058 | threshing                        | \*  |       |           | TRUE |

In order to account for these entires, we have decided to recognize that all of the above activities specifically for these households are being done by both men and women. Hence the entry which marks only men have been removed. We realize that we are assuming for the better here when we have decided to keep the former.

The \* in the column were replaced with the value 1. While doing the same, it was ntoiced that the column `women` contained one observation with the value 9 and 3 observations in the column `men_women` with the value 0. These values were removed.

#### 1.9 Sources of marketing and other information

The sources of marketing and other information schedule of the GES questionnaire identifies institutions which the household considers as valid sources of information and also the ranking in which the household would approach each for different activities related to cultivation.

After performing basic wrangling measures, We identified 4 potential duplicate entries across all columns. Adding the same here:
| sur_yr | hh_id | inputs | Input Dealer | Seed Company | Other Farmers | NGO | Agriculture/Veterinary Dept | Research Station | Media | Krishi-melas | Others | rese_station | ip_manu | dups |
|--------|------------|--------------------|--------------|--------------|---------------|-----|-----------------------------|------------------|-------|--------------|--------|--------------|---------|------|
| 2014 | IBH14B0090 | crop output prices | 2 | | 1 | | | | | | | | | TRUE |
| 2014 | IBH14B0090 | crop output prices | 2 | | 1 | | | | | | | | | TRUE |
| 2014 | IBH14D0200 | crop output prices | | | 1 | | | | | | | | | TRUE |
| 2014 | IBH14D0200 | crop output prices | | | 1 | | | | | | | | | TRUE |

The duplicates in the above table have been removed followed by cleaning the `inputs` column which lists the activities and resources which the household would seek information for. Again in the duplicate entry check, we found the following entry:
| sur_yr | hh_id | inputs | Input Dealer | Seed Company | Other Farmers | NGO | Agriculture/Veterinary Dept | Research Station | Media | Krishi-melas | Others | rese_station | ip_manu | dups |
|--------|------------|--------------------|--------------|--------------|---------------|-----|-----------------------------|------------------|-------|--------------|--------|--------------|---------|------|
| 2012 | IBH12A0001 | crop output prices | 1 | | 2 | | | | | | | | | TRUE |
| 2012 | IBH12A0001 | crop output prices | 1 | | 2 | | | | | | | | | TRUE |

The duplicate entry was removed. The columns `rese_station, ip_manu` were renamed for better clarity. Also, all the columns have numbers or ranks as response values and hence all th columns were convereted to float data type. The dataframe was then widened to enable further processing.

#### 1.10 Coping echanisms

The coping mechanisms schedule of the GES questionnaire collects information from hosueholds related to the fact whether their livelihoods were affected by any severe drought/flood/pest/diseases/misfortunes. If yes, whether they received any support from the government. There are 4 parts to this schdeule:

##### 1.10.1 Coping mechanisms

Under this section, the affected households and the households which undertook coping mechanisms are identified. Three different coping mechanisms adopted by the male and female member of the household, each, is recorded. The loss incurred is recorded and its relative size to total income of the hosuehold is also recorded.

After implementing the basic wrangling measures, the `problem` column describing the adversity faced was recoded to the following categories:

- Anthropogenic
- Biophysical
- Climate Flood Drought
- Climate Others
- Others

The binary columns `ado_co_me`, mentioning whether the household adopted any coping mechanism when faced with adversity, was recoded to reflect binary choices as "adopted" and "not_adopted". Under the same column, there are 3 households, namely, `IOR14D0001, IOR14D0009, IOR14D0034` which has adopted multiple coping mechanisms. However, these households have `ado_co_me` as missing while they have multiple coping mechanisms mentioned. So the "adopted" string was extrtapolated for these households. If they are left as missing, it will generate as duplicate entries later in the process.

This dataset had special issue stemming from the East India subset where for years 2010 and 2011 in states Bihar, Jharkhand and Orissa where the household ID is mispelt as the succedding `hh_id`. Eg: in 2010 for a household in Orissa, the `hh_id` must look like "IOR10xxxx". Instead, the ID appeared here as "IOR11xxxx" which is essentially ID for the same household but in year 2011. This issue was rectified.

The coping mechnanisms were mapped to the strings mentioned in the schedule. The columns `loss_prctc_inc` and `loss_rs` were renamed to `percent_of_income_lost` and `losses_in_rupees` respectively for better clarity.

When checked for duplicate entries across all columns, we found the following 52 entries:
| sur_yr | hh_id | affected | ado_co_me | problem | percent_of_income_lost | co_mech_m1 | co_mech_m2 | co_mech_m3 | co_mech_f1 | co_mech_f2 | co_mech_f3 | losses_in_rupees | dups |
|--------|------------|----------|-------------|-----------------------|------------------------|---------------------|---------------------|------------|---------------------|---------------------|------------|------------------|------|
| 2010 | IKN10C0002 | Yes | not_adopted | Climate Flood Drought | | | | | | | | | TRUE |
| 2010 | IKN10C0002 | Yes | not_adopted | Climate Flood Drought | | | | | | | | | TRUE |
| 2010 | IKN10C0002 | Yes | not_adopted | Biophysical | | | | | | | | | TRUE |
| 2010 | IKN10C0002 | Yes | not_adopted | Anthropogenic | | | | | | | | | TRUE |
| 2010 | IKN10C0002 | Yes | not_adopted | Biophysical | | | | | | | | | TRUE |
| 2010 | IKN10C0002 | Yes | not_adopted | Anthropogenic | | | | | | | | | TRUE |
| 2010 | IKN10C0002 | Yes | not_adopted | Anthropogenic | | | | | | | | | TRUE |
| 2010 | IKN10C0002 | Yes | not_adopted | Biophysical | | | | | | | | | TRUE |
| 2010 | IKN10C0030 | Yes | not_adopted | Climate Flood Drought | | | | | | | | | TRUE |
| 2010 | IKN10C0030 | Yes | not_adopted | Climate Flood Drought | | | | | | | | | TRUE |
| 2010 | IKN10C0030 | Yes | not_adopted | Biophysical | | | | | | | | | TRUE |
| 2010 | IKN10C0030 | Yes | not_adopted | Anthropogenic | | | | | | | | | TRUE |
| 2010 | IKN10C0030 | Yes | not_adopted | Biophysical | | | | | | | | | TRUE |
| 2010 | IKN10C0030 | Yes | not_adopted | Anthropogenic | | | | | | | | | TRUE |
| 2010 | IKN10C0030 | Yes | not_adopted | Anthropogenic | | | | | | | | | TRUE |
| 2010 | IKN10C0030 | Yes | not_adopted | Biophysical | | | | | | | | | TRUE |
| 2010 | IKN10C0032 | Yes | not_adopted | Climate Flood Drought | | | | | | | | | TRUE |
| 2010 | IKN10C0032 | Yes | not_adopted | Climate Flood Drought | | | | | | | | | TRUE |
| 2010 | IKN10C0032 | Yes | not_adopted | Biophysical | | | | | | | | | TRUE |
| 2010 | IKN10C0032 | Yes | not_adopted | Anthropogenic | | | | | | | | | TRUE |
| 2010 | IKN10C0032 | Yes | not_adopted | Biophysical | | | | | | | | | TRUE |
| 2010 | IKN10C0032 | Yes | not_adopted | Anthropogenic | | | | | | | | | TRUE |
| 2010 | IKN10C0032 | Yes | not_adopted | Anthropogenic | | | | | | | | | TRUE |
| 2010 | IKN10C0032 | Yes | not_adopted | Biophysical | | | | | | | | | TRUE |
| 2010 | IKN10C0040 | Yes | not_adopted | Climate Flood Drought | | | | | | | | | TRUE |
| 2010 | IKN10C0040 | Yes | not_adopted | Climate Flood Drought | | | | | | | | | TRUE |
| 2010 | IKN10C0040 | Yes | not_adopted | Biophysical | | | | | | | | | TRUE |
| 2010 | IKN10C0040 | Yes | not_adopted | Anthropogenic | | | | | | | | | TRUE |
| 2010 | IKN10C0040 | Yes | not_adopted | Biophysical | | | | | | | | | TRUE |
| 2010 | IKN10C0040 | Yes | not_adopted | Anthropogenic | | | | | | | | | TRUE |
| 2010 | IKN10C0040 | Yes | not_adopted | Anthropogenic | | | | | | | | | TRUE |
| 2010 | IKN10C0040 | Yes | not_adopted | Biophysical | | | | | | | | | TRUE |
| 2010 | IKN10C0048 | Yes | not_adopted | Climate Flood Drought | | | | | | | | | TRUE |
| 2010 | IKN10C0048 | Yes | not_adopted | Climate Flood Drought | | | | | | | | | TRUE |
| 2010 | IKN10C0048 | Yes | not_adopted | Biophysical | | | | | | | | | TRUE |
| 2010 | IKN10C0048 | Yes | not_adopted | Anthropogenic | | | | | | | | | TRUE |
| 2010 | IKN10C0048 | Yes | not_adopted | Biophysical | | | | | | | | | TRUE |
| 2010 | IKN10C0048 | Yes | not_adopted | Anthropogenic | | | | | | | | | TRUE |
| 2010 | IKN10C0048 | Yes | not_adopted | Anthropogenic | | | | | | | | | TRUE |
| 2010 | IKN10C0048 | Yes | not_adopted | Biophysical | | | | | | | | | TRUE |
| 2010 | IMP10A0030 | Yes | adopted | Biophysical | 10 | cash loans | own savings | | cash loans | own savings | | | TRUE |
| 2010 | IMP10A0030 | Yes | adopted | Biophysical | 10 | cash loans | own savings | | cash loans | own savings | | | TRUE |
| 2011 | IMP11A0055 | Yes | adopted | Biophysical | 10 | own savings | cash loans | | own savings | help from relatives | | | TRUE |
| 2011 | IMP11A0055 | Yes | adopted | Biophysical | 10 | own savings | cash loans | | own savings | help from relatives | | | TRUE |
| 2013 | IMP13B0035 | Y | adopted | Biophysical | 10 | help from relatives | | | help from relatives | | | | TRUE |
| 2013 | IMP13B0035 | Y | adopted | Biophysical | 10 | help from relatives | | | help from relatives | | | | TRUE |
| 2014 | IMP14B0050 | Y | adopted | Biophysical | 10 | own savings | help from relatives | | own savings | help from relatives | | | TRUE |
| 2014 | IMP14B0050 | Y | adopted | Biophysical | 10 | own savings | help from relatives | | own savings | help from relatives | | | TRUE |
| 2010 | IBH10C0036 | Y | adopted | Climate Flood Drought | 20 | own savings | help from relatives | | own savings | help from relatives | | 2000 | TRUE |
| 2010 | IBH10C0036 | Y | adopted | Climate Flood Drought | 20 | own savings | help from relatives | | own savings | help from relatives | | 2000 | TRUE |
| 2010 | IBH10C0045 | Y | adopted | Climate Flood Drought | 20 | help from relatives | own savings | | help from relatives | own savings | | 3000 | TRUE |
| 2010 | IBH10C0045 | Y | adopted | Climate Flood Drought | 20 | help from relatives | own savings | | help from relatives | own savings | | 3000 | TRUE |

Later when checked for duplicates across columns `hh_id, ado_cop_me, problem` we found 184 duplicates. However, these entires are result of the fact that we recoded various calamities in `problem` into few categories. So the same houshepld which faced two separate calamities with different amount of losses are now popping up as duplicates. To resolve the above situation we adopted the following steps:

- We split the data into 2 parts: `df_cop`: which contains the hosuehold id and the coping mechanisms, `df_loss`: which contains the household id and losses. Both these parts contain the `ado_co_me`, `problem` columns as categories (part of data frame index when needed).
- For `df_cop`, the original data had 3 coping mechanisms for men and women, each. However, there is no requirement to stick to this. So we decided to consider the coping mechanisms adopted for two or more calamities in the same category (e.g.: Anthropogenic) as one instance and consider the adopted measures int he same order. For instance hosuehold x faced 2 calamities (y,z) belonging to Anthropogenic category. For calamity y, the women of the household adopted 3 mechanisms and men adopted 1 mechanism. For calamity z, the women adopted 2 mechanism and men adopted 3 mechanism. The data would consider, y and z as the same event and woukld take into account 5 mechanisms from the women and 4 mechanism from men.
- In case of `df_loss`, the when the houshold faces two or more calamities of the same category, the `percent_of_income_lost` and `losses_in_rupees` were aggregated across groups of `hh_id, ado_co_me, problem`.
- `df_cop` and `df_loss` were merged to arrive at the restructed version of the original dataframe.

Post merging, the data was widened for further processing.

##### 1.10.2 Government assistance

The governemnt assistance section enquires whether the household received any assistance from the government. And if yes, what is the assistance.

As per the data is concerned, this contains only information about households which received governemnet assistance. Moreover the there are mutiple households which recived multiple assistance during the same time period. Beyond that, the `assist_type` column, listing the assistance received by each household, conatins only string values and need some other processing method to make inferences out of it.

##### 1.10.3 Reliability ranking

In the reliability ranking section, the schedule expects the respondents to rank various government institutions, family and friends in terms of acting as a source of assisstance both in times of flood and drought.

After conducting the basic wrangling steps, the check for duplicate entires across all columns was conducted and no duplicates were found. Then we proceeded with cleaning the `sou_assistance` column which lists the various government institutions and other points of contact which are expected to be sought after by the affected households during the time of a disaster. The rogue string values in the column was cleaned and recoded to better reflect the questionnaire. There were quite a few rpgue strings which repeated themselves in different formats and were reluctant to place them in Others category instead we added sensible category names beyond the questionnaire and they are listed for reference:

- Micro Finance
- Landlord
- Employer
- Kinship and Relatives
- Government
- Input Dealer
- Migration
- Merchants
- Labour Work
- Others

In the duplicate entry check across `hh-id, sou_assistance`, after cleaning the latter, it was found that there were 6 duplicate entries. These entries were inspected whether to have originated as a result of cleaning of string values in `sou_assistance` but negative. The follwoing entries are the suspected duplicates:
| sur_yr | hh_id | sou_assistance | rank_rel_dro | rank_rel_flo | dups |
|--------|------------|-----------------------|--------------|--------------|------|
| 2014 | IOR14D0005 | kinship and relatives | | 6 | TRUE |
| 2014 | IOR14D0005 | kinship and relatives | | 5 | TRUE |
| 2014 | IOR14D0031 | kinship and relatives | | 5 | TRUE |
| 2014 | IOR14D0031 | kinship and relatives | | 4 | TRUE |
| 2014 | IOR14D0051 | village community | | 3 | TRUE |
| 2014 | IOR14D0051 | village community | | 4 | TRUE |

We can observe that the same household is ranking the same source with different ranks. So we have decided to asuume the best and take the highest rank \(lowest number\) assigned to a source in such cases. Also, the columns `rank_rel_dro, rank_rel_flo` which represents rank of source during drought and flood respectively, was converetd to float data type and renamed for better clarity.

##### 1.10.4 Proactive Measures

In the proactive measures section, the households are enquired abouy the their Aadoption of any proactive measures to mitigate future climate change related losses or shocks.

After performing basic wrangling steps, we discovered the presence 12 duplicate entires \(across all columns\) which are the following:
| sur_yr | hh_id | ad_proac_mea | proac_mea | dups |
|--------|------------|--------------|--------------------------------------------------------------|------|
| 2014 | IMH14B0059 | Y | SAVING IN BANK | TRUE |
| 2014 | IMH14B0059 | Y | SAVING IN BANK | TRUE |
| 2011 | IBH11A0039 | Y | MIGRATION FOR WORK | TRUE |
| 2011 | IBH11A0039 | Y | MIGRATION FOR WORK | TRUE |
| 2011 | IBH11B0031 | Y | STORAGE OF FOOD GRAINS | TRUE |
| 2011 | IBH11B0031 | Y | STORAGE OF FOOD GRAINS | TRUE |
| 2011 | IBH11B0031 | Y | STORAGE OF FOOD GRAINS | TRUE |
| 2011 | IBH11B0053 | Y | CASH SAVING | TRUE |
| 2011 | IBH11B0053 | Y | CASH SAVING | TRUE |
| 2012 | IBH12B0032 | Y | Storage Of Grains | TRUE |
| 2012 | IBH12B0032 | Y | Storage Of Grains | TRUE |
| 2012 | IBH12B0032 | Y | Storage Of Grains | TRUE |

Steps were taken to remove the above duplicates. Moreover, there are two main issue with the data:

- First major issue with the dataset is that, as seen above, the proactive measures are basically string values. There are no categories defined for this in the questionnaire which leaves us in the dark. Strangely enough, after stripping the column off white spaces and converting the strings to lower cases, to enforce uniformity in string values, we have 1706 unique rogue string values.

- Second, the column `ad_proac_mea` which identifies households whoich adopted proactive emasures with a tag "Y", has only "Y" as the response. In other owrds, the dataset is exclusively about households which adopted proactive measures.

### 2. Transaction Module (VDSA-L)

The transactions schedule collects data for each month at household resolution. This schedule is divided into 4 parts:

#### 2.1 Consumer expenditure

The consumer expenditure section of the schedule collects information about the quantity, unit price and total value of materials consumed and belonging to the following broad categories, namely,

- cereals
- pulses
- oils
- fruits
- vegetables
- dry fruits
- dairy products
- meat products
- other food items
- non food expenditure

The data was in provided in a shape where food expenditure for SAT India was split into state levels amd non food expenditure was provided similalry as adifferent set. On the other hand, data for East India was provided as a single dataset for each year. Hence each of the 3 had to be cleaned separately and compiled together.

##### 2.1.1 Food Expenditure - SAT India

The column `sur_mon_yr` was recast into "month-year" format inorder to appropriately reflect the month for which the corresponsding expenses were incurred. The column `item_type` was recoded to better reflect the categories of expenditure as listed above.

The column `tot_val` which correpsonds to the total expenditure of each household in a month for each specific food item mentioned in the schedule, has been renamed to `total_expense` to better clarity.

Although the file contains information about the source of procurement of the items, our research interest lies in extracting the total value of expenditure `total_expense` for each category for each household in each month, that is across columns `hh_id, sur_mon_yr, item_type`. Hence, the data was grouped and the `total_expense` columns was aggregated across columns `hh_id, sur_mon_yr, item_type`.

Prior to grouping, we identified 430 observations which were duplicates across all columns. Since the dataset had quantity of commodities purchased, it is not intutitive to have the same quantity of goods at the same price. Hence all such duplicate entries have been removed.
The following is a snapshot of the duplicates identified from the data:

| sur_yr | hh_id      | state | sur_mon_yr | item_type               | item_name                   | item_unit | qty_home_prod | qty_pur | qty_ot | ot_code | price_unit | total_expense | dups |
| ------ | ---------- | ----- | ---------- | ----------------------- | --------------------------- | --------- | ------------- | ------- | ------ | ------- | ---------- | ------------- | ---- |
| 2010   | IAP10D0006 | AP    | 40483      | cereals                 | PDS Rice                    | Kg        |               | 25      |        |         | 2          |               | TRUE |
| 2010   | IAP10D0006 | AP    | 40483      | other food items        | Sugar & Gur                 | Kg        |               | 3       |        |         | 30         |               | TRUE |
| 2010   | IAP10D0006 | AP    | 40483      | non-veg (meat and eggs) | Meat (goat, chicken, sheep) | Kg        |               | 2       |        |         | 120        |               | TRUE |
| 2010   | IAP10D0006 | AP    | 40483      | cereals                 | PDS Rice                    | Kg        |               | 25      |        |         | 2          |               | TRUE |
| 2010   | IAP10D0006 | AP    | 40483      | other food items        | Sugar & Gur                 | Kg        |               | 3       |        |         | 30         |               | TRUE |
| 2010   | IAP10D0006 | AP    | 40483      | non-veg (meat and eggs) | Meat (goat, chicken, sheep) | Kg        |               | 2       |        |         | 120        |               | TRUE |
| 2010   | IMH10A0286 | MH    | 40391      | cereals                 | PDS Rice                    | Kg        |               | 10      |        |         | 6          |               | TRUE |
| 2010   | IMH10A0286 | MH    | 40391      | oils                    | Palm oil/Dalda              | Kg        |               | 0.5     |        |         | 100        |               | TRUE |
| 2010   | IMH10A0286 | MH    | 40391      | other food items        | Tea/Coffee powder           | Kg        |               | 0.2     |        |         | 280        |               | TRUE |
| 2010   | IMH10A0286 | MH    | 40391      | other food items        | Mid day meal                | Rs        |               |         | 90     | 1       |            |               | TRUE |
| 2010   | IMH10A0286 | MH    | 40391      | cereals                 | PDS Rice                    | Kg        |               | 10      |        |         | 6          |               | TRUE |
| 2010   | IMH10A0286 | MH    | 40391      | oils                    | Palm oil/Dalda              | Kg        |               | 0.5     |        |         | 100        |               | TRUE |
| 2010   | IMH10A0286 | MH    | 40391      | other food items        | Tea/Coffee powder           | Kg        |               | 0.2     |        |         | 280        |               | TRUE |
| 2010   | IMH10A0286 | MH    | 40391      | other food items        | Mid day meal                | Rs        |               |         | 90     | 1       |            |               | TRUE |
| 2010   | IMH10A0286 | MH    | 40513      | pulses                  | Chickpea                    | Kg        | 0.5           |         |        |         | 38         |               | TRUE |
| 2010   | IMH10A0286 | MH    | 40513      | oils                    | Palm oil/Dalda              | Kg        |               | 0.5     |        |         | 100        |               | TRUE |
| 2010   | IMH10A0286 | MH    | 40513      | pulses                  | Chickpea                    | Kg        | 0.5           |         |        |         | 38         |               | TRUE |
| 2010   | IMH10A0286 | MH    | 40513      | oils                    | Palm oil/Dalda              | Kg        |               | 0.5     |        |         | 100        |               | TRUE |
| 2010   | IMH10B0237 | MH    | 40575      | cereals                 | PDS Wheat                   | Kg        |               | 10      |        |         | 10         |               | TRUE |
| 2010   | IMH10B0237 | MH    | 40575      | pulses                  | Chickpea                    | Kg        |               | 1       |        |         | 35         |               | TRUE |
| 2010   | IMH10B0237 | MH    | 40575      | other food items        | ALL SPICES & CONDIMENTS     | Rs        |               | 50      |        |         |            |               | TRUE |
| 2010   | IMH10B0237 | MH    | 40575      | other food items        | Sugar & Gur                 | Kg        |               | 7       |        |         | 30         |               | TRUE |
| 2010   | IMH10B0237 | MH    | 40575      | non-veg (meat and eggs) | Meat (goat, chicken, sheep) | Kg        |               | 0.5     |        |         | 150        |               | TRUE |
| 2010   | IMH10B0237 | MH    | 40575      | other food items        | Mid day meal                | Rs        |               |         | 120    | 1       |            |               | TRUE |
| 2010   | IMH10B0237 | MH    | 40575      | cereals                 | PDS Wheat                   | Kg        |               | 10      |        |         | 10         |               | TRUE |
| 2010   | IMH10B0237 | MH    | 40575      | pulses                  | Chickpea                    | Kg        |               | 1       |        |         | 35         |               | TRUE |
| 2010   | IMH10B0237 | MH    | 40575      | other food items        | ALL SPICES & CONDIMENTS     | Rs        |               | 50      |        |         |            |               | TRUE |
| 2010   | IMH10B0237 | MH    | 40575      | other food items        | Sugar & Gur                 | Kg        |               | 7       |        |         | 30         |               | TRUE |
| 2010   | IMH10B0237 | MH    | 40575      | non-veg (meat and eggs) | Meat (goat, chicken, sheep) | Kg        |               | 0.5     |        |         | 150        |               | TRUE |
| 2010   | IMH10B0237 | MH    | 40575      | other food items        | Mid day meal                | Rs        |               |         | 120    | 1       |            |               | TRUE |

##### 2.1.2 Non-Food Expenditure - SAT India

This section contains information on consumption expenditure of non-food items in SAT India.

The column `sur_mon_yr` was recast into "month-year" format inorder to appropriately reflect the month for which the corresponsding expenses were incurred. The column `nf_tot_val`, which corresponds to total epxenses related to non-food consumption was converted to float. We found the follwoing 82 observations which were duplicates across all columns:
| sur_yr | hh_id | sur_mon_yr | nf_item_name | nf_home_prod | nf_pur | nf_others | nf_ot_co | nf_tot_val | dups |
|--------|------------|------------|---------------------------------------------|--------------|--------|-----------|----------|------------|------|
| 2010 | IAP10D0006 | 40483 | Cigarettes,Pan,Ganja,Beedi,Tocacco,Arecanut | | 300 | | | 300 | TRUE |
| 2010 | IAP10D0006 | 40483 | Entertainment, TV, cable exp. | | 200 | | | 200 | TRUE |
| 2010 | IAP10D0006 | 40483 | News Paper Bill | | 100 | | | 100 | TRUE |
| 2010 | IAP10D0006 | 40483 | Cigarettes,Pan,Ganja,Beedi,Tocacco,Arecanut | | 300 | | | 300 | TRUE |
| 2010 | IAP10D0006 | 40483 | Entertainment, TV, cable exp. | | 200 | | | 200 | TRUE |
| 2010 | IAP10D0006 | 40483 | News Paper Bill | | 100 | | | 100 | TRUE |
| 2010 | IMH10B0237 | 40575 | Grinding / Milling charges | | 60 | | | 60 | TRUE |
| 2010 | IMH10B0237 | 40575 | Grinding / Milling charges | | 60 | | | 60 | TRUE |
| 2010 | IMH10B0237 | 40575 | Others (Specify) | | 50 | | | 50 | TRUE |
| 2010 | IMH10B0237 | 40575 | Others (Specify) | | 50 | | | 50 | TRUE |
| 2010 | IMH10C0055 | 40513 | Clothes, shoes, socks & Tailoring etc. | | 250 | | | 250 | TRUE |
| 2010 | IMH10C0055 | 40513 | Clothes, shoes, socks & Tailoring etc. | | 250 | | | 250 | TRUE |
| 2010 | IMH10D0036 | 40603 | Grinding / Milling charges | | 24 | | | 24 | TRUE |
| 2010 | IMH10D0036 | 40603 | Grinding / Milling charges | | 24 | | | 24 | TRUE |
| 2010 | IMH10D0036 | 40603 | Phone bill(Cell & Landline) | | 25 | | | 25 | TRUE |
| 2010 | IMH10D0036 | 40603 | Phone bill(Cell & Landline) | | 25 | | | 25 | TRUE |
| 2011 | IAP11D0045 | 40909 | Ele. and water charges | | 250 | | | 250 | TRUE |
| 2011 | IAP11D0045 | 40909 | Ele. and water charges | | 250 | | | 250 | TRUE |
| 2011 | IGJ11D0035 | 40940 | Ceremonies, marriage exp. | | 100 | | | 100 | TRUE |
| 2011 | IGJ11D0035 | 40940 | Ceremonies, marriage exp. | | 100 | | | 100 | TRUE |
| 2011 | IGJ11D0054 | 40940 | Ceremonies, marriage exp. | | 150 | | | 150 | TRUE |
| 2011 | IGJ11D0054 | 40940 | Ceremonies, marriage exp. | | 150 | | | 150 | TRUE |
| 2011 | IKN11C0006 | 40787 | Grinding/Milling Charges | | 30 | | | 30 | TRUE |
| 2011 | IKN11C0006 | 40787 | Grinding/Milling Charges | | 30 | | | 30 | TRUE |
| 2012 | IAP12A0303 | 41275 | Toddy & Alcohol | | 60 | | | 60 | TRUE |
| 2012 | IAP12A0303 | 41275 | HH articles & small durables | | 5 | | | 5 | TRUE |
| 2012 | IAP12A0303 | 41275 | Charcoal,LPG,firewood etc. | 240 | 30 | | | 270 | TRUE |
| 2012 | IAP12A0303 | 41275 | All cosmetics | | 260 | | | 260 | TRUE |
| 2012 | IAP12A0303 | 41275 | Cigarettes, pan, ganja, etc. | | 140 | | | 140 | TRUE |
| 2012 | IAP12A0303 | 41275 | Education expenses | | 40 | | | 40 | TRUE |
| 2012 | IAP12A0303 | 41275 | Travel, petrol, veh. maint. | | 90 | | | 90 | TRUE |
| 2012 | IAP12A0303 | 41275 | Cell and land phone bill | | 40 | | | 40 | TRUE |
| 2012 | IAP12A0303 | 41275 | Grinding/Milling charges | | 35 | | | 35 | TRUE |
| 2012 | IAP12A0303 | 41275 | Toddy & Alcohol | | 60 | | | 60 | TRUE |
| 2012 | IAP12A0303 | 41275 | HH articles & small durables | | 5 | | | 5 | TRUE |
| 2012 | IAP12A0303 | 41275 | Charcoal,LPG,firewood etc. | 240 | 30 | | | 270 | TRUE |
| 2012 | IAP12A0303 | 41275 | All cosmetics | | 260 | | | 260 | TRUE |
| 2012 | IAP12A0303 | 41275 | Cigarettes, pan, ganja, etc. | | 140 | | | 140 | TRUE |
| 2012 | IAP12A0303 | 41275 | Education expenses | | 40 | | | 40 | TRUE |
| 2012 | IAP12A0303 | 41275 | Travel, petrol, veh. maint. | | 90 | | | 90 | TRUE |
| 2012 | IAP12A0303 | 41275 | Cell and land phone bill | | 40 | | | 40 | TRUE |
| 2012 | IAP12A0303 | 41275 | Grinding/Milling charges | | 35 | | | 35 | TRUE |
| 2012 | IGJ12A0039 | 41395 | Entertainment, TV, cable exp. | | 200 | | | 200 | TRUE |
| 2012 | IGJ12A0039 | 41395 | Entertainment, TV, cable exp. | | 200 | | | 200 | TRUE |
| 2012 | IGJ12B0009 | 41334 | Cigarettes, pan, ganja, etc. | | 600 | | | 600 | TRUE |
| 2012 | IGJ12B0009 | 41334 | Cigarettes, pan, ganja, etc. | | 600 | | | 600 | TRUE |
| 2012 | IGJ12B0055 | 41334 | Grinding/Milling charges | | 90 | | | 90 | TRUE |
| 2012 | IGJ12B0055 | 41334 | Grinding/Milling charges | | 90 | | | 90 | TRUE |
| 2012 | IGJ12C0003 | 41183 | Charcoal,LPG,firewood etc. | | 180 | | | 180 | TRUE |
| 2012 | IGJ12C0003 | 41183 | Cell and land phone bill | | 100 | | | 100 | TRUE |
| 2012 | IGJ12C0003 | 41183 | Grinding/Milling charges | | 120 | | | 120 | TRUE |
| 2012 | IGJ12C0003 | 41183 | Charcoal,LPG,firewood etc. | | 180 | | | 180 | TRUE |
| 2012 | IGJ12C0003 | 41183 | Cell and land phone bill | | 100 | | | 100 | TRUE |
| 2012 | IGJ12C0003 | 41183 | Grinding/Milling charges | | 120 | | | 120 | TRUE |
| 2012 | IKN12B0037 | 41183 | All cosmetics | | 120 | | | 120 | TRUE |
| 2012 | IKN12B0037 | 41183 | Grinding/Milling charges | | 62 | | | 62 | TRUE |
| 2012 | IKN12B0037 | 41183 | All cosmetics | | 120 | | | 120 | TRUE |
| 2012 | IKN12B0037 | 41183 | Grinding/Milling charges | | 62 | | | 62 | TRUE |
| 2012 | IKN12B0057 | 41244 | Cell and land phone bill | | 150 | | | 150 | TRUE |
| 2012 | IKN12B0057 | 41244 | Cell and land phone bill | | 150 | | | 150 | TRUE |
| 2012 | IMH12C0047 | 41365 | Toddy & Alcohol | | 3500 | | | 3500 | TRUE |
| 2012 | IMH12C0047 | 41365 | Charcoal,LPG,firewood etc. | 150 | 150 | | | 300 | TRUE |
| 2012 | IMH12C0047 | 41365 | Cigarettes, pan, ganja, etc. | | 1000 | | | 1000 | TRUE |
| 2012 | IMH12C0047 | 41365 | Grinding/Milling charges | | 100 | | | 100 | TRUE |
| 2012 | IMH12C0047 | 41365 | Toddy & Alcohol | | 3500 | | | 3500 | TRUE |
| 2012 | IMH12C0047 | 41365 | Charcoal,LPG,firewood etc. | 150 | 150 | | | 300 | TRUE |
| 2012 | IMH12C0047 | 41365 | Cigarettes, pan, ganja, etc. | | 1000 | | | 1000 | TRUE |
| 2012 | IMH12C0047 | 41365 | Grinding/Milling charges | | 100 | | | 100 | TRUE |
| 2013 | IAP13A0008 | 41518 | HH articles & small durables | | 30 | | | 30 | TRUE |
| 2013 | IAP13A0008 | 41518 | HH articles & small durables | | 30 | | | 30 | TRUE |
| 2013 | IAP13B0200 | 41730 | Ele. and water charges | | 15 | | | 15 | TRUE |
| 2013 | IAP13B0200 | 41730 | Ele. and water charges | | 15 | | | 15 | TRUE |
| 2013 | IGJ13A0043 | 41699 | Education expenses | | 100 | | | 100 | TRUE |
| 2013 | IGJ13A0043 | 41699 | Education expenses | | 100 | | | 100 | TRUE |
| 2014 | IMH14A0051 | 41883 | Ele. and water charges | | 245 | | | 245 | TRUE |
| 2014 | IMH14A0051 | 41883 | Ele. and water charges | | 245 | | | 245 | TRUE |
| 2014 | IMH14B0041 | 41852 | | | | | | 0 | TRUE |
| 2014 | IMH14B0041 | 41852 | | | | | | 0 | TRUE |
| 2014 | IMH14B0041 | 41852 | | | | | | 0 | TRUE |
| 2014 | IMH14B0041 | 42156 | All cosmetics | | 200 | | | 200 | TRUE |
| 2014 | IMH14B0041 | 42156 | All cosmetics | | 200 | | | 200 | TRUE |
| 2014 | IMH14B0202 | 41852 | Ele. and water charges | | 280 | | | 280 | TRUE |
| 2014 | IMH14B0202 | 41852 | Ele. and water charges | | 280 | | | 280 | TRUE |

We have adopted necessary measures to remove these duplicates.

Since all the items belong to the broader category of non-food items, we grouped the values across households and for each month, `hh_id, sur_mon_yr`. After aggregating the `nf_tot_val` column, it was renamed to `total_expense` for seamless row concatenation with data from the Food Expenditure - SAT India section. On the same grounds we are creating a new column `item_type` whcih will hold the string value "non food expenditure".

##### 2.1.3 Consumption Expenditure - East India

This section contains all the consumption expenditure pertaining to households in East India. This daatset resembles the combined version of food and non food expenditure for East India.

Primarily, we cleaned the `item_category, item_type, item_name` columns inorder to ensure uniform string values before we check for duplicates. Following actions were adopted to clean the entries:

- Entires were mising in `item_type` when `item_category` was "non-food" for certain observation in some states for some years. Similary it was marked as "non-food expenditure" in some other cases. So the latter was extrapolated for the former.

- Rogue entries in `'item_map` column were recoded to reflect categories mentioned in the Food Consumption SAT India section.

- For years 2010, 2011, 2012, we see a category "all fruits and vegetables" in the `item_type` column whcih encompasses all values mentioned under fruits, vegetables, and dry fruits. So we isolated these unique fruits and dry fruits and recoded the `item_type` to keep fruits and dry fruits separate from "all fruits and vegetables" and also recoded it as "vegetables".

The columns `tot_val` was renamed as `total_expense`.

In the check for duplicates entries we were able to flag 5850 entries. Compared to the size of the data, whcih goes upto 965,215 observations, the size of duplicates is very small and a possoble number.

#### 2.2 Sale of crop and livestock products

The sale of crop and livestock products enquires about the quantity and total value of products sold by the household. It also collects information on whether the products were sold within the village or not and to whom. If not, how far was the market outisde the village.

After performing the basic wrangling measures, we cleaned the `crop_lst_prod` column which to reflect the categories of products sold. We recoded the column to have two categories, namely, "Crops" and "Livestock". The `sur_mon_yr` column was converetd to date format and the column corresponds to the month for which the data is collected.

The column `sold_in_out` is expected to be a binary column indicating whether the products were sold within the village or not. However, the 2 observations contain the rogue values "0" and "6". All the values in the column were recoded to string values "Within village" and "Outside village" as defined in the schedule. Teh rogue values were recoded tp within village because it didnot have values mentioning the name of and distance to the outside market.

The `sold_to_co` column, which represents the agency to which the farmer sold his/her products, such as fellow farmer, cooperative society etc, were assigned their string values provided in the questionnaire. There existed the numeric value "10" which was beyond the categories mentioned schedule. When inspected closely, it mostly corresponds to saler sof Milk under "Livestock Products", the households which had the value 10 sold milk to fellow farmers, which g=had the numeric code 1. So we assume that the code 10 is an error and corresponds to feloow farmers. So 10 was recoded Fellow Farmers.

The numeric columns, `qty_sold, unit_pri, os_dist, os_mar_costs`, were converted to float data type. They represent the quantity sold, the unit price and if sold outside village, then how far is that market and the per unit market cost at the outside village market, repectively. Once the numeric columns were converted to float, we created the `total_sales` column which is the prodcut of `qty_sold, unit_pri`. Similarly the total market cost was calculated, while selling at, outside village, markets by multiplying `qty_sold, os_mar_costs`. A new variable `outside_village_market_cost` was created to hold this information.

We identified 12 observations which were duplicates, when checked across columns. These entires are presented below for reference:
| sur_yr | hh_id | sur_mon_yr | dt_int | crop_lst_prod | prod_name | sold_in_out | sold_to_co | unit_sold | qty_sold | unit_pri | os_place | os_dist | os_mar_costs | sold_to_co_ot | total_sales | dups |
|--------|------------|------------|------------|--------------------|----------------------|----------------|---------------|-----------|----------|----------|------------------|---------|--------------|----------------------|-------------|------|
| 2013 | IBH13D0038 | 01-11-2013 | 27-01-2014 | Livestock Products | Milk | Within Village | Fellow farmer | Lt | 90 | 25 | | | | | 2250 | TRUE |
| 2013 | IBH13D0038 | 01-11-2013 | 27-01-2014 | Livestock Products | Milk | Within Village | Fellow farmer | Lt | 90 | 25 | | | | | 2250 | TRUE |
| 2014 | IOR14C0055 | 01-04-2015 | 23-04-2015 | Livestock Products | Milk | Within Village | Co-operative | Lt | 120 | 24 | | | | | 2880 | TRUE |
| 2014 | IOR14C0058 | 01-04-2015 | 28-04-2015 | Livestock Products | Milk | Within Village | Fellow farmer | Lt | 5 | 24 | | | | | 120 | TRUE |
| 2014 | IOR14C0059 | 01-04-2015 | 15-04-2015 | Livestock Products | Milk | Within Village | Fellow farmer | Lt | 5 | 24 | | | | | 120 | TRUE |
| 2014 | IOR14C0055 | 01-04-2015 | 23-04-2015 | Livestock Products | Milk | Within Village | Co-operative | Lt | 120 | 24 | | | | | 2880 | TRUE |
| 2014 | IOR14C0058 | 01-04-2015 | 28-04-2015 | Livestock Products | Milk | Within Village | Fellow farmer | Lt | 5 | 24 | | | | | 120 | TRUE |
| 2014 | IOR14C0059 | 01-04-2015 | 15-04-2015 | Livestock Products | Milk | Within Village | Fellow farmer | Lt | 5 | 24 | | | | | 120 | TRUE |
| 2014 | IJH14C0037 | 01-04-2015 | 20-05-2015 | Crop | PADDY | Within Village | Broker | Qt | 1 | 1750 | | | | | 1750 | TRUE |
| 2014 | IJH14C0037 | 01-04-2015 | 20-05-2015 | Crop | PADDY | Within Village | Broker | Qt | 1 | 1750 | | | | | 1750 | TRUE |
| 2012 | IMH12C0047 | 01-04-2013 | | Livestock Products | Milk | Within Village | Fellow farmer | Lt | 90 | 36 | | | | | 3240 | TRUE |
| 2012 | IMH12C0047 | 01-04-2013 | | Livestock Products | Milk | Within Village | Fellow farmer | Lt | 90 | 36 | | | | | 3240 | TRUE |

The duplicate entires have been successfully removed. The data was then grouped across the columns `hh_id,	sur_mon_yr, crop_lst_prod, sold_in_out	sold_to_co` and the sum of columns `total_sales, outside_village_market_cost` and mean of column `os_dist` was taken for each group. The data widened in the process for further processing.

#### 2.3 Financial Transactions

The Financial transactions section of the Transactions schedule contains information about the following:

- Loans taken by the household from:

  1. Loans from institutions
  2. Loans from non-institutions

- Gifts \(both cash and kind\)
- Savings and deposits
- Receipts and payments
- Loss of property
- Benefits from government programs

Out of the above, loans taken by household and benefits from government have been provided as a seperate dataset.

##### 2.3.1 Loans

The loans subset contains information on the loans repaid, taken, interest rate and purpose for which the loan was taken. It also enquires about the source from which the loan was taken.

After the basic wrangling measures, the `sur_mon_yr` column was converted to a date to reflect the month for which the values were collected. After ensuring that there are no furtehr errors with the column, we recoded the `loan_source` column, which had 97 rogue string values, to better reflect the categories mentioned in the schedule. `loan_source` mentions the source whcih the household received the loan. The mapper used to recode `loan_source` is available at [loan_source_map](). We will not considering `loan_category` column because it mentions whether the source is institutional or not. However, the source names are intuitive enough to identify themsleves as instituional sources or not. The columns `loan_repaid,	loan_rec, loan_int`, representing the loan repaid by the household, the loan received by the household and interest rate per loan respectively, were converted to float.

We identified 42 observations with duplicates and the entries are listed below:
| sur_yr | hh_id | dt_int | sur_mon_yr | loan_category | loan_source | loan_repaid | loan_rec | loan_purpose | loan_int | remarks | who_sp_ben | id_who_did | dups |
|--------|------------|------------|------------|------------------|-------------------|-------------|----------|--------------------------|----------|---------|------------|------------|------|
| 2010 | IJH10B0039 | 10-06-2011 | 01-05-2011 | non-institutions | Others | | 5000 | Domestic | 0 | | | | TRUE |
| 2010 | IJH10B0039 | 10-06-2011 | 01-05-2011 | non-institutions | Others | | 5000 | Domestic | 0 | | | | TRUE |
| 2012 | IOR12A0008 | 02-04-2013 | 01-03-2013 | non-institutions | Self-help groups | 500 | | | | | | | TRUE |
| 2012 | IOR12A0008 | 02-04-2013 | 01-03-2013 | non-institutions | Self-help groups | 500 | | | | | | | TRUE |
| 2012 | IOR12A0037 | 05-04-2013 | 01-03-2013 | non-institutions | Money lenders | | 4000 | Marriage | 10 | | | | TRUE |
| 2012 | IOR12A0037 | 05-04-2013 | 01-03-2013 | non-institutions | Money lenders | | 4000 | Marriage | 10 | | | | TRUE |
| 2012 | IOR12A0051 | 03-04-2013 | 01-03-2013 | non-institutions | Others | | 7000 | Marriage | 12 | | | | TRUE |
| 2012 | IOR12A0051 | 03-04-2013 | 01-03-2013 | non-institutions | Others | | 7000 | Marriage | 12 | | | | TRUE |
| 2012 | IOR12A0054 | 02-04-2013 | 01-03-2013 | non-institutions | Others | | 20000 | Marriage | 24 | | | | TRUE |
| 2012 | IOR12A0054 | 02-04-2013 | 01-03-2013 | non-institutions | Others | | 20000 | Marriage | 24 | | | | TRUE |
| 2012 | IOR12B0201 | 03-04-2013 | 01-03-2013 | non-institutions | Self-help groups | 1000 | | | | | | | TRUE |
| 2012 | IOR12B0201 | 03-04-2013 | 01-03-2013 | non-institutions | Self-help groups | 1000 | | | | | | | TRUE |
| 2012 | IOR12D0050 | 29-10-2012 | 01-10-2012 | institutions | Commercial banks | 2400 | | | | | | | TRUE |
| 2012 | IOR12D0050 | 29-10-2012 | 01-10-2012 | institutions | Commercial banks | 2400 | | | | | | | TRUE |
| 2012 | IOR12D0052 | 28-10-2012 | 01-11-2012 | institutions | Commercial banks | 5000 | | | | | | | TRUE |
| 2012 | IOR12D0052 | 28-10-2012 | 01-11-2012 | non-institutions | Money lenders | 5000 | | | | | | | TRUE |
| 2012 | IOR12D0052 | 28-10-2012 | 01-11-2012 | institutions | Commercial banks | 5000 | | | | | | | TRUE |
| 2012 | IOR12D0052 | 28-10-2012 | 01-11-2012 | non-institutions | Money lenders | 5000 | | | | | | | TRUE |
| 2012 | IOR12D0056 | 07-11-2012 | 01-11-2012 | institutions | Finance companies | 12500 | | | | | | | TRUE |
| 2012 | IOR12D0056 | 07-11-2012 | 01-11-2012 | institutions | Finance companies | 12500 | | | | | | | TRUE |
| 2014 | IOR14B0001 | 23-07-2014 | 01-07-2014 | non-institutions | Friend/relative | | 1000 | CULTIVATION | 0 | | | | TRUE |
| 2014 | IOR14B0032 | 17-07-2014 | 01-07-2014 | non-institutions | Friend/relative | 700 | | MARKETING | 0 | | | | TRUE |
| 2014 | IOR14B0040 | 23-07-2014 | 01-07-2014 | non-institutions | Friend/relative | | 1000 | MARKETING | 0 | | | | TRUE |
| 2014 | IOR14B0046 | 28-07-2014 | 01-07-2014 | non-institutions | Friend/relative | | 5000 | AGRICULTURE | 0 | | | | TRUE |
| 2014 | IOR14B0205 | 23-07-2014 | 01-07-2014 | non-institutions | Input dealer | | 15000 | BUSINESS | 0 | | | | TRUE |
| 2014 | IOR14B0052 | 25-07-2014 | 01-07-2014 | non-institutions | Friend/relative | 1000 | | DAILY NEED | 0 | | | | TRUE |
| 2014 | IOR14B0056 | 30-07-2014 | 01-07-2014 | non-institutions | Friend/relative | | 10000 | AGRICULTURE | 0 | | | | TRUE |
| 2014 | IOR14B0001 | 23-07-2014 | 01-07-2014 | non-institutions | Friend/relative | | 1000 | CULTIVATION | 0 | | | | TRUE |
| 2014 | IOR14B0032 | 17-07-2014 | 01-07-2014 | non-institutions | Friend/relative | 700 | | MARKETING | 0 | | | | TRUE |
| 2014 | IOR14B0040 | 23-07-2014 | 01-07-2014 | non-institutions | Friend/relative | | 1000 | MARKETING | 0 | | | | TRUE |
| 2014 | IOR14B0046 | 28-07-2014 | 01-07-2014 | non-institutions | Friend/relative | | 5000 | AGRICULTURE | 0 | | | | TRUE |
| 2014 | IOR14B0205 | 23-07-2014 | 01-07-2014 | non-institutions | Input dealer | | 15000 | BUSINESS | 0 | | | | TRUE |
| 2014 | IOR14B0052 | 25-07-2014 | 01-07-2014 | non-institutions | Friend/relative | 1000 | | DAILY NEED | 0 | | | | TRUE |
| 2014 | IOR14B0056 | 30-07-2014 | 01-07-2014 | non-institutions | Friend/relative | | 10000 | AGRICULTURE | 0 | | | | TRUE |
| 2010 | IAP10D0006 | | 01-11-2010 | institutions | Self-help groups | 300 | | | | | | 4 | TRUE |
| 2010 | IAP10D0006 | | 01-11-2010 | institutions | Self-help groups | 300 | | | | | | 4 | TRUE |
| 2010 | IKN10C0036 | | 01-02-2011 | institutions | Cooperatives | 3000 | | HOUSE | 14 | | | 1 | TRUE |
| 2010 | IKN10C0036 | | 01-02-2011 | institutions | Cooperatives | 3000 | | HOUSE | 14 | | | 1 | TRUE |
| 2011 | IKN11C0036 | | 01-07-2011 | institutions | Cooperatives | 3000 | | | | | | 1, 2 | TRUE |
| 2011 | IKN11C0036 | | 01-07-2011 | institutions | Cooperatives | 3000 | | | | | | 1, 2 | TRUE |
| 2012 | IKN12B0057 | | 01-12-2012 | institutions | Commercial banks | 5000 | | | | | | 1 | TRUE |
| 2012 | IKN12B0057 | | 01-12-2012 | institutions | Commercial banks | 5000 | | | | | | 1 | TRUE |

Duplicates from these entries were removed. Post that, the `loan_source` column was recoded as described earlier. The columns `loan_rec, loan_int` were renamed to `loan_received, interest_on_loan` for better clarity. The data was later widened by grouping over columns `hh_id, sur_mon_yr, loan_source` and aggregating the columns`loan_repaid, loan_received` to sum across groups and the avergae of column `interest_on_loan` was taken across groups.

##### 2.3.2 Gifts, Savings, Receipts, Loss of property

In the current dataset, as part of the basic wrangling measures, we have removed 6 columns which are completely nill and some are relatively populated but irrelevant for the current analysis.

As the first step, we converetd the `sur_mon_yr` column, whcih identifies the month for which the transaction is mentioned, to date format. We noticed that unlike other years, the dataset from East India for the year 2014 swaps the `dt_int` and `sur_mon_yr` where the former is the date on which the interview was conducted. there are 7418 observations stemming from this year and region and hence necessary action have been taken to swap them back to place. Also, for households `IOR14C0033, IOR14C0039` a date value was wrongly passed as August 2008 while it was August 2014 and date was in wrong format respectively. Hence both the errors were rectified.

Followed by the cleaning of the `fin_category` column whicgh identifies categories of transactions exercised by the household. The columns were recoded to reflect the categories mentioned above. However, while attempting to do so, we came across a small header related issue with the data where, we have the following the entry:
| sur_yr | hh_id | dt_int | sur_mon_yr | fin_category | fin_source | amt_giv | amt_rec | id_who_did | remarks |
|--------|--------|------------|------------|--------------|------------|---------|---------|------------|---------|
| 2014 | VDS_ID | SUR_MON_YR | DT_INT | fin_category | fin_source | AMT_GIV | AMT_REC | ID_WHO_DID | |

We tend to belive that this could be a header option rleated issue which crept in from one of the 2014 subfiles. So this particular entry has been selectively removed from the dataset, before recoding the `fin_category` column.

The `fin_source` column has 1618 rogue string values and we expect to widen the data using only the `fin_category` column. Hence, we are ignoring this column. `who_sp` is another categorical column which identifies whetehr the money was used by the male or female member of the household. Some string values were recoded to better reflect the categories `Male, Female, Both` within the column.

The columns `amt_giv, amt_rec, who_sp` were renamed as `amount_given, amount_received, amount_spend_by` for better clarity.

We found 198 observations with duplicates across all columns and the first 25 obs are presented here for reference. These duplicates have been removed.
| sur_yr | hh_id | dt_int | sur_mon_yr | fin_category | fin_source | amount_given | amount_received | amount_spend_by | dups |
|--------|------------|--------|------------|-----------------------|-------------------------------------------|--------------|-----------------|-----------------|------|
| 2012 | IJH12B0031 | 41135 | 41091 | receipts and payments | exp. for repairs of house, impl., etc. | 350 | | | TRUE |
| 2012 | IJH12B0031 | 41135 | 41091 | receipts and payments | exp. for repairs of house, impl., etc. | 350 | | | TRUE |
| 2012 | IOR12A0041 | 41335 | 41306 | receipts and payments | rents on land, house & others | | 5000 | | TRUE |
| 2012 | IOR12A0041 | 41335 | 41306 | receipts and payments | rents on land, house & others | | 5000 | | TRUE |
| 2012 | IOR12A0044 | 41339 | 41306 | gift and remittances | institutions | | 21000 | | TRUE |
| 2012 | IOR12A0044 | 41339 | 41306 | gift and remittances | institutions | | 21000 | | TRUE |
| 2012 | IOR12A0049 | 41369 | 41334 | savings and deposits | payment(chit fund & shg) | 100 | | | TRUE |
| 2012 | IOR12A0049 | 41369 | 41334 | savings and deposits | payment(chit fund & shg) | 100 | | | TRUE |
| 2012 | IOR12A0049 | 41222 | 41183 | savings and deposits | payment(chit fund & shg) | 100 | | | TRUE |
| 2012 | IOR12A0049 | 41222 | 41183 | savings and deposits | payment(chit fund & shg) | 100 | | | TRUE |
| 2013 | IOR13A0001 | 41761 | 41730 | savings and deposits | payments (chit funds and shg) | 100 | | | TRUE |
| 2013 | IOR13A0001 | 41761 | 41730 | receipts and payments | hired services (barber, washer man, etc.) | 60 | | | TRUE |
| 2013 | IOR13A0001 | 41761 | 41730 | savings and deposits | payments (chit funds and shg) | 100 | | | TRUE |
| 2013 | IOR13A0001 | 41761 | 41730 | receipts and payments | hired services (barber, washer man, etc.) | 60 | | | TRUE |
| 2013 | IJH13D0041 | 41513 | 41456 | savings and deposits | payments (chit funds and shg) | 80 | | | TRUE |
| 2013 | IJH13D0041 | 41513 | 41456 | savings and deposits | payments (chit funds and shg) | 80 | | | TRUE |
| 2013 | IJH13D0044 | 41508 | 41456 | savings and deposits | payments (chit funds and shg) | 40 | | | TRUE |
| 2013 | IJH13D0044 | 41508 | 41456 | savings and deposits | payments (chit funds and shg) | 40 | | | TRUE |
| 2013 | IJH13D0046 | 41508 | 41456 | savings and deposits | payments (chit funds and shg) | 40 | | | TRUE |
| 2013 | IJH13D0046 | 41508 | 41456 | savings and deposits | payments (chit funds and shg) | 40 | | | TRUE |
| 2013 | IJH13D0048 | 41505 | 41456 | savings and deposits | payments (chit funds and shg) | 80 | | | TRUE |
| 2013 | IJH13D0048 | 41505 | 41456 | savings and deposits | payments (chit funds and shg) | 80 | | | TRUE |
| 2013 | IJH13D0053 | 41510 | 41456 | savings and deposits | payments (chit funds and shg) | 40 | | | TRUE |
| 2013 | IJH13D0053 | 41510 | 41456 | savings and deposits | payments (chit funds and shg) | 40 | | | TRUE |

After rectifying the duplicates issue, the columns `amount_given, amount_received` were aggregated at across columns `hh_id, sur_mon_yr, fin_category, amount_spend_by`.

##### 2.3.3 Benefits from government programs

The benefits from government programs section of the Transaction schedule needs special care and attention in wrangling. The various issues that plague this dataset is that:

- Data or information collected for questions in this schedule is available only for SAT India region and for years 2010-2014. This data is stored under the "transactions" folder in raw data directory, typically, with the file name Ben_govt_prog.xlsx. Since these files are part of Transactions module, their frequency is month and resoltuion is household.
- However, for East India, data or information pertaining to this section of transactions schedule is absent. Instead, we have information collected as part of the Development Programs and Participation (July 2009 to June 2010) schedule (dev schedule henceforth), where the frequncy is year and resolution is household.
- Both these schedules ask whether the household has been benefitted by which government sponsored development program. How much was the amount of benefit received? Which household member was the direct beneficiary of the direct benefit transfer? The presence of these 3 fields makes SAT and East India data compatible to each other, for a data append across rows, if and olny if the SAT India values available for every month, is aggregated across years.
- In terms non-compatibility, we need to be aware that the dev schedule is far more exhaustive in terms of data (East India) than the transactions schedule (SAT India). The dev schedule colelcts information on type of ration cards possessed by the household and the number of programs addrssed is also nearly twice as in transactions schedule.

Hence, we have taken the follwoing measures to arrive at a consoildated data:

- The column `sur_mon_yr` stemming from SAT India was converetd to a date type column. It represents the month for whcih the governemnt benefit was recieved.
- The column `program_name` identifies each development program for which the household received benefits from the government. This column, when stripped of empty line spaces and converted to lower case, contains 812 unique strings. The 812 unique strings were mapepd to values mentioned in the dev schedule since it had all the programs mentioned in the transactions schedule and more. The [govt_ben_prog_map]() file was used to achieve this mapping and the values are available for reference.
- The column `amt_ben` whcih represents the amount of benecfit received by each household for every programhas been converted to a float data type.
- The data was grouped across columns `hh_id, program_name` and aggregated the `amt_ben` for each group. Teh daqta was then widened for further processing.

#### 2.4 Sale and purchase of capital Assets

The sale and purchase of capital assets section of the transactions schedule, colelcts information on the quantity, price and the total cost incurred or revenue generated from the purchase or sale of capital assets. The schedule lists out 10 categories or kinds of capital assets whcih need to be recorde. It also enquires about the person, place and how far away.

After performing the basic wrangling measures, we converetd the `sur_mon_yr` column, whcih identifies the month for which the transaction is mentioned, to date format. The column `item_category` was recoded to reflect the categories mentioned int he schedule.

It was notcied that files stemming from East india, has the information on distance to markets outside villlage, entered in two different column, such as `pur_dist` and `pur_pl_dist`. Similarly, `sold_dist` and `sold_pl_dist` have the same kind of information. On close inspection, for sales, the values in `sold_dist` seems more in number and meaningful. `sold_pl_dist` has only 5 observations. On the other hand `pur_pl_dist` has 156 observation and for the same observations `pur_dist` is missing. So we extrapolated the former on to the later, when the the latter is misisng for the 156 observations where the former is noon-missing.

The columns `pur_from, sold_to` represents the person or institution from or to whom the product was purchased or sold. The numeric codes were mapped to their categorical values mentioned in the schedule. In the column `pur_from` there are 5 observations with the value 0 which is beyond the schedule. Similarly, `sold_to` has the values -1 for on observation. These values have removed.

The required numeric columns `pur_cost, pur_dist, sold_cost, sold_dist, pur_qty, sold_qty` were converted to float data type. While attempting to do so, it was noticed that the column `sold_qty` had a rogue string value "Ac". So only the values which had digits where extracted and converted to float.

While inspecting for duplictates, it was noticed that excpet for the column `sur_mon_yr`, everything else is missing for the following 19 households from SAT India in 2013:

- IAP13B0037
- IAP13B0038
- IAP13B0257
- IAP13B0278
- IAP13C0003
- IAP13C0005
- IAP13C0006
- IAP13C0008
- IAP13C0030
- IAP13C0032
- IAP13C0038
- IAP13C0041
- IAP13C0046
- IAP13C0047
- IAP13C0054
- IAP13C0055
- IAP13C0059
- IAP13C0070
- IAP13C0200

Later, we identified the 12 observations which were duplicates and necessary action was taken to remove the duplicates. Attaching the duplicates here for reference:
| sur_yr | hh_id | dt_int | sur_mon_yr | item_category | item_pur_sold | pur_unit | pur_qty | pur_cost | pur_place | pur_place_ot | pur_dist | pur_from | pur_from_ot | sold_qty | sold_cost | sold_pl_dist | sold_place | sold_dist | sold_to | sold_to_ot | pur_pl_dist | sold_unit | dups |
|--------|------------|------------|------------|-------------------------|--------------------------------------------|--------------|---------|----------|------------|--------------|----------|----------|-------------|----------|-----------|--------------|------------|-----------|---------|------------|-------------|-----------|------|
| 2012 | IOR12A0037 | 05-04-2013 | 01-03-2013 | consumer durables | Consumer Durables | No | 1 | 500 | AINLATUNGA | | | Friend | | | | | | | | | | | TRUE |
| 2012 | IOR12A0037 | 05-04-2013 | 01-03-2013 | consumer durables | Consumer Durables | No | 1 | 500 | AINLATUNGA | | | Friend | | | | | | | | | | | TRUE |
| 2012 | IOR12D0036 | 30-10-2012 | 01-10-2012 | house or farm buildings | Material Purchased for House/Farm Building | | | 15000 | DHENKANAL | | 15 | Shop | | | | | | | | | | | TRUE |
| 2012 | IOR12D0036 | 30-10-2012 | 01-10-2012 | house or farm buildings | Material Purchased for House/Farm Building | | | 15000 | DHENKANAL | | 15 | Shop | | | | | | | | | | | TRUE |
| 2012 | IOR12D0044 | 06-11-2012 | 01-10-2012 | house or farm buildings | Material Purchased for House/Farm Building | | | 1500 | PANDUA | | 8 | Shop | | | | | | | | | | | TRUE |
| 2012 | IOR12D0044 | 06-11-2012 | 01-10-2012 | house or farm buildings | Material Purchased for House/Farm Building | | | 1500 | PANDUA | | 8 | Shop | | | | | | | | | | | TRUE |
| 2012 | IOR12D0045 | 07-11-2012 | 01-10-2012 | consumer durables | Consumer Durables | No | 1 | 200 | DHENKANAL | | 25 | Shop | | | | | | | | | | | TRUE |
| 2012 | IOR12D0045 | 07-11-2012 | 01-10-2012 | consumer durables | Consumer Durables | No | 1 | 200 | DHENKANAL | | 25 | Shop | | | | | | | | | | | TRUE |
| 2012 | IOR12D0054 | 05-11-2012 | 01-11-2012 | house or farm buildings | Material Purchased for House/Farm Building | | | 8000 | PANDUA | | 8 | Shop | | | | | | | | | | | TRUE |
| 2012 | IOR12D0054 | 05-11-2012 | 01-11-2012 | house or farm buildings | Material Purchased for House/Farm Building | | | 8000 | PANDUA | | 8 | Shop | | | | | | | | | | | TRUE |
| 2012 | IOR12D0059 | 12-11-2012 | 01-11-2012 | consumer durables | Consumer Durables | No | 1 | 600 | DHENKANAL | | 25 | Shop | | | | | | | | | | | TRUE |
| 2012 | IOR12D0059 | 12-11-2012 | 01-11-2012 | consumer durables | Consumer Durables | No | 1 | 600 | DHENKANAL | | 25 | Shop | | | | | | | | | | | TRUE |

Another aspect that requires attention is that the dataset is arranged in long format with items purchased and sold listed in column `item_category`. So any sort of data widening \(pivoting\) will require the numeric columns like `pur_cost` and `sold_cost` to be appended along row axis into a single column. This will ensure that with the help of an identifier column, which identifies each record as a purchase or sale, the numeric columns can be aggregated across index columns such as `hh_id`. Inorder to achieve this, the original dataset was split into two, where:

- columns `hh_id, sur_mon_yr, item_category, pur_from, pur_qty	pur_cost, pur_dist` will become the purchases data
- columns `hh_id, sur_mon_yr, item_category, sold_from, sold_qty	sold_cost, sold_dist` will become the sales data

Then, each dataset was further subsetted to remove all observations where all the numeric columns \(last 3 columns\) were missing together and thus ensuring that any sales related entry in the index columns \(first 4 columns\) for purchase data can be removed and vice-versa. An identifier column was also added to both the datsets caleld `pur_sold` which will hold the string "purchased" and "sold" for the purchases and sales data respectively. Now both these datasets were appended into a single dataframe.

The appended dataset was grouped across columns `hh_id, sur_mon_yr, pur_sold, 'item_category, from_whom` and the sum of quantity and cost and the mean of distance from village was calculated for each group. The data was widendened after aggregation across groups for further processing.

### 3. Cultivation Schedule (VDSA -Y)

The cultivation schdeule is a dedicated towards collecting information on the quantity, price, total value and the size of total production of main and subsidiary crops by each household. It takes into account the seasons, plots and crop varieties. The schedule is divided into two sections:

#### 3.1 Crop Cultivation

The data stemming from this section deals with crop cultivation by each household in each season at each plot they own. It measures the quantity, unit price and total value of production of main and subsidiary crops cultivated by each household.

The dataset conatins information on land ownership, rent etc which are also present in the Plotlist and Cropping Patterns schedule and the GES schedule. Hence it's decided to remove the following columns from the dataset: `irri_area, plot_ownership_status,	rent_val, rent_tenure`.

After performing the basic data wrangling measures, the numeric columns were converted to float data type. The cloumn `crop_variety_type` whcih identified whether the crop under consideration is local, hybrid or improved variety, has been mapped to the string values mentioned in the schedule.

We couldn't find any duplicate entries across columns. We can, prima facie, understand that the unique entry identifiers of this dataset are columns `hh_id, plot_code, season, crop_name, crop_variety_name`. The check for duplicates tagged 41 observations as duplicates when checked across the above mentioned columns. The duplicate entries are:

| sur_yr | hh_id      | plot_code | plot_area | season | crop_name | crop_variety_name | crop_variety_type | prct_area | op_main_prod_unit | op_main_prod_qty | op_main_prod_rate | op_by_prod_unit | op_by_prod_qty | op_by_prod_rate | op_ot_prod_unit | op_ot_prod_qty | op_ot_prod_rate | op_remarks | dups |
| ------ | ---------- | --------- | --------- | ------ | --------- | ----------------- | ----------------- | --------- | ----------------- | ---------------- | ----------------- | --------------- | -------------- | --------------- | --------------- | -------------- | --------------- | ---------- | ---- |
| 2010   | IBH10C0031 | C         | 0.15      | rabi   | wheat     | up262             | 2                 | 100       | Kg                | 25               | 12                | Qt              | 0.25           | 400             |                 |                |                 |            | TRUE |
| 2010   | IBH10C0031 | C         | 0.15      | rabi   | wheat     | up262             | 2                 | 100       |                   |                  |                   | Qt              | 0              | 0               |                 |                |                 |            | TRUE |
| 2011   | IBH11C0053 | A         | 0.25      | rabi   | wheat     | 234               | 1                 | 50        | Kg                | 30               | 30                | Qt              | 0.6            | 300             |                 |                |                 |            | TRUE |
| 2011   | IBH11C0053 | A         | 0.25      | rabi   | wheat     | 234               | 1                 | 50        | Kg                | 25               | 30                |                 |                |                 |                 |                |                 |            | TRUE |
| 2011   | IBH11C0053 | B         | 0.25      | rabi   | wheat     | 343               | 1                 | 50        | Kg                | 25               | 30                | Qt              | 0.6            | 300             |                 |                |                 |            | TRUE |
| 2011   | IBH11C0053 | B         | 0.25      | rabi   | wheat     | 343               | 1                 | 50        | Kg                | 28               | 30                |                 |                |                 |                 |                |                 |            | TRUE |
| 2011   | IBH11C0053 | C         | 0.25      | rabi   | wheat     | 343               | 1                 | 50        | Kg                | 20               | 30                | Qt              | 0.4            | 300             |                 |                |                 |            | TRUE |
| 2011   | IBH11C0053 | C         | 0.25      | rabi   | wheat     | 343               | 1                 | 50        | Kg                | 30               | 30                |                 |                |                 |                 |                |                 |            | TRUE |
| 2011   | IBH11C0053 | Q         | 0.4       | kharif | paddy     | sargu 52          | 1                 | 50        | Kg                | 500              | 10.8              | Qt              | 10             | 80              |                 |                |                 |            | TRUE |
| 2011   | IBH11C0053 | Q         | 0.4       | kharif | paddy     | sargu 52          | 1                 | 50        |                   |                  |                   |                 |                |                 |                 |                |                 |            | TRUE |
| 2011   | IBH11C0053 | Q         | 0.4       | kharif | paddy     | sargu 52          | 1                 | 100       | Kg                | 600              | 10.8              | Qt              | 11             | 80              |                 |                |                 |            | TRUE |
| 2011   | IBH11C0055 | FA        | 0.05      | kharif | paddy     | swarna            | 1                 | 30        |                   |                  |                   |                 |                |                 |                 |                |                 |            | TRUE |
| 2011   | IBH11C0055 | FA        | 0.05      | kharif | paddy     | swarna            | 1                 | 35        |                   |                  |                   |                 |                |                 |                 |                |                 |            | TRUE |
| 2013   | IBH13B0036 | D         | 0.1       | kharif | paddy     | mtv 7029          | 1                 | 100       |                   |                  |                   |                 |                |                 |                 |                |                 |            | TRUE |
| 2013   | IBH13B0036 | D         | 0.1       | kharif | paddy     | mtv 7029          | 1                 | 100       | Kg                | 150              | 15.6              | Qt              | 2              | 400             |                 |                |                 |            | TRUE |
| 2013   | IBH13B0041 | B         | 0.11      | kharif | paddy     | mtv 7029          | 1                 | 100       |                   |                  |                   |                 |                |                 |                 |                |                 |            | TRUE |
| 2013   | IBH13B0041 | B         | 0.11      | kharif | paddy     | mtv 7029          | 1                 | 100       | Kg                | 170              | 15.6              | Qt              | 2.5            | 400             |                 |                |                 |            | TRUE |
| 2013   | IBH13B0200 | B         | 0.11      | kharif | paddy     | mtv 7029          | 1                 | 100       |                   |                  |                   |                 |                |                 |                 |                |                 |            | TRUE |
| 2013   | IBH13B0200 | B         | 0.11      | kharif | paddy     | mtv 7029          | 1                 | 100       | Kg                | 150              | 15.6              | Qt              | 2.25           | 400             |                 |                |                 |            | TRUE |
| 2013   | IBH13C0032 | E         | 0.04      | kharif | paddy     | rajendra mansoory | 2                 | 100       |                   |                  |                   |                 |                |                 |                 |                |                 |            | TRUE |
| 2013   | IBH13C0032 | E         | 0.04      | kharif | paddy     | rajendra mansoory | 2                 | 100       | Kg                | 50               | 10                | Qt              | 0.7            | 70              |                 |                |                 |            | TRUE |
| 2013   | IBH13C0037 | F         | 0.04      | kharif | paddy     | rajendra mansoory | 2                 | 100       |                   |                  |                   |                 |                |                 |                 |                |                 |            | TRUE |
| 2013   | IBH13C0037 | F         | 0.04      | kharif | paddy     | rajendra mansoory | 2                 | 100       | Kg                | 60               | 10                | Qt              | 0.7            | 70              |                 |                |                 |            | TRUE |
| 2013   | IBH13C0048 | E         | 0.04      | kharif | paddy     | mansoory          | 2                 | 50        |                   |                  |                   |                 |                |                 |                 |                |                 |            | TRUE |
| 2013   | IBH13C0048 | E         | 0.04      | kharif | paddy     | mansoory          | 2                 | 100       | Kg                | 50               | 10                | Qt              | 0.6            | 70              |                 |                |                 |            | TRUE |
| 2013   | IBH13C0052 | L         | 0.05      | kharif | paddy     | 6444              | 2                 | 50        |                   |                  |                   |                 |                |                 |                 |                |                 |            | TRUE |
| 2013   | IBH13C0052 | L         | 0.05      | kharif | paddy     | 6444              | 2                 | 100       | Kg                | 80               | 10                | Qt              | 1              | 70              |                 |                |                 |            | TRUE |
| 2013   | IBH13C0055 | C         | 0.07      | kharif | paddy     | saryug-52         | 2                 | 40        |                   |                  |                   |                 |                |                 |                 |                |                 |            | TRUE |
| 2013   | IBH13C0055 | C         | 0.07      | kharif | paddy     | saryug-52         | 2                 | 100       | Kg                | 90               | 10                | Qt              | 1              | 70              |                 |                |                 |            | TRUE |
| 2013   | IBH13C0057 | F         | 0.03      | kharif | paddy     | swarna            | 2                 | 65        |                   |                  |                   |                 |                |                 |                 |                |                 |            | TRUE |
| 2013   | IBH13C0057 | F         | 0.03      | kharif | paddy     | swarna            | 2                 | 100       | Kg                | 15               | 10                | Qt              | 0.2            | 70              |                 |                |                 |            | TRUE |
| 2014   | IBH14C0201 | M         | 0.05      | kharif | paddy     | mansoory          | 2                 | 11        |                   |                  |                   |                 |                |                 |                 |                |                 |            | TRUE |
| 2014   | IBH14C0201 | M         | 0.05      | kharif | paddy     | mansoory          | 2                 | 84        | Kg                | 90               | 10                | Qt              | 1              | 200             |                 |                |                 |            | TRUE |
| 2014   | IOR14B0031 | B         | 0.4       | kharif | paddy     | swarna            | 2                 | 100       | Kg                | 700              | 11.2              | Qt              | 5              | 50              |                 |                |                 |            | TRUE |
| 2014   | IOR14B0031 | B         | 0.4       | kharif | paddy     | swarna            | 2                 | 100       | Kg                | 700              | 11.2              | Qt              | 6              | 50              |                 |                |                 |            | TRUE |
| 2014   | IOR14B0035 | A         | 1         | kharif | paddy     | pooja             | 1                 | 100       | Kg                | 2200             | 11.2              |                 |                |                 |                 |                |                 |            | TRUE |
| 2014   | IOR14B0035 | A         | 1         | kharif | paddy     | pooja             | 1                 | 100       | Kg                | 2200             | 11.2              | Qt              | 25             | 50              |                 |                |                 |            | TRUE |

These duplicate entries can only be removed by carefully selecting the parameters for each household separately and then removing the duplicate entry based on which amongst the entires \(for the household, plot, crop, crop variety and crop type\) have more misisng values. Such actions taken for households in the above atable are as follows:

- Household `IBH10C0031` producing wheat in plot C during rabi has 2 rows, where the second row is not adding any value to the data and hence determined as a duplicate and removed.

- Household `IBH11C0053` producing wheat in plots A, B and C during rabi season has 2 rows for each plot and each row has different value for the columns `op_main_prod_qty,	op_main_prod_rate` which identifies the quantity and per unit price of the primary crop cultivated. Hence all the rows were retained.

- Household `IBH11C0053` producing paddy in plot Q during kharif season has 3 rows, where the second row is not adding any value to the data and hence determined as a duplicate and removed.

- Household `IBH13B0036, IBH13B0041, IBH13B0200, IBH13C0032, IBH13C0037` producing paddy in plots D, B, B, E, F respectively during kharif season has 2 rows, where the first row is not adding any value to the data and hence determined as a duplicate and removed.

- Household `IBH11C0055, IBH13C0048, IBH13C0052, IBH13C0055, IBH13C0057, IBH14C0201` producing paddy in plots Q, E, L, C, F, M during kharif season has 2 rows, having different values in the `prct_area` column which identifies the portion of the total plot area which was used for cultivation that specific crop. These rows have misisng values in all other columns. Hence all the rows were retained.

- Household `IOR14B0031` producing paddy in plot B during kharif season has two rows, where the first row has a different value for the column `op_by_prod_qty` which identifies the quantity of the subsidiary crop cultivated. Hence all the rows were retained.

- Household `IOR14B0035` producing paddy in plot A during kharif has 2 rows, where the first row is not adding any value to the data and hence determined as a duplicate and removed.

In total we have identified and removed 8 rows.

For the remaining observations, it must be established that any analysis which we expect to conduct on the data will view this dataset not from the perspective of the crop types cultivated and not based on specific crop cultivated by the household. Having established same, we have grouped the dataset on the basis of `hh_id, plot_code, season` and type of crop cultivated. A new column `crop_type` was created after mapping the crop names existing in the dataset to a better and reduced naming system using the crop name mapper file [crop_names_map.json](). Then, the new names were furter mapped to their respective categories using the crop type mapper file [crop_type_map.json]().

The dataset was grouped on the basis of `hh_id, plot_code, season, crop_type, crop_variety_type`. After being grouped, the columns `prct_area	op_main_prod_qty,	op_by_prod_qty,	op_ot_prod_qty`, which provides information on the percentage of plot area used for cultivation, and quantity of primary, subsidiary and other crops cultivated respectively, were aggregated and columns `op_main_prod_rate, op_by_prod_rate,	op_ot_prod_rate`, which provides information on the per unit price of primary, subsidiary and other crops cultivated respectively, were averaged to better reflect the groups. Thus, the data was widened for further processing.

We also have information on the plot area used for cultivation, however, it will be better sourced from the plotlist and cropping pattern schedule.

#### 3.2 Inputs for Cultivation

The inputs for cultivation section of the cultivation schedule record information on the plot and its size, the quantity, rate and total value of human labour and material inputs used on the field and the operation performed using the inputs.

As part of the basic wrangling measures, we have decided to remove the plot name, survey round number and village name for these information fromn the GES schedule.

There are 485,814 observations in the data initially. The data contains multiple categorical varibales and numerical variables. As the first step, we cleaned and mapped the columns `season, lab_type, operations`, to values in the schedule, which corresponds to the season of operation, type of labour employed, type and source of the material used. The following measures were taken for:

- column `lab_type` we noticed 3 rogue values "0", "6" and "B" in 3 observations. These values fall beyond the values in the schedule and hence set to missing. Rest of the values were mapped to the respective categories.

- column `operations` had 1222 rogue values, which were cleaned re-classified into the following categories:

1. Harvesting
2. Irrigation
3. Fertilizing
4. Weeding
5. Sowing
6. Cleaning
7. Applying Pesticides
8. Land Preparation
9. Threshing
10. Sowing
11. Transplanting
12. Ploughing

There were no original categories mentioned in the schedule and hence the authors decided on the above categories.

Afetr cleaning the string columns, presence of duplicate entries were inspected. However, its is impossible to distinguis between duplicates across all columns becuase the housheold can employ two hired men to work on the same field on the same day at the same rate and there is no distinguisher in the data which potentially identifies this as a duplicate entry. So, all entries are assumed to be valid and taken into consideration for all the data wrangling processes which were implemented hence forth.

The data also had information on the type of labour hired for each operation, the kind of machinery used and source from which the machinery was procured. However, those information were ignored and instead the total cost incurred, in terms of labour and materials, for each operation was calculated from the dataset. The total labour cost was calculated using the per unit cost and number of units of labour hired. A new column `labour_cost` was created as the product of `work_hr, wage` and then aggregated across `hh_id, plot_code, season, operation` level to arrive at the total labour cost for each operation.

On the other hand, the value of each material used for for each operation was already provided in dataset. This, suppposedly, numeric column had a string value "\*\*\*\*\*\*\*\*\*\*" for household `IJH14B0048`. This value was removed and cast as missing. This column was aggregated at `hh_id, plot_code, season, operation` level.

### 4. Plot List and Cropping Pattern

The plot list and cropping pattern questionnaire collects information on the pieces of land owned, shared, leased in or out and mortgaged in and out by the agriculture households for a 5 years. It enquires about the crops cultivated in each piece of land, the total size of the land, the area of land which is irrigated and the any amount which is received or paid as rent for the land by the household.

The Plotlist dataset had issues with the column `hh_id`. This was resolved by isolating the household identifier from the existing identifier column. Strings columns, `ownership_status_plotlist` and `season` was cleaned to reflect categories mentioned in the questionnaire.

While dealing with duplicate entries in the plotlist dataset, the following steps were follwoed after carefully analysing the data and confirming findings via discreet manual inspection:

- The data had 43 observations which were exact replicas of another observation. These were identified using `duplicated` function in Python package called Pandas, by running it across all the columns in the dataset. These 43 duplicate observations were removed.

- Next we used the same function to identify using a subset of index columns: `hh_id, plot_name, plot_code, sub_plot_code, ownership_status_plotlist, season, crop_1, crop_2, crop_3, crop_4, crop_5`. We identified 30 observations which have duplicates. Out of these 30 observations, the following households had duplicates where the the value in the `plot_rent_received_paid` column was missing.
  | Plot code | Plot sub code | household ID |
  |---|---|---------|
  | I | | IBH12B0047 |
  | D | D | IBH14A0031 |
  | E | E | IBH14A0031 |
  | E | E | IBH14A0033 |
  | H | H | IBH14A0033 |
  | G | G | IBH14A0033 |
  | D | D | IBH14A0034 |
  | E | E | IBH14A0034 |
  | E | E | IBH14A0040 |
  | I | I | IBH14A0040 |
  | H | H | IBH14A0044 |
  | C | C | IBH14A0047 |
  | G | G | IBH14A0050 |
  | J | J | IBH14A0052 |
  | K | K | IBH14A0052 |
  | G | G | IBH14A0054 |
  | Q | Q | IBH14A0055 |
  | R | R | IBH14A0055 |
  | S | S | IBH14A0055 |
  | J | J | IBH14A0057 |
  | H | H | IBH14A0080 |
  | I | I | IBH14A0080 |
  | C | C | IBH14C0041 |

So removing the duplicates for these sub-plots. Post that the following were the duplicate entries:

| sur_yr | plot_name       | plot_code | plot_area | ownership_status_plotlist | sub_plot_code | crop_area | irri_area | season            | crop_1        | crop_2 | crop_3 | crop_4 | crop_5 | plot_rent_received_paid | hh_id      | dups |
| ------ | --------------- | --------- | --------- | ------------------------- | ------------- | --------- | --------- | ----------------- | ------------- | ------ | ------ | ------ | ------ | ----------------------- | ---------- | ---- |
| 2010   | ERIKILODI CHENU | F         | 2.5       | Leased-in on fixed rent   | FA            | 1.25      | 0         | Rainy (Kharif)    | PIGEONPEA     |        |        |        |        | 1334                    | IAP10D0057 | TRUE |
| 2010   | ERIKILODI CHENU | F         | 2.5       | Leased-in on fixed rent   | FA            | 1.25      | 0         | Rainy (Kharif)    | PIGEONPEA     |        |        |        |        | 1000                    | IAP10D0057 | TRUE |
| 2010   | BAS WALA        | A         | 0.75      | Own land                  |               | 0.03      | 0.75      | Rainy (Kharif)    | Paddy         |        |        |        |        |                         | IBH10C0040 | TRUE |
| 2010   | BAS WALA        | A         | 0.75      | Own land                  |               | 0.15      | 0.75      | Rainy (Kharif)    | Paddy         |        |        |        |        |                         | IBH10C0040 | TRUE |
| 2012   | GAMBHIR BABA    | H         | 0.07      | Own land                  |               | 0.07      |           | Perennial         | Teak (Sagwan) |        |        |        |        |                         | IBH12A0033 | TRUE |
| 2012   | GAMBHIR BABA    | H         | 0.07      | Own land                  |               | 0.07      | 0.07      | Perennial         | Teak (Sagwan) |        |        |        |        |                         | IBH12A0033 | TRUE |
| 2012   | BANS TAR        | E         | 0.05      | Own land                  |               | 0.05      |           | Perennial         | Bamboo        |        |        |        |        |                         | IBH12A0034 | TRUE |
| 2012   | BANS TAR        | E         | 0.05      | Own land                  |               |           |           | Perennial         | Bamboo        |        |        |        |        |                         | IBH12A0034 | TRUE |
| 2014   | BENGA BADH      | H         | 0.65      | Leased-out on crop share  | H             |           |           | Post rainy (Rabi) |               |        |        |        |        | 2600                    | IBH14D0056 | TRUE |
| 2014   | BENGA BADH      | H         | 0.65      | Leased-out on crop share  | H             |           |           | Post rainy (Rabi) |               |        |        |        |        | 2650                    | IBH14D0056 | TRUE |
| 2013   | RASTAVALU       | C         | 0.5       | Own land                  | C             | 0.5       | 0         | Perennial         | TEAK          |        |        |        |        |                         | IGJ13B0046 | TRUE |
| 2013   | RASTAVALU       | C         | 0.5       | Own land                  | C             | 0.5       | 0.5       | Perennial         | TEAK          |        |        |        |        |                         | IGJ13B0046 | TRUE |
| 2011   | SARNA DON       | L         | 0.1       | Mortgaged-in              | L             |           |           | Post rainy (Rabi) | Fallow        |        |        |        |        |                         | IJH11D0044 | TRUE |
| 2011   | SARNA DON       | L         | 0.1       | Mortgaged-in              | L             | 0.1       |           | Post rainy (Rabi) | Fallow        |        |        |        |        |                         | IJH11D0044 | TRUE |

From the above data subset, it's observed that households `IBH12A0033`, `IBH12A0034`, `IGJ13B0046` and `IJH11D0044` have duplicates but certain missing values in columns `crop_area` and `plot_area` distinguishes them. We have decided to retain rows which has minimall missing observations and remove the other.

The first filter removes rows where `hh_id` is equal to `"IBH12A0033"`, `plot_code` is equal to `"H"`, and `irri_area` is NaN.

The second filter removes rows where `hh_id` is equal to `"IBH12A0034"`, `plot_code` is equal to `"E"`, and `crop_area` is NaN.

The third filter removes rows where `hh_id` is equal to `"IGJ13B0046"`, `plot_code` is equal to `"C"`, and `irri_area` is equal to `0`.

The fourth filter removes rows where `hh_id` is equal to `"IJH11D0044"`, `plot_code` is equal to `"L"`, and `crop_area` is NaN.

The remaining cases belong to households `IAP10D0057`, `IBH10C0040`, and `IBH14D0056`. In `IBH10C0040` both the rows are eaxct duplicates except for the `crop_area` which displays two different values. This could be information regarding two crops and hence, the same same will be replaced by the sum of the two values, which is 0.18 (0.03+0.15).
However for the other two households, we have different values distinguishing the prospective duplicates in the `plot_rent_received_paid` column. We suspect that the rent being different is sussgestive of income from crop cultivation and hence these values would be replaced with the sum of existing values. That is:

- For household `IAP10D0057`, rent would be 1334 + 1000 = 2334
- For household `IBH14D0056`, rent would be 2600 + 2650 = 5250

Post all the above duplicates-related data cleaning process, the following data snapshot, with 6 entries, exists and one is the exact replica of the other. Hence, they will be removed.

| sur_yr | plot_name       | plot_code | plot_area   | ownership_status_plotlist | sub_plot_code | crop_area | irri_area | season            | crop_1    | crop_2 | crop_3 | crop_4 | crop_5 | plot_rent_received_paid | hh_id      | dups |
| ------ | --------------- | --------- | ----------- | ------------------------- | ------------- | --------- | --------- | ----------------- | --------- | ------ | ------ | ------ | ------ | ----------------------- | ---------- | ---- |
| 2010   | ERIKILODI CHENU | F         | 2.5         | Leased-in on fixed rent   | FA            | 1.25      | 0         | Rainy (Kharif)    | PIGEONPEA |        |        |        |        | 2334                    | IAP10D0057 | TRUE |
| 2010   | ERIKILODI CHENU | F         | 2.5         | Leased-in on fixed rent   | FA            | 1.25      | 0         | Rainy (Kharif)    | PIGEONPEA |        |        |        |        | 2334                    | IAP10D0057 | TRUE |
| 2010   | BAS WALA        | A         | 0.75        | Own land                  |               | 0.18      | 0.75      | Rainy (Kharif)    | Paddy     |        |        |        |        |                         | IBH10C0040 | TRUE |
| 2010   | BAS WALA        | A         | 0.75        | Own land                  |               | 0.18      | 0.75      | Rainy (Kharif)    | Paddy     |        |        |        |        |                         | IBH10C0040 | TRUE |
| 2014   | BENGA BADH      | H         | 0.649999976 | Leased-out on crop share  | H             |           |           | Post rainy (Rabi) |           |        |        |        |        | 5250                    | IBH14D0056 | TRUE |
| 2014   | BENGA BADH      | H         | 0.649999976 | Leased-out on crop share  | H             |           |           | Post rainy (Rabi) |           |        |        |        |        | 5250                    | IBH14D0056 | TRUE |

There are 56 entires stemming from 2014 raw data file, specifically for households in Odisha, where the column `crop_5` contains numeric values instead of strings \(crop names\). Whenever, digits occur in `crop_5`, `plot_rent_received_paid` is blank. So these vales in `crop_5` will be extrapolated to their corresposnding positions in `plot_rent_received_paid`.

The crop names are spread across 5 crop name columns. There are around 348 rogue crop names which vary across spellings and even includes regional names. These rougue string values are mapped to their respective english names and available at [crop_names_map.json]() and later mapped to their crop types and available at [crop_type_map.json](). Once the crop type has been mapped, we checked for duplicates again across all columns in the dataset and found the following 24 observations:

| sur_yr | plot_name       | plot_code | plot_area   | ownership_status_plotlist | sub_plot_code | crop_area   | irri_area   | season         | crop_1       | crop_2 | crop_3 | crop_4 | crop_5 | plot_rent_received_paid | hh_id      | dups |
| ------ | --------------- | --------- | ----------- | ------------------------- | ------------- | ----------- | ----------- | -------------- | ------------ | ------ | ------ | ------ | ------ | ----------------------- | ---------- | ---- |
| 2014   | NAHAR PAR       | H         | 0.039999999 | Own land                  | H             | 0.039999999 |             | Perennial      | Timber Trees |        |        |        |        |                         | IBH14A0035 | TRUE |
| 2014   | DEVI STHAN      | W         | 0.079999998 | Own land                  | W             | 0.079999998 |             | Perennial      | Timber Trees |        |        |        |        |                         | IBH14A0059 | TRUE |
| 2014   | NAHAR PAR       | H         | 0.039999999 | Own land                  | H             | 0.039999999 |             | Perennial      | Timber Trees |        |        |        |        |                         | IBH14A0035 | TRUE |
| 2014   | DEVI STHAN      | W         | 0.079999998 | Own land                  | W             | 0.079999998 |             | Perennial      | Timber Trees |        |        |        |        |                         | IBH14A0059 | TRUE |
| 2010   | GHARCHESHET     | B         | 3           | Own land                  | BA            | 1.25        | 1.25        | Perennial      | Fruits       |        |        |        |        |                         | IMH10D0312 | TRUE |
| 2010   | GHARCHESHET     | B         | 3           | Own land                  | BA            | 1.25        | 1.25        | Perennial      | Fruits       |        |        |        |        |                         | IMH10D0312 | TRUE |
| 2012   | DARWAZE PAR     | E         | 0.05        | Own land                  |               | 0.05        | 0.05        | Perennial      | Timber Trees |        |        |        |        |                         | IBH12A0033 | TRUE |
| 2012   | DARWAZE PAR     | E         | 0.05        | Own land                  |               | 0.05        | 0.05        | Perennial      | Timber Trees |        |        |        |        |                         | IBH12A0033 | TRUE |
| 2012   | MIYA BAGICHA    | C         | 0.31        | Own land                  |               | 0.31        | 0.31        | Rainy (Kharif) | Cereals      |        |        |        |        |                         | IBH12B0039 | TRUE |
| 2012   | MIYA BAGICHA    | C         | 0.31        | Own land                  |               | 0.31        | 0.31        | Rainy (Kharif) | Cereals      |        |        |        |        |                         | IBH12B0039 | TRUE |
| 2012   | UTTAR BHAR      | B         | 0.19        | Own land                  |               | 0.19        | 0.19        | Rainy (Kharif) | Cereals      |        |        |        |        |                         | IBH12B0040 | TRUE |
| 2012   | UTTAR BHAR      | B         | 0.19        | Own land                  |               | 0.19        | 0.19        | Rainy (Kharif) | Cereals      |        |        |        |        |                         | IBH12B0040 | TRUE |
| 2012   | DEVI ASTHAN     | B         | 0.22        | Own land                  |               | 0.22        | 0.22        | Rainy (Kharif) | Cereals      |        |        |        |        |                         | IBH12B0041 | TRUE |
| 2012   | DEVI ASTHAN     | B         | 0.22        | Own land                  |               | 0.22        | 0.22        | Rainy (Kharif) | Cereals      |        |        |        |        |                         | IBH12B0041 | TRUE |
| 2012   | HASUR TANR      | E         |             | Own land                  | EA            | 0.13        |             | Rainy (Kharif) | Pulses       |        |        |        |        |                         | IJH12D0036 | TRUE |
| 2012   | HASUR TANR      | E         |             | Own land                  | EA            | 0.13        |             | Rainy (Kharif) | Pulses       |        |        |        |        |                         | IJH12D0036 | TRUE |
| 2013   | Ghoghar Nal Par | B         |             | Own land                  | B             | 0.100000001 | 0.100000001 | Rainy (Kharif) | Cereals      |        |        |        |        |                         | IBH13A0037 | TRUE |
| 2013   | Ghoghar Nal Par | B         |             | Own land                  | B             | 0.100000001 | 0.100000001 | Rainy (Kharif) | Cereals      |        |        |        |        |                         | IBH13A0037 | TRUE |
| 2013   | Rahi Par        | A         |             | Own land                  | AA            | 0.02        | 0.02        | Rainy (Kharif) | Cereals      |        |        |        |        |                         | IBH13C0010 | TRUE |
| 2013   | Rahi Par        | A         |             | Own land                  | AA            | 0.02        | 0.02        | Rainy (Kharif) | Cereals      |        |        |        |        |                         | IBH13C0010 | TRUE |
| 2013   | Najir Wala      | F         |             | Own land                  | F             | 0.039999999 | 0.039999999 | Rainy (Kharif) | Cereals      |        |        |        |        |                         | IBH13C0037 | TRUE |
| 2013   | Najir Wala      | F         |             | Own land                  | F             | 0.039999999 | 0.039999999 | Rainy (Kharif) | Cereals      |        |        |        |        |                         | IBH13C0037 | TRUE |
| 2013   | Bhitha Ghar     | L         |             | Own land                  | L             | 0.050000001 | 0.050000001 | Rainy (Kharif) | Cereals      |        |        |        |        |                         | IBH13C0052 | TRUE |
| 2013   | Bhitha Ghar     | L         |             | Own land                  | L             | 0.050000001 | 0.050000001 | Rainy (Kharif) | Cereals      |        |        |        |        |                         | IBH13C0052 | TRUE |

We believe, positively, that these duplicates arise because the enumerator, listed multiple crops cultivated together in the same plot in the same season instead of writing it in the `crop_2` column. Since these crops belong to the same category cultivates in the same plot of the same housheold, these duplicates \(12 observations\) can be removed. Later, another round of duplication check was conducted based on columns `hh_id, plot_name, plot_code, sub_plot_code, ownership_status_plotlist, season, crop_1_type, crop_2_type, crop_3_type, crop_4_type, crop_5_type`. The following 36 observations were flagged:
| sur_yr | plot_name | plot_code | plot_area | ownership_status_plotlist | sub_plot_code | crop_area | irri_area | season | crop_1 | crop_2 | crop_3 | crop_4 | crop_5 | plot_rent_received_paid | hh_id | crop_1_type | crop_2_type | crop_3_type | crop_4_type | crop_5_type | dups |
|--------|--------------------------|-----------|-------------|---------------------------|---------------|-------------|-------------|-------------------|-------------|--------|--------|--------|--------|-------------------------|------------|-------------|-------------|-------------|-------------|-------------|------|
| 2012 | MASTER GHAR NEAR | F | 0.13 | Own land | | 0.13 | 0.13 | Rainy (Kharif) | Rice | | | | | | IBH12C0059 | Cereals | | | | | TRUE |
| 2012 | MASTER GHAR NEAR | F | 0.13 | Own land | | 0.1 | 0.1 | Rainy (Kharif) | Rice | | | | | | IBH12C0059 | Cereals | | | | | TRUE |
| 2014 | BAGICHA | E | 0.100000001 | Own land | E | 0.1 | 0.1 | Perennial | Other | | | | | | IBH14B0036 | Fallow | | | | | TRUE |
| 2014 | BAGICHA | E | 0.100000001 | Own land | E | 0.1 | | Perennial | Fallow | | | | | | IBH14B0036 | Fallow | | | | | TRUE |
| 2014 | BAGICHA | D | 0.310000002 | Own land | D | 0.31 | 0.31 | Perennial | Fallow | | | | | | IBH14B0043 | Fallow | | | | | TRUE |
| 2014 | BAGICHA | D | 0.310000002 | Own land | D | | | Perennial | Fallow | | | | | | IBH14B0043 | Fallow | | | | | TRUE |
| 2014 | BAGICHA | D | 0.31 | Own land | D | 0.31 | 0.310000002 | Perennial | Fallow | | | | | | IBH14B0045 | Fallow | | | | | TRUE |
| 2014 | BAGICHA | D | 0.310000002 | Own land | D | | | Perennial | Fallow | | | | | | IBH14B0045 | Fallow | | | | | TRUE |
| 2014 | BAGICHA | E | 1 | Own land | E | 1 | 1 | Perennial | Other | | | | | | IBH14B0059 | Fallow | | | | | TRUE |
| 2014 | BAGICHA | E | 1 | Own land | E | 1 | | Perennial | Fallow | | | | | | IBH14B0059 | Fallow | | | | | TRUE |
| 2014 | GACHHI | F | 0.050000001 | Own land | F | 0.050000001 | 0.050000001 | Perennial | Mango | | | | | | IBH14C0034 | Fruits | | | | | TRUE |
| 2014 | GACHHI | F | 0.050000001 | Own land | F | 0.050000001 | 0.05 | Perennial | Mango | | | | | | IBH14C0034 | Fruits | | | | | TRUE |
| 2014 | BABURWANI | F | 0.02 | Own land | F | 0.02 | 0.02 | Perennial | Other | | | | | | IBH14C0038 | Fallow | | | | | TRUE |
| 2014 | BABURWANI | F | 0.02 | Own land | F | 0.02 | 0.02 | Perennial | Fallow | | | | | | IBH14C0038 | Fallow | | | | | TRUE |
| 2014 | GACHHI | F | 0.100000001 | Own land | F | 0.100000001 | 0.100000001 | Perennial | Mango | | | | | | IBH14C0039 | Fruits | | | | | TRUE |
| 2014 | GACHHI | F | 0.100000001 | Own land | F | 0.100000001 | 0.1 | Perennial | Mango | | | | | | IBH14C0039 | Fruits | | | | | TRUE |
| 2014 | RAHI PAR | A | 0.349999994 | Own land | A | 0.349999994 | 0.349999994 | Perennial | Mango | Other | | | | | IBH14C0043 | Fruits | Fallow | | | | TRUE |
| 2014 | RAHI PAR | A | 0.349999994 | Own land | A | 0.349999994 | 0.35 | Perennial | Mango | Fallow | | | | | IBH14C0043 | Fruits | Fallow | | | | TRUE |
| 2014 | GACHHI PAR WALA | H | 0.119999997 | Own land | H | 0.119999997 | 0.119999997 | Perennial | Mango | Other | | | | | IBH14C0047 | Fruits | Fallow | | | | TRUE |
| 2014 | GACHHI PAR WALA | H | 0.119999997 | Own land | H | 0.119999997 | 0.12 | Perennial | Mango | Other | | | | | IBH14C0047 | Fruits | Fallow | | | | TRUE |
| 2014 | DIH GACHHI | I | 0.150000006 | Own land | I | 0.150000006 | 0.150000006 | Perennial | Mango | | | | | | IBH14C0054 | Fruits | | | | | TRUE |
| 2014 | DIH GACHHI | I | 0.150000006 | Own land | I | 0.059999999 | 0.06 | Perennial | Mango | | | | | | IBH14C0054 | Fruits | | | | | TRUE |
| 2014 | GACHHI | K | 0.200000003 | Own land | K | 0.200000003 | 0.200000003 | Perennial | Mango | Other | | | | | IBH14C0058 | Fruits | Fallow | | | | TRUE |
| 2014 | GACHHI | K | 0.200000003 | Own land | K | 0.200000003 | 0.2 | Perennial | Mango | Fallow | | | | | IBH14C0058 | Fruits | Fallow | | | | TRUE |
| 2014 | GACHHI AAM WALA | G | 0.150000006 | Own land | G | 0.150000006 | 0.150000006 | Perennial | Mango | | | | | | IBH14C0200 | Fruits | | | | | TRUE |
| 2014 | GACHHI AAM WALA | G | 0.150000006 | Own land | G | 0.150000006 | 0.15 | Perennial | Mango | | | | | | IBH14C0200 | Fruits | | | | | TRUE |
| 2014 | MIYA PASCHIM | C | 0.029999999 | Own land | C | 0.029999999 | 0.029999999 | Perennial | Mango | | | | | | IBH14C0201 | Fruits | | | | | TRUE |
| 2014 | MIYA PASCHIM | C | 0.029999999 | Own land | C | 0.029999999 | 0.03 | Perennial | Mango | | | | | | IBH14C0201 | Fruits | | | | | TRUE |
| 2014 | MIYA PASCHIM | C | 0.039999999 | Own land | C | 0.039999999 | 0.039999999 | Perennial | Mango | | | | | | IBH14C0202 | Fruits | | | | | TRUE |
| 2014 | MIYA PASCHIM | C | 0.039999999 | Own land | C | 0.039999999 | 0.04 | Perennial | Mango | | | | | | IBH14C0202 | Fruits | | | | | TRUE |
| 2012 | HASUR TANR | E | | Own land | EA | 0.13 | | Rainy (Kharif) | Black gram | | | | | | IJH12D0036 | Pulses | | | | | TRUE |
| 2012 | HASUR TANR | E | | Own land | EA | 0.13 | | Rainy (Kharif) | Horse gram | | | | | | IJH12D0036 | Pulses | | | | | TRUE |
| 2010 | GHARCHESHET | B | 3 | Own land | BA | 1.25 | 1.25 | Perennial | Pomegranate | | | | | | IMH10D0312 | Fruits | | | | | TRUE |
| 2010 | GHARCHESHET | B | 3 | Own land | BA | 1.25 | 1.25 | Perennial | Berries | | | | | | IMH10D0312 | Fruits | | | | | TRUE |
| 2013 | Baraha Kani | A | | Own land | | 1 | 0 | Post rainy (Rabi) | Chickpea | | | | | | IOR13B0203 | Pulses | | | | | TRUE |
| 2013 | Baraha Kani | A | | Own land | | 2 | 0 | Post rainy (Rabi) | Black gram | | | | | | IOR13B0203 | Pulses | | | | | TRUE |

Out of the above, we will be specifically handling the households as the following:

- Household `IBH12C0059` have same crop name from the same category and diferent values in the `crop_area` and `plot_area` columns distinguishing them. However, row one shows that the total crop area beig used for rice cultivation. Hence the second row is covered and will be removed.

- Households `IBH14B0036` and `IBH14B0059` have different crop names \(Fallow and Other\) but the second row contains a missing value and hecne the first row, since it provide more information, will have more weightage to be retained.

- Households `IBH14B0043` and `IBH14B0045` have same crop names of the same cropt type but in row 2, the `crop_area` and `plot_area` columns are missing and moreover, crop in row 1 covers the entire plot area. Hence row 1 will be retained.

- Household `IBH14C0054` has the same crop but row one indicates cultivation of mangoes for the entire plot area and row 2 is assumed to be only a subset of row 1. Hence, row 2 will be removed.

- Household `IOR13B0203` doesn't mention the total plot area and has different crops cultivated in different `crop_area` values. We inspected whether the same housheold mentions `plot_area` in any other years and found that in 2014, the same household `IOR14B0203` marks a `plot_area` of 2. Hence, row 2 of the household is decided to be retained.

- Household `IBH14C0038` both rows are exact replicas except for crop name. Since Fallow is better defined that Others in `crop_1`, the row 1 will be removed.

For the households:

- IBH14C0034
- IBH14C0039
- IBH14C0043
- IBH14C0047
- IBH14C0058
- IBH14C0200
- IBH14C0201
- IBH14C0202
  can observe that the differences between duplicates arise from the float values in `irri_area`. so row 2 of all the above households will be removed. Household `IJH12D0036` and `IMH10D0312` have different crops but numeric values in `plot_area`, `crop_area` and `irri_area`is the same. So, row 2 will be removed to get a unique value.

Now that all duplicates are removed, we will proceed to widening the dataframe. To reduce the dimensionality involved, we can remove the `plot_name` column. This can be achieved by grouping by all the string columns except plot name. We have manually inspected these rows and they are similar in all except for the plot name. So a `grouby.agg` fucntionality of `Pandas` package will achieve the desired the result.
