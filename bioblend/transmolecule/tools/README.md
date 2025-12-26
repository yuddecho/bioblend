
## 数值
```yaml
  - id: heat1_tempi
    name: Heat1 Temperature Initial
    type: text
    help: null
    optional: true
    value: 0
```
- text：`{'heat1_tempi': '0'}`

## 单个文件
```yaml
inputs:
  - id: pdb_file
    type: data
    name: PDB file
    multiple: false
    optional: false
    extensions:
      - pdb
    help: null
```
- file：`{'pdb_file': {'id': 'file_id', 'src': 'hda'}}`
- dataset：`{'pdb_file': {'id': 'dataset_id', 'src': 'hdca'}}` 会将dataset内容依次作为输入运行工具

## 输入多个文件
```yaml
inputs:
  - id: pdb_files
    type: data
    name: PDB files
    multiple: true
    optional: false
    extensions:
      - pdb
    help: null
```
- multiple file：`{'pdb_files': [{'id': 'file_id', 'src': 'hda'}, ...]}`
- dataset：`{'pdb_files': [{'id': 'dataset_id','src': 'hdca'}, ...]}`
- mix: `{'pdb_files': [{'id': 'file_id', 'src': 'hda'}, {'id': 'dataset_id','src': 'hdca'}, ...]}`

## 条件选择
```yaml
inputs:
  - id: local_db_name
    type: select
    name: Select local small molecules database
    optional: false
    value: TopScience_Zinc_ChemDiv
    options:
      - [TopScience_Zinc_ChemDiv, TopScience_Zinc_ChemDiv, false]
      - [TopScienceDB, TopScienceDB, false]
      - [Zinc, Zinc, false]
      - [ChemDiv, ChemDiv, false]
```
- `{'local_db_name': 'TopScience_Zinc_ChemDiv'}`

## 条件嵌套
```yaml
inputs:
  - id: cond
    name: Input SMILES
    type: conditional
    case_id: sele
    cases:
      - value: cond_1
        inputs:
          - id: smiles_content
            type: text
            name: SMILES
            help: null
            optional: false
            value: "O=C(N(C)C)Nc1cc(ccc1F)SC1=C(N(c2ccncc2)C2CCN(CC2)C(=O)C)C(=O)N(C1=O)C(=O)N(C)C"
      - value: cond_2
        inputs:
          - id: smiles_file
            type: data
            name: SMILES file
            help: One SMILES per line
            extensions:
              - txt
            multiple: false
            options: false
```
- `{'cond|sele': 'cond_1', 'cond|smiles_content': 'O=C(N(C)C)Nc1cc(ccc1F)SC1=C(N(c2ccncc2)C2CCN(CC2)C(=O)C)C(=O)N(C1=O)C(=O)N(C)C'}`

