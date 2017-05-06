#! /usr/bin/env nix-shell
#! nix-shell -i python3 -p nox python3
import itertools
import os
from nox.search import NixEvalError #nix_packages_json
from operator import itemgetter
import argparse
import json
import subprocess

FILENAME = '../nix-python-requires/requirements.txt'

def nix_packages_json(src):
    try:
        output = subprocess.check_output(['nix-env', '-qa', '-f' '{}'.format(src), '--json', '--show-trace'],
                                         universal_newlines=True)

    except subprocess.CalledProcessError as e:
        raise NixEvalError from e
    return json.loads(output)

def yield_python_derivations(data):
    """Yield keys that are python derivations."""
    searchnames = ['pypy', 'python']
    for key, value in data.items():
        for searchname in searchnames:
            if value['name'].startswith(searchname):
                yield key

def separated(pythonpackages):
    """Takes an iterable of names of derivations and splits the strings up. Yield the attribute name, derivation name, and version."""
    for derivation in pythonpackages:
        splitted = derivation.split('-')
        yield derivation, "-".join(splitted[1:-1]), splitted[-1] # (derivation, name, version)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str)

    args = parser.parse_args()
    src = args.src

    if os.path.isdir(src):
        src = os.path.join(src, 'default.nix')


    data = nix_packages_json(src)
    derivations = {key: data[key] for key in yield_python_derivations(data)}

    sep = list( separated((derivation['name'] for derivation in derivations.values())) )

    name_and_version = sorted(list(set((name, version) for derivation, name, version in sep if name and version)), key=itemgetter(0,1))

    with open(FILENAME, 'w') as file:
        file.writelines(("{}=={}\n".format(name, version) for name, version in name_and_version))


if __name__ == '__main__':
    main()






    main()
