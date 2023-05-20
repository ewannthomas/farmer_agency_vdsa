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

### General Endowments Schedule

#### Household Member Schedule (VDSA – C)

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

#### Landholding information (VDSA – D)

The landholding information schedule of the GES questionnaire enquires about information on who owns the land and unique identifiers for the plots. It identifies the various sources from whcih each plot is irrigated, soil depth, soil type, revenue from the land etc. The schdeule provides very exhaustive information on the soil conditions and land type of the plot. The identifiers used, `plot_code` is equivalent to the identifier used in the Plotlist and Cropping Patterns questionnaire of VDSA. So, the values are comparable.

The duplicates were checked on columns `hh_id`, `sl_no`, and `plot_code`. There were no duplicates.
Later, all columns which had numeric values were converted to float data type. Teh column `plot_name` was removed because `plot_code` enabled identification of the rows uniquely. Columns on ownership status, change of ownership status, source of irrigation, soil type, fertility and degradation, bunding and bunding type were reassigned to their corrsponding string based vategory values as in the questionnaire. Columns which housed values beyond any defined category of any column was enetered as col_name_others. Such other column which had string values were removed fromthe datastet. e.g.: bund_type_others

#### Animal inventory of the Household (VDSA – E)

The animal inventory schedule of the GES questionnaire collects details about the kind, count, mode of acquisition and present value of livestock inventory owned by the household.

After exercising the basic wrangling measures, we inspected for duplicates across all columns in the dataset and found 2 entries,
| sur_yr | hh_id | livestock_type | livestock_count | no_of_rea | no_pur | no_rec_gift | no_sha_rea | livestock_present_value | remarks | dups |
|--------|------------|----------------|-----------------|-----------|--------|-------------|------------|-------------------------|---------|------|
| 2011 | IJH11C0037 | goats | 2 | 2 | | | | 1200 | | TRUE |
| 2011 | IJH11C0037 | goats | 2 | 2 | | | | 1200 | | TRUE |

One entry was removed to ensure unique identification of dataframe. Necessary column name renaming was done to make better sense of the column names.

The column `livestock_type` holding categories of livestock types had rogue string values which were recoded to reflect the categories mentioned in the questionnaire. Post mapping of categorical string values, the dataframe was grouped on the basis of household and livestock type columns \(`hh_id, livestock_type`\) and a sum of the subsequent count columns of livestock were obtained. Prior to grouping and summing all columns with numeric values `present_val, on_farm_reared_count, purchased_count, received_gift_count, shared_rearing_count` were necessarily converted to float data type.

#### Farm implements owned by the household (VDSA – F)

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

#### Building & consumer durables (VDSA – G)

The Building and consumer durables schedule under the GES questionnaire collects information on the building type owned by the household and details about the facilities available in the house. The facilities included the house involves the durables owned by the household. Data cleaning pertaining to this schedule has been, for ease of work, split into:

- Consumer Durables: Deals specifically with the count, present value of the durables owned by the household.
- Buildings: Deals specifically with the details of the house owned, the type of house and amenities built into the house.

##### Consumer Durables

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

##### Buildings

#### Stock inventory (VDSA – N)

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

#### Debt and Credit Schedule (VDSA – P)

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

#### Role of gender

The role of gender schedule of the GES questionnaire collects information from both women and men of the household abou their involvement in the decision making process of the household. It's divided into two sub sections:

##### Resource ownership and decision-making

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

##### Role of gender in crop cultivation

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

#### Sources of marketing and other information

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

#### Coping mechanisms

The coping mechanisms schedule of the GES questionnaire collects information from hosueholds related to the fact whether their livelihoods were affected by any severe drought/flood/pest/diseases/misfortunes. If yes, whether they received any support from the government. There are 4 parts to this schdeule:

##### Coping Mechanisms

##### Government Assistance

The governemnt assistance section enquires whether the household received any assistance from the government. And if yes, what is the assistance.

As per the data is concerned, this contains only information about households which received governemnet assistance. Moreover the there are mutiple households which recived multiple assistance during the same time period. Beyond that, the `assist_type` column, listing the assistance received by each household, conatins only string values and need some other processing method to make inferences out of it.

##### Reliability ranking

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

##### Proactive Measures

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

### Cultivation Schedule (VDSA -Y)

The cultivation schdeule is a dedicated towards collecting information on the quantity, price, total value and the size of total production of main and subsidiary crops by each household. It takes into account the seasons, plots and crop varieties. The schedule is divided into two sections:

#### Crop Cultivation

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

#### Inputs for Cultivation

### Plot List and Cropping Pattern

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
