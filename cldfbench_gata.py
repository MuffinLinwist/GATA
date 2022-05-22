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
        return CLDFSpec(
                dir=self.cldf_dir, 
                module='StructureDataset',
                data_fnames={"ParameterTable": "features.csv"}
                ) 


    def cmd_makecldf(self, args):
        sources = parse_string(
            self.raw_dir.joinpath('sources.bib').read_text(encoding='utf8'), 'bibtex')
        args.log.info("added sources")
        args.writer.cldf.add_columns(
                "ParameterTable",
                "Category",
                "Shortname",
                "Variable_type",
                "Category_Esp",  
                "Description_esp",
                "Comments")
        args.writer.cldf.add_component(
                "LanguageTable",
                "AES")
        args.writer.cldf.add_columns(
            "ValueTable",
            "Certainty",
            "Reference",
            "Comments",
            "Year")


        for row in self.etc_dir.read_csv(
            'parameters.csv',
            dicts=True,
            ):
            args.writer.objects['ParameterTable'].append(row)
        args.log.info("added parameters")
        
        for row in self.etc_dir.read_csv(
            'languages.csv',
            dicts=True,
            ):
            args.writer.objects['LanguageTable'].append(row)
        args.log.info("added languages")
        
        for row in self.raw_dir.read_csv(
            'gata_raw.csv',
            dicts=True,
            ):
                args.writer.objects['ValueTable'].append(row)
        args.log.info("added values")
