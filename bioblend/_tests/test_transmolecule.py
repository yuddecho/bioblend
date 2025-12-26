import unittest
from bioblend.transmolecule import TransMolecule
import os

import importlib.resources as res  # Py3.9+

_DATA = res.files(__package__) / "transm_data"

class TestTransMolecule(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        transmolecule_url = os.environ["TRANSMOLECULE_URL"]
        transmolecule_key = os.environ["TRANSMOLECULE_API_KEY"]
        
        self.trans_molecule = TransMolecule(transmolecule_url, transmolecule_key)

        is_new_history = True

        if is_new_history:
            self.trans_molecule.history.create(name='Test')

            self.trans_molecule.dataset.upload(file_dir=_DATA)

        else:
            history_id = "e14715ce11d8be59"
            self.trans_molecule.history.select(history_id=history_id) 

        self.data = self.trans_molecule.dataset.get()
        # print(self.data)        

        self.tools = self.trans_molecule.tool

    def test_admet_ai(self):
        tool_id = 'admet_ai'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels['No']

        data = ['reinvent4_813_docked_0_docked_0.sdf', 'reinvent4_813_docked_0_docked_1.sdf', 'reinvent4_813_docked_0_docked_2.sdf']
        tool_input['sdf_files'] = [{'id': self.data[data_name][0]['id'], 'src': 'hda'} for data_name in data]

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

    def test_admetica(self):
        tool_id = 'admetica'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels['No']

        data = ['reinvent4_813_docked_0_docked_0.sdf', 'reinvent4_813_docked_0_docked_1.sdf', 'reinvent4_813_docked_0_docked_2.sdf']
        tool_input['sdf_files'] = [{'id': self.data[data_name][0]['id'], 'src': 'hda'} for data_name in data]

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

    def test_amber(self):
        tool_id = 'amber'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels

        tool_input['receptor'] = {'id': self.data['3u2z_protein.pdb'][0]['id'], 'src': 'hda'}
        tool_input['ligand'] = {'id': self.data['130.pdb'][0]['id'], 'src': 'hda'}

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

    def test_build_db(self):
        tool_id = 'build_db'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels

        tool_input['ligand_zip_file']['id'] = self.data['matched_files.zip'][0]['id']

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

    def test_dbsearch(self):
        tool_id = 'dbsearch'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels

        tool_input['json_file']['id'] = self.data['test.json'][0]['id']

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

    def test_extract(self):
        tool_id = 'extract'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels

        tool_input['mol_file']['id'] = self.data['ph_6.txt'][0]['id']

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

    def test_gnina(self):
        tool_id = 'gnina'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels

        tool_input['receptor']['id'] = self.data['receptor.pdb'][0]['id']
        tool_input['reference_ligand']['id'] = self.data['ligand.sdf'][0]['id']

        data = ['RAIEQIIQPDI.sdf', 'ZXWUGWV.sdf', 'T608.sdf']
        tool_input['options|sdf'] = [{'id': self.data[data_name][0]['id'], 'src': 'hda'} for data_name in data]

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

    def test_gnina_scoreonly(self):
        tool_id = 'gnina_scoreonly'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels

        tool_input['receptor']['id'] = self.data['receptor.pdb'][0]['id']

        data = ['RAIEQIIQPDI.sdf', 'ZXWUGWV.sdf', 'T608.sdf']
        tool_input['options|sdf'] = [{'id': self.data[data_name][0]['id'], 'src': 'hda'} for data_name in data]

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

    def test_gnina_search_ligand(self):
        tool_id = 'gnina_search_ligand'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels

        tool_input['receptor']['id'] = self.data['receptor.pdb'][0]['id']

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

    def test_lipinsk(self):
        tool_id = 'lipinsk'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels['No']

        data = ['reinvent4_813_docked_0_docked_0.sdf', 'reinvent4_813_docked_0_docked_1.sdf', 'reinvent4_813_docked_0_docked_2.sdf']
        tool_input['sdf_files'] = [{'id': self.data[data_name][0]['id'], 'src': 'hda'} for data_name in data]

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

    def test_obabel(self):
        tool_id = 'obabel'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels

        tool_input['input_file']['id'] = self.data['T608.sdf'][0]['id']

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

    def test_pdb2sdf(self):
        tool_id = 'pdb2sdf'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels

        tool_input['pdb_files'] = [{'id': self.data['1ITI_214.pdb'][0]['id'], 'src': 'hda'}]

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

    def test_pharma(self):
        tool_id = 'pharma'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels

        tool_input['pdb_file']['id'] = self.data['receptor.pdb'][0]['id']
        tool_input['sdf_file']['id'] = self.data['ligand.sdf'][0]['id']

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

    def test_pharma_pep_gen(self):
        tool_id = 'pharma_pep_gen'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels

        tool_input['input_files'] = [{'id': self.data['test.json'][0]['id'], 'src': 'hda'}]

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

    def test_rascore(self):
        tool_id = 'rascore'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels['smiles']

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

    def test_reinvent4_de_novo(self):
        tool_id = 'reinvent4_de_novo'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

    def test_reinvent4_linker(self):
        tool_id = 'reinvent4_linker'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

    def test_reinvent4_mol2mol(self):
        tool_id = 'reinvent4_mol2mol'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

    def test_reinvent4_r(self):
        tool_id = 'reinvent4_r'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

    def test_sdf2smi(self):
        tool_id = 'sdf2smi'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels

        data = ['RAIEQIIQPDI.sdf', 'ZXWUGWV.sdf', 'T608.sdf']
        tool_input['sdf_files'] = [{'id': self.data[data_name][0]['id'], 'src': 'hda'} for data_name in data]

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

    def test_smi2pdb(self):
        tool_id = 'smi2pdb'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels

        tool_input['smiles_file']['id'] = self.data['Reinvent4_Res.csv'][0]['id']

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

    def test_table_sort(self):
        tool_id = 'table_sort'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels

        tool_input['table_file']['id'] = self.data['Reinvent4_Res.csv'][0]['id']
        tool_input['sort_column'] = 'NLL'

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

    def test_transpharmer(self):
        tool_id = 'transpharmer'
        print(f"\n----------------------------------------------------------------------")
        print(f"Testing {tool_id}")

        # 获取工具，传入id或者name
        tool = self.tools.get_tool(tool_id=tool_id)

        # 获取工具输入示例
        input_exampels = tool.inputs()
        print(f'input_exampels: {input_exampels}')

        # 构建输入，将上传的文件数据的id放到对应value
        tool_input = input_exampels

        print(f'tool_input: {tool_input}')

        # 运行工具，提取药效团
        tool_output = tool.run(tool_input)
        print(f'tool_output: {tool_output}')

if __name__ == '__main__':
    unittest.main()

    # # 只测试 test_admet_ai
    # suite = unittest.TestSuite()
    # suite.addTest(TestTransMolecule('test_table_sort'))
    # runner = unittest.TextTestRunner()
    # runner.run(suite)