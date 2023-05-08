# VDSA DATA WRANGLING DOCUMENTATION

## Panel Data Regression

## tSNE and Deep Learning

Basic wrangling exercises include:

- Ensuring presence uniform column names for compatible datasets stemming from east-india and sat-india folders.
- Removing columns with all missing values

### General Endowments Schedule

#### Debt and Credit Schedule (VDSA – P)

After performing the basic wrangling, the categoies of the `source` column has been identified to be 176. These rogue categories have been recoded into the categories as per the questionnaire. They are:

- Co-operative banks : 1
- Commercial banks : 2
- Grameen bank (RRB) : 3
- Friends & relatives : 4
- Finance companies : 5
- Employer : 6
- Landlord : 7
- Shopkeeper : 8
- Moneylender : 9
- Self-help groups : 10
- Commission agent : 11
- Input supplier : 12
- Others : 13

These categories were then mapped to the above mentioned numeric codes to facilitate DL operations.
