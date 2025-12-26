# bioblend-transmolecule

BioBlend is a Python library for interacting with the `Galaxy-TransMolecule` API.

BioBlend is supported and tested on:

- Python 3.10 - 3.14

## installation

```
pip install git+https://github.com/yuddecho/bioblend.git

# or
git clone https://github.com/yuddecho/bioblend.git
cd bioblend && pip install .
```

## usage

1. Log in to the web site.
2. Go to **User → Settings → Manage API key**.
3. Generate and copy the API key.

```python
from bioblend.transmolecule import TransMolecule

# connect to transmolecule instance
client = TransMolecule(url='http://localhost:8080', key='your_api_key')
```
- For basic usage, please refer to file [transmolecule_usage.ipynb]().
- For tool parameter descriptions, please refer to file [README.md](https://github.com/yuddecho/bioblend/blob/main/bioblend/transmolecule/tools/README.md).
- For a workflow usage tutorial, please refer to file [transmolecule_workflow.ipynb]().

## test

- For test code, please refer to file [test_transmolecule.py](https://github.com/yuddecho/bioblend/blob/main/bioblend/_tests/test_transmolecule.py).

```bash
# win
# set TRANSMOLECULE_URL=http://localhost:8080
# set TRANSMOLECULE_API_KEY=your_api_key

export TRANSMOLECULE_URL=http://localhost:8080
export TRANSMOLECULE_API_KEY=your_api_key

python -m bioblend._tests.test_transmolecule
```
