import pandas as pd

# Load the existing CSV file
df = pd.read_csv('E:/bishe/data/collective/collectiveInfo/slug_flag_github.csv')

# Remove duplicates based on the 'slug' column, keeping the first occurrence
df_unique = df.drop_duplicates(subset=['slug'], keep='first')

# Save the cleaned data to a new CSV file
df_unique.to_csv('E:/bishe/data/collective/collectiveInfo/slug_flag_github_unique.csv', index=False)

print("CSV file with unique slugs has been created successfully.")
