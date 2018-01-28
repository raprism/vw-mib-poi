import os
import sys
import re
import argparse
import hashlib
from collections import OrderedDict
from pathlib import Path


def is_file(fn):
    p = Path(fn)
    if p.is_file():
        return p


def get_hashes(path, read_size=-1):
    with path.open('rb') as fh:
        hashes = []
        while True:
            buf = fh.read(read_size)
            if not len(buf): break
            h = hashlib.sha1()
            h.update(buf)
            hashes.append(h.hexdigest())
        return hashes


def get_options(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path',
        metavar='<hashes.txt path>',
        nargs=1,
        type=is_file,
        help="""Specify path of 'hashes.txt'.
        Typically: PersonalPOI/Package/0/default/hashes.txt
        """)
    options = parser.parse_args(args=args)
    options.path = options.path[0]
    return options


class HashFile:

    # first key per file
    key_file = 'FileName'
    # defined with same order as in hashes.txt
    keys_other = ['FileSize', 'CheckSumSize', 'CheckSum']

    def __init__(self, path, load=True):

        self.path = path
        self.txt = None
        self.files = []
        self.values = OrderedDict()
        self.hashes = OrderedDict()
        if load:
            self.read()
            self.parse()

    def read(self):
        with self.path.open('r') as fh:
            self.txt = fh.read()

    def _parse(self, key):
        return re.findall(r'{} = "(.*)"'.format(key), self.txt)

    def parse(self):
        # put everything in OrderedDict of OrderedDict's
        self.files = self._parse(self.key_file)
        file_values = {k: self._parse(k) for k in self.keys_other}
        self.values = OrderedDict()
        for i, f in enumerate(self.files):
            self.values[f] = OrderedDict(
                [(k, file_values[k][i]) for k in self.keys_other])

    def get_file_sizes(self):
        if self.values:
            return sum(int(self.values[f]['FileSize']) for f in self.values)

    @staticmethod
    def _report(fn, key, value, status=''):
        fn = '{:28}'.format(fn)
        kv = '{} = "{}"'.format(key, value)
        if status:
            print(fn, status + '\t', kv)
        else:
            print(fn, kv)

    def eval(self):
        rootdir = self.path.parent
        s__OK = 'passed'
        s_NOK = 'FAILED'
        print()
        for fn in self.files:
            fn_parts = fn.split('/')
            path = rootdir.joinpath(*fn_parts)
            ##
            key = 'CheckSum'  ##
            hashes = get_hashes(path, int(self.values[fn]['CheckSumSize']))
            ## TODO: check also CheckSum[N] for poidata.db
            self.hashes[fn] = hashes[0]
            if hashes[0] == self.values[fn][key]:
                status = s__OK
            else:
                status = s_NOK
            self._report(fn, key, hashes[0], status)
            ##
            key = 'FileSize'  ##
            fsize = os.stat(str(path)).st_size  # str for Py2.7 comp.
            if fsize == int(self.values[fn][key]):
                status = s__OK
            else:
                status = s_NOK
            self._report(fn, key, fsize, status)
        # own hash sum
        hashes = get_hashes(self.path)
        self.hashes[self.path.name] = hashes[0]
        print()
        self._report(self.path.name, 'CheckSum', hashes[0])
        self._report(self.path.name, 'FileSize',
                     os.stat(str(self.path)).st_size)  # str for Py2.7 comp.


if __name__ == '__main__':

    checks = HashFile(get_options(sys.argv[1:]).path)
    checks.eval()
