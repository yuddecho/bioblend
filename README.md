# bioblend-transmolecule

BioBlend is a Python library for interacting with the `Galaxy`_ API.

BioBlend is supported and tested on:

- Python 3.10 - 3.14
- Galaxy release 19.05 and later.

## installation

```
pip install git+https://github.com/yuddecho/bioblend.git

# or
git clone https://github.com/yuddecho/bioblend.git
cd bioblend && pip install .
```

## usage

```python
from bioblend.transmolecule import TransMolecule

# connect to transmolecule instance
client = TransMolecule(url='http://localhost:8080', key='your_api_key')
```

## test
```bash
# win
# set TRANSMOLECULE_URL=http://localhost:8080
# set TRANSMOLECULE_API_KEY=your_api_key

export TRANSMOLECULE_URL=http://localhost:8080
export TRANSMOLECULE_API_KEY=your_api_key

python -m bioblend._tests.test_transmolecule
```
