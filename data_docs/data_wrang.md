# VDSA DATA WRANGLING DOCUMENTATION

The Village Dymanics Situation Assessment is a yearly panel dataset collected across 9 states in India between 2010 and 2014.

To replicate the results we generated, please clone the `farmers_agency_vdsa` git repository from `https://shorturl.at/rV178`. Post repository cloning, one may dowanload the necessary data from the VDSA data portal at `https://vdsa.icrisat.org/vdsa-database.aspx`

## Panel Data Regression

## tSNE and Deep Learning

Basic wrangling exercises includ- Ensuring presence uniform column names for compatible datasets stemming from east-india and sat-india folders.

- Removing columns with all the entires as missing values.

### General Endowments Schedule

#### Debt and Credit Schedule (VDSA – P)

- class: `VdsaMicrotSNE`
- method: `assests_liabs`

After performing the basic wrangling, the categoies of the `source` column has been identified to be 176. These rogue categories have been recoded into the categories as per the questionnaire. They ar- Co-operative banks

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

#### Farm implements owned by the household (VDSA – F)

- class: `VdsaMicrotSNE`
- method: `farm_equip`

The basic wrangling measures were followed by recoding of the `item_name` column which lists the name of the farm equipment owned by the household. The following were the equipments listed by the questionaire:

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
- Submersible pump 1
- Submersible pump 2
- Submersible pump 3
- Bullock cart
- Truck
- Other minor implements
- Mechanical thresher
- Electric motor 1
- Electric motor 2
- Electric motor 3
- Diesel pump set 1
- Diesel pump set 2
- Diesel pump set 3
- Pipeline in feet
- Combined harvester cum thresher
- Implements used for caste occupation
- Implements used for handy- craft
- Groundnut opener
- Bore-well or Open-well
- Others

However, the data contained around 237 rogue categories whcih varied widely in terms of string, spellings etc. All such rogue values were carefully checked and mapped to one of the values in the above list. The category mapping was followed by widening of the dataset. There are multiple households which own many number of the same equipment, some fully owned by the household and some shared at a percent of stake, as reported in the `prct_share` column. So these multiple number of the equipments at different stake act as duplicates of eachother. To resolve this we can make use of the `farm_equipment_present_value` column which, as per the documnetation, is the reported value of the implement as per the stake in the ownership. So to widen the dataset, the `prct_share` column can be ignored and the same equipments can be aggregated in terms of the number and its present value. For the column, `horse_power` recorded only for major machinery like tractor, thresher, and pumpset, we take the maximum value within the `item_name` category.
