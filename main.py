import pandas as pd
from planning_permission import check_planning_permission
import re

# Load the Excel file
file_path = './PlanningHubCodeChallenge.xlsx'

# these are columns retrieved using multi-indexing from the file
df_sheet2 = pd.read_excel(pd.ExcelFile(file_path), sheet_name='Sheet2', dtype=None, header=[1,2,4])
df_sheet2 = df_sheet2.replace('\n',' ', regex=True)
cleansed_rules = df_sheet2.dropna(how='all').reset_index(drop=True)

temp_columns = list(cleansed_rules.columns.values)
col_val =None

for idx,col in enumerate(temp_columns):
    for val in col:
        if re.match(r'(Restrictions)', val):
            col_val = 'Project Type'
            break
        elif re.match(r'(Details)', val):
            col_val = 'Details'
            break
        elif re.match(r'(\d+U\d+)', val):
            col_val = val + 'Universal'
            break
        elif re.match(r'(\d+A\d+)', val):
            col_val = val + 'Others'
            break 
        else:
            pass
    
    temp_columns[idx] = col_val
    
cleansed_rules.columns = temp_columns
pd.set_option("display.max_columns", None)

# Forward fill NaNs in Project_Type and Details
cleansed_rules['Project Type'] = cleansed_rules['Project Type'].ffill()
cleansed_rules['Details'] = cleansed_rules['Details'].ffill()
# print(cleansed_rules)

# Replace NaN values in Universal/Others columns with 'n'
rule_columns = [col for col in cleansed_rules.columns if 'Universal' in col or 'Others' in col]
cleansed_rules[rule_columns] = cleansed_rules[rule_columns].fillna('n')
# print(cleansed_rules)

# Check planning permission requirement for the below example cases

# project_type_input = "Height of gate, fence, wall"
# details_input = "above 1m"

# project_type_input = "fence"
# details_input = "above 1m"

project_type_input = "Height of gate"
details_input = "up to 1m"

# project_type_input = "Other"
# details_input = "New build"
 
result = check_planning_permission(cleansed_rules, project_type_input, details_input)
print(result) 
