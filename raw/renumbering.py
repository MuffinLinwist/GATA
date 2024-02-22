import csv

# Open the CSV file for reading and writing
with open('raw/gata_raw.csv', 'r') as file:
    reader = csv.reader(file)
    data = list(reader)

# Renumber the entries
for index, row in enumerate(data):
    row[0] = str(index + 1)

# Write the updated data back to the CSV file
with open('raw/gata_raw.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("Renumbering complete.")