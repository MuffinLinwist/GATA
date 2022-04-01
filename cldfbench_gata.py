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

    def cmd_download(self, args):
        pass


    def read(self, core, extended=False, pkmap=None, key=None):
        if not key:
            key = lambda d: int(d['pk'])
        res = collections.OrderedDict()
        for row in sorted(self.read_csv('{0}.csv'.format(core), dicts=True), key=key):
            res[row['pk']] = row
            if pkmap is not None:
                pkmap[core][row['pk']] = row['id']
        if extended:
            for row in self.read_csv('{0}.csv'.format(extended), dicts=True):
                res[row['pk']].update(row)
        return res    


    def cmd_makecldf(self, args):
        self.create_schema(args.writer.cldf)
        pk2id = collections.defaultdict(dict)

        sources = parse_string(
            self.raw.joinpath('sources.bib').read_text(encoding='utf8'), 'bibtext')
        gbs_lg_refs = collections.defaultdict(set)
        src_names = {}
        

        for row in self.read(
            'parameters',
            extended= 'feature',
            pkmap=pk2id,
            key=lambda d: d['id']).values():
            args.writer.objects['ParameterTable'].append({
                'ID': row['ID'],
                'Category': row['Category'],
                'Name': row['Name'],
                'Shortname': row['Shortname'],
                'Variable type': row['Variable_type'],
                'Description': row['Description'],
                'Comments': row['Comments']
                })

        families = self.read('lang_with_aes')
        glang = {l.hid: (l.id, l.iso) for l in args.glottolog.api.languoids() if l.hid}
        for row in self.read(
                'lang_with_aes', pkmap=pk2id, key=lambda d: d['id']).values():
            args.writer.objects['LanguageTable'].append({
                'ID': row['ID'],
                'Name': row['Name'],
                'Glottocode': glang[row['id']][0],
                'Family': families[row['family_pk']]['name'],
                'Latitude': row['Latitude'],
                'Longitude': row['Longitude'],
                'AES': row['aes'],
            })
        args.writer.objects['LanguageTable'].sort(key=lambda d: d['ID']) 



        refs = {
            vspk: sorted(pk2id['source'][r['source_pk']] for r in rows)
            for vspk, rows in itertools.groupby(
                self.read('valuesetreference', key=lambda d: d['valueset_pk']).values(),
                lambda d: d['valueset_pk'],
            )
        }
        vsdict = self.read('valueset', pkmap=pk2id)
        for row in self.read('gata_raw').values():
            vs = vsdict[row['valueset_pk']]
            args.writer.objects['ValueTable'].append({
                'ID': vs['ID'],
                'Language_ID': pk2id['lang_with_aes'][vs['language_pk']],
                'Parameter_ID': pk2id['parameters'][vs['parameter_pk']],
                'State_1': pk2id['domainelement'][row['domainelement_pk']].split('-')[1],
                'Certainty_1': row['Certainty_1'],
                'Reference_1': vs['source'],
                'Comments_1': row['Comments_1'],
                'Source': refs.get(row['Reference_1'], []),
            })

        args.writer.objects['ValueTable'].sort(
            key=lambda d: (d['Language_ID'], d['Parameter_ID']))

    def create_schema(self, cldf):
        cldf.add_component(
            'ParameterTable',
        )
        cldf.add_component('LanguageTable')
        cldf.add_table(
            'CONTRIBUTORS.md',
            'Name',
            {
                'name': 'Contributor',
                'propertyUrl': 'http://purl.org/dc/terms/creator',
            },
            'GitHub user',
            'Description',
            'Role'
        )
        cldf.add_columns('ValueTable', 'Contributor', 'Reference')
        cldf.add_foreign_key('ParameterTable', 'CONTRIBUTORS.md', 'ID')    
