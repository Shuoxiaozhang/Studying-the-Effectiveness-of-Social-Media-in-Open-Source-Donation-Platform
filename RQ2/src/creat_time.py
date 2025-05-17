import json
import csv

# Load the JSON data from the file with the correct encoding
with open('E:/bishe/newdata/collectiveinfo/fixed_time.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Prepare a list to store the rows for the CSV
rows = []

# Loop through the data and extract "slug" and "createdAt"
for entry in data:
    # Accessing nested data: 'slug' and 'createdAt' are inside 'data' -> 'collective'
    collective = entry.get('data', {}).get('collective', {})
    slug = collective.get('slug')
    created_at = collective.get('createdAt')

    if slug and created_at:
        rows.append({'slug': slug, 'createdAt': created_at})

# Write the data to a CSV file
with open('collective_created_time.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['slug', 'createdAt']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("CSV file has been created successfully.")
