.. image:: https://img.shields.io/pypi/v/bioblend.svg
    :target: https://pypi.org/project/bioblend/
    :alt: latest version available on PyPI

.. image:: https://readthedocs.org/projects/bioblend/badge/
    :alt: Documentation Status
    :target: https://bioblend.readthedocs.io/

.. image:: https://badges.gitter.im/galaxyproject/bioblend.svg
   :alt: Join the chat at https://gitter.im/galaxyproject/bioblend
   :target: https://gitter.im/galaxyproject/bioblend?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge


BioBlend is a Python library for interacting with the `Galaxy`_ API.

BioBlend is supported and tested on:

- Python 3.10 - 3.14
- Galaxy release 19.05 and later.

Full docs are available at https://bioblend.readthedocs.io/ with a quick library
overview also available in `ABOUT.rst <./ABOUT.rst>`_.

.. References/hyperlinks used above
.. _Galaxy: https://galaxyproject.org/

---

# bioblend-transmolecule

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
