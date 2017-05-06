# nix-update-python-requires

Nixpkgs contains a large amount of Python packages. This script uses `nox` to
determine the names and versions of these Python packages and then writes it to
a `requirements.txt` file.

Just run 

    ./update.py
