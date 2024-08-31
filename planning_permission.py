# Function to check if planning permission is required
def check_planning_permission(df, project_type, details, category_priority=('Universal', 'Others')):
    filtered_df = df[
        (df['Project Type'].notna()) & 
        (df['Details'].notna()) &
        (df['Project Type'].str.contains(project_type, case=False, na=False)) &
        (df['Details'].str.contains(details, case=False, na=False))
    ]

    if filtered_df.empty:
        return "No matching project type and details found."
    
    for category in category_priority:
        category_columns = [col for col in df.columns if category in col]
        if (filtered_df[category_columns] == 'y').any().any():
            return f"Planning permission is required due to {category} Category."
    
    return "Planning permission is not required."


