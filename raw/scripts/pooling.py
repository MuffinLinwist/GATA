"""Module pools all raw questionnaires to a single tsv-file."""
from pathlib import Path
import pandas as pd

files = list(Path("questionnaires").glob("*.ods"))
params = pd.read_csv(
    'cldf_test/etc/parameters.tsv',
    sep=',',
    index_col=0
    )
years = pd.read_csv(
    'cldf_test/raw/others/lang_sources.tsv',
    sep=',',
    index_col=0
    )
data = pd.DataFrame()

for f in files:
    lang_name = f.stem
    lang_name = lang_name.replace('_', '').replace('-', '').replace('ó', 'o')
    print(f"PROCESSING: {lang_name}")
    data_lang = pd.read_excel(f)
    data_lang["Language"] = lang_name
    data = data.append(data_lang, ignore_index=True)

data = data.drop(columns=data.columns[[0, 2, 12, 13, 14, 15, 16]])
data.columns.values[2] = "Certainty_1"
data.columns.values[6] = "Certainty_2"
data = data.rename(columns={
    "CARACTERISTICA": "Feature",
    "Estado 1": "State_1",
    "REFERENCIA": "Reference_1",
    "Comentarios": "Comments_1",
    "Estado 2": "State_2",
    "REFERENCIA.1": "Reference_2",
    "Comentarios.1": "Comments_2"
    })

data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)
params = params.applymap(lambda x: x.strip() if isinstance(x, str) else x)

lookup_prm = params[['Shortname', 'Description_esp']]

new_data = pd.merge(
    data,
    lookup_prm,
    left_on=data['Feature'].str.lower(),
    right_on=lookup_prm['Description_esp'].str.lower(),
    how='left'
    )
new_data = new_data.drop(columns=new_data.columns[[0, 1, -1]])
new_data.columns.values[-1] = "Parameter"

years['Year_1'] = years['Source_1'].str[-4:]
years['Year_2'] = years['Source_2'].str[-4:]

cols = ['Language', 'Parameter']
new_order = new_data[cols + [c for c in new_data.columns if c not in cols]]


def split_obs(dataframe):
    """Function provides a long format for data."""
    state_1 = dataframe.drop(columns=dataframe.columns[[6, 7, 8, 9, -1]])
    state_1 = pd.merge(
        state_1,
        years,
        left_on='Language',
        right_on='ID',
        how='left'
        )
    state_1 = state_1.drop(columns=state_1.columns[[-1, -3, -5]])
    state_1.columns = state_1.columns.str.replace(
        pat='_1',
        repl='',
        regex=True
        )

    state_2 = dataframe.drop(columns=dataframe.columns[[2, 3, 4, 5]])
    state_2 = pd.merge(
        state_2,
        years,
        left_on='Language',
        right_on='ID',
        how='left'
        )
    state_2 = state_2.drop(columns=state_2.columns[[-2, -4, -5]])
    state_2.columns = state_2.columns.str.replace(pat='_2', repl='', regex=True)

    full = state_1.append(state_2)
    full = full.rename(columns={"State": "Value"})
    full_order = full.sort_values(
        by=['Language', 'Parameter', 'Value'],
        ignore_index=True
        )

    return full_order


final = split_obs(new_order)

final['Value'] = final['Value'].astype(str)
final['Value'] = final.Value.str.replace('.0', '', regex=False)
final['Value'] = final.Value.str.replace('nan', 'NA', regex=False)
final['Value'] = final.Value.str.replace(r'^\s*$', 'NA', regex=True)
final['Value'] = final.Value.str.replace("ambos", 'both', regex=False)
final['Value'] = final.Value.str.replace("no hay orden básico", 'no basic word order', regex=False)
final['Value'] = final.Value.str.replace("GEN N", 'Gen N', regex=False)
final['Value'] = final.Value.str.replace("N GEN", 'N Gen', regex=False)
final['Value'] = final.Value.str.replace("Jerárquico", 'hierarchic', regex=False)
final['Value'] = final.Value.str.replace("activo-inactivo", 'active-inactive', regex=False)
final['Value'] = final.Value.str.replace("ergativo-absolutivo", 'ergative-absolutive', regex=False)
final['Value'] = final.Value.str.replace("neutro", 'neuter', regex=False)
final['Value'] = final.Value.str.replace("nominativo-acusativo", 'nominative-accusative', regex=False)
final['Value'] = final.Value.str.replace("tripartito", 'tripartite', regex=False)
final['Value'] = final.Value.str.replace("morfología y prosodia", 'morphology and prosody', regex=False)
final['Value'] = final.Value.str.replace("morfología", 'morphology', regex=False)
final['Value'] = final.Value.str.replace("prosodia", 'prosody', regex=False)

final['Certainty'] = final['Certainty'].astype(str)
final['Certainty'] = final.Certainty.str.replace('.0', '', regex=False)
final['Certainty'] = final.Certainty.str.replace('nan', 'NA', regex=False)
final['Certainty'] = final.Certainty.str.replace(r'^\s*$', 'NA', regex=True)

final = final.fillna('')
final.index += 1

final.to_csv('cldf_test/raw/gata_raw.csv', index_label="ID")
# params.to_csv('etc/parameters.tsv', sep = ",")
