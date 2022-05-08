import io 
import re 
import json 
import pathlib
import itertools
import collections



from csvw import dsv 
from cldfbench import Dataset as BaseDataset
from cldfbench import CLDFSpec, Metadata
from clldutils.misc import data_url
from pycldf.sources import Source, Reference
from pybtex.database import parse_string




class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "gata"

    def cldf_specs(self):  # A dataset must declare all CLDF sets it creates.
        return CLDFSpec(dir=self.cldf_dir, module='StructureDataset') 


    def cmd_makecldf(self, args):
        args.writer.add_sources()
        args.writer.cldf.add_component("ParameterTable")
        args.writer.cldf.add_component("LanguageTable")
        
        args.writer.cldf.add_table(
            "parameters.tsv",
            {
                "name": "ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#id",
            }, 
            "Category",
            {
                "name": "Name",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#name",
            },     
            "Shortname",
            "Variable_type",
            "Category_Esp",
            {
                "name": "Description",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#description",
            },    
            "Description_esp",
            {
                "name": "Comments",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#comment",
            },
        )
        args.writer.cldf.add_table(
            "languages.tsv",
            {
                "name": "ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#id",
            },
            {
                "name": "Name",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#name",
            },     
            "Family",
            {
                "name": "Macroarea",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#macroarea",
            },   
            {
                "name": "Latitude",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#latitude",
            },   
            {
                "name": "Longitude",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#longitude",
            },   
            {
                "name": "Glottocode",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#glottocode",
            },     
            "aes",
        )
        args.writer.cldf.add_table(
            "gata_raw.csv",
            {
                "name": "ID",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#id",
            },
            "Language",
            "Parameter",
            {
                "name": "Value",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#value",
            },
            "Certainty",
            "Reference",
            {
                "name": "Comments",
                "propertyUrl": "http://cldf.clld.org/v1.0/terms.rdf#comment",
            },
            "Source",
            "Year",
        )
        args.writer.cldf.add_foreign_key(
            "gata_raw.csv", "Value", "ValueTable", "ID"
        )
        args.writer.cldf.add_foreign_key(
            "gata_raw.csv", "Parameter", "parameters.tsv", "Shortname"
        )
        args.writer.cldf.add_foreign_key(
            "gata_raw.csv", "Language", "languages.tsv", "ID" 
        )


        for row in self.raw_dir.read_csv(
            'parameters.tsv',
            dicts=True,
            ):
            args.writer.objects['ParameterTable'].append(
                {
                    'ID': row['ID'],
                    'Category': row['Category'],
                    'Category Spanish': row['Category_esp'],
                    'Name': row['Name'],
                    'Shortname': row['Shortname'],
                    'Variable Type': row['Variable_type'],
                    'Description': row['Description'],
                    'Description Spanish': row['Description_esp'],
                    'Comments': row['Comments'],
                }
            )   
        
        for row in self.raw_dir.read_csv(
            'languages.tsv',
            dicts=True,
            ):
            args.writer.objects['LanguageTable'].append(
                {
                    'ID': row['ID'],
                    'Name': row['Name'],
                    'Family': row['Family'],
                    'Macro-Area': row['Macro-Area'],
                    'Latitude': row['Latitude'],
                    'Longitude': row['Longitude'],
                    'Glottocode': row['Glottocode'],
                    'AES': row['aes'],
                }
            )

        
        for row in self.raw_dir.read_csv(
            'gata_raw.csv',
            dicts=True,
            ):
                args.writer.objects['ValueTable'].append(
                    {
                        'ID': row['ID'],
                        'Language': row['Language'],
                        'Parameter': row['Parameter'],
                        'Value': row['Value'],
                        'Certainty': row['Certainty'],
                        'Reference': row['Reference'],
                        'Comments': row['Comments'],
                        'Source': row['Source'],
                        'Year': row['Year',]
                    }
                )