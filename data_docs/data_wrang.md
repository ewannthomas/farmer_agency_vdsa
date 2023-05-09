# VDSA DATA WRANGLING DOCUMENTATION

## Panel Data Regression

## tSNE and Deep Learning

Basic wrangling exercises includ- Ensuring presence uniform column names for compatible datasets stemming from east-india and sat-india folders.

- Removing columns with all the entires as missing values.

### General Endowments Schedule

#### Debt and Credit Schedule (VDSA – P)

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

After mapping the categories, we identified certain cases where the same household was taking as loan or saving different amounts from the same source for the same purpose. There were 555 such entries in the data and they were grouped at a household, source and purpose level. Such grouped cases were aggregated (intra group) after estimating a blended interest for the respective amounts. Regarding the duration of such entries, the maximum duration, within group, of saving or loan among such entires were extrapolated.
