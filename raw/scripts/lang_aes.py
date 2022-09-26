"""This script adds AES values to the etc/languages.tsv"""
import pandas as pd

langs = pd.read_csv('etc/languages.tsv', sep='\t')
aes = pd.read_csv('raw/others/aes.csv', sep=',')

aes['Code_ID'] = aes.Code_ID.str.replace('aes-', '')
aes_stat = aes[['Language_ID', 'Code_ID']]
aes_stat = aes_stat.rename(columns={"Code_ID": "aes"})

lang_combined = langs.merge(
    aes_stat,
    left_on='Glottocode',
    right_on='Language_ID',
    how='left'
    )
lang_final = lang_combined.drop(columns=lang_combined.columns[[-2]])

lang_final.to_csv('etc/languages.tsv', sep=',', index=False)
