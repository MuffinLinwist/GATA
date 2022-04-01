import pandas as pd

ind_data = pd.read_csv('cldf_test/raw/gata_raw.csv', sep = ',', index_col = 0)

filtered = ind_data.groupby(['Parameter','Value']).size().reset_index().rename(columns={0:'count'})

filtered.to_csv("cldf_test/raw/others/unique_vals.csv")