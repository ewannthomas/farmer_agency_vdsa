# GICC - Exploratory Data Analysis

The following is the total number of unique households surveyed in each year:

- 2010 : 1346
- 2011 : 1344
- 2012 : 1348
- 2013 : 1357
- 2014 : 1367

### Family Comp

In the household details section of the General Endowments Schdule (GES), the following households doesnot have a valid entry in the `relation` column to isolate the head of the household (code:1 - Head of Household):

- IJH10C0005
- IBH11B0008
- IBH11C0001
- IBH11C0005
- IBH11C0048
- IBH11C0057
- IJH11C0058
- IJH11D0049

So the total number of unique households in:

- 2010 : 1345
- 2011 : 1337

and the other years remain unchanged.

Similarly, in each year we have the following number of households where any member's relation to head is missing:

- 2010 : 111
- 2011 : 173
- 2012 : 144
- 2013 : 145
- 2014 : 182

# Creating Gender wise summary for GICC

## Merging Family Comp with Info ranking

# Does access to information and institutions by the household vary by caste of household head?

Step 1: Merged `Gen_info` dataset with `Info_ranking`. The merge stats are:

1. 314 unmerged households in `Gen_info`.
2. All households from `Info_ranking` were merged.
3. Both datasets had 1419 common households.

# Does households belonging to different castes adopt different coping mechanisms?

Step 1: Merged `Gen_info` dataset with `Cop_mech`. The merge stats are:

1. 637 unmerged households in `Gen_info`.
2. All households from `Cop_mech` were merged.
3. Both datasets had 889 common households.

# Does coping mechanism adopted by a household vary by the ownership status of land?
