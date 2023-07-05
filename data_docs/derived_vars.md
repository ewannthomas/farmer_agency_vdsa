# Derived Variables

## Total Production and Success

These varibales were created in two different forms:

- at household, crop type, year level
- at household, year level

The dataset in the "data/interim/tsne" folder with the name, `total_cult_crop.csv` is the former and `total_cult_yr.csv` is the latter.

### Total Production

The `crop_info_op` file contains variables mentioning the rate and quantity of produce created by each household in each year for different crop types. There are 3 different kinds of produce mentioned in the data, namely,

- Main product
- By product
- Other products

Using this information, we created the `total_prodn` variable which is the total monetary value of agricultural produce for each household for each crop type in each year and also for each household for each year.

For each household, we calculated:
Main product total production= Rate \* Quantity of main product
By product total production= Rate \* Quantity of by product
Other product total production= Rate \* Quantity of other product

Total Production= (Main product total production + By product total production + Other product total production)

### Success

From the `total_prodn` varibale, the first difference value (`diff`) for each year production was calculated. The variable `success` will take a value 1 if the total production for each crop type, or year in later case, in each housheold was increasing across years or all values in column `diff` was greater than zero. The inverse is case where success = 0.

Success variable was also assigned a value 1 (household is successful) if the household managed to produce the same output as of last year so that the first difference varibale (`diff`) was zero for that year. Similarly success, for households which had zero production across years and hecne the irst difference varibale (`diff`) was zero for all years, was assigned zero.

Apart from the generic framework, the success variable is filtered at the following levels:

- Crop Type: Out of 1238 households under consideration, the households who left their field idle or had a crop category "Fallow" was 278 households. These 278 households, for their fallow cases, didn't cutlivate any and were not assigned any value for success. Please be aware that apart from the fallow cases, these 278 households can have successful other agricultural produces apart from leaving some of their fields or parts of the fields fallow.

|            | Observations |
| ---------- | ------------ |
| All        | 11442        |
| Fallow     | 673          |
| Difference | 10679        |

- Number of years of production: Success was considered only for households which had a 2 or more consecutive years of cultivation for each crop type. If a household had only one year entry (or length of 1), success was assigned as missing and not considered.
