import unittest
from bioblend.aimedorig import TransProtein
from bioblend.aimedorig.base import ToolNotAvailableError
import os

import importlib.resources as res  # Py3.9+

_DATA = res.files(__package__) / "transprotein_data"


class TestTransProtein(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        transprotein_url = os.environ["TRANSPROTEIN_URL"]
        transprotein_key = os.environ["TRANSPROTEIN_API_KEY"]

        self.trans_protein = TransProtein(transprotein_url, transprotein_key)

        cache_file = os.path.join(os.path.dirname(__file__), ".transprotein_history_id")
        create = os.environ.get("TRANSPROTEIN_CREATE_HISTORY", "false").lower() == "true"

        if create:
            self.trans_protein.history.create(name='Test')
            history_id = self.trans_protein.ctx.history_id
            self.trans_protein.ctx.gi.histories.update_history(history_id, name=f"test-{history_id}")
            self.trans_protein.dataset.upload(file_dir=_DATA)
            with open(cache_file, 'w') as f:
                f.write(history_id)
            print(f"\n[History] create {history_id}\n")
        elif os.path.exists(cache_file):
            history_id = open(cache_file).read().strip()
            self.trans_protein.history.select(history_id=history_id)
        else:
            print(f"\n[History] use current (no cache, no create)\n")

        self.data = self.trans_protein.dataset.get()
        self.tools = self.trans_protein.tool

    @classmethod
    def tearDownClass(self):
        self.tools.show_warnings()

    def _run_tool(self, tool, tool_input):
        try:
            return tool.run(tool_input)
        except ToolNotAvailableError as e:
            self.skipTest(str(e))

    # ============================================================
    # antibody_design
    # ============================================================

    def test_boltzgen(self):
        tool_id = 'boltzgen'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['antibody_protein']['id'] = self.data['8jjs.cif'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_igdesign(self):
        tool_id = 'igdesign'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['antibody_protein']['id'] = self.data['1n8z.pdb'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    # ============================================================
    # backbone_design
    # ============================================================

    def test_rf_diffusion(self):
        tool_id = 'rf_diffusion'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_rf_diffusion_binder(self):
        tool_id = 'rf_diffusion_binder'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb']['id'] = self.data['insulin_target.pdb'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_rf_diffusion_ms(self):
        tool_id = 'rf_diffusion_ms'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb']['id'] = self.data['5ius_ref.pdb'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_rfdiffusion3(self):
        tool_id = 'rfdiffusion3'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb']['id'] = self.data['rf3_input.pdb'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_gpdl(self):
        tool_id = 'gpdl'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['reference']['id'] = self.data['2FYD.pdb'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    # ============================================================
    # filtering
    # ============================================================

    def test_global_rmsd(self):
        tool_id = 'global_rmsd'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        data = [f'sample_{i}.pdb' for i in range(2, 9)]
        tool_input['input_files'] = [{'id': self.data[data_name][0]['id'], 'src': 'hda'} for data_name in data]
        tool_input['r']['id'] = self.data['sample_1.pdb'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_motif_rmsd(self):
        tool_id = 'motif_rmsd'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        data = [f'sample_{i}.pdb' for i in range(1, 9)]
        tool_input['input_files'] = [{'id': self.data[data_name][0]['id'], 'src': 'hda'} for data_name in data]
        tool_input['motif_rmsd_r']['id'] = self.data['5ius_ref.pdb'][0]['id']
        tool_input['motif_d']['id'] = self.data['motif.txt'][0]['id']
        tool_input['motif_r']['id'] = self.data['motif.txt'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_net_charge(self):
        tool_id = 'net_charge'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        data = [f'sample_{i}.pdb' for i in range(1, 9)]
        tool_input['input_files'] = [{'id': self.data[data_name][0]['id'], 'src': 'hda'} for data_name in data]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_polar_score(self):
        tool_id = 'polar_score'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        data = [f'sample_{i}.pdb' for i in range(1, 9)]
        tool_input['input_files'] = [{'id': self.data[data_name][0]['id'], 'src': 'hda'} for data_name in data]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_rg(self):
        tool_id = 'rg'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        data = [f'sample_{i}.pdb' for i in range(1, 9)]
        tool_input['input_files'] = [{'id': self.data[data_name][0]['id'], 'src': 'hda'} for data_name in data]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_sap(self):
        tool_id = 'sap'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        data = [f'sample_{i}.pdb' for i in range(1, 9)]
        tool_input['input_files'] = [{'id': self.data[data_name][0]['id'], 'src': 'hda'} for data_name in data]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_rosetta(self):
        tool_id = 'rosetta'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_files'] = [{'id': self.data['7zkr_GABARAP.pdb'][0]['id'], 'src': 'hda'}]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_rosetta_s(self):
        tool_id = 'rosetta_s'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_file']['id'] = self.data['rosetta_res.csv'][0]['id']
        tool_input['input_files_1'] = [{'id': self.data['7zkr_GABARAP.pdb'][0]['id'], 'src': 'hda'}]
        tool_input['input_files_2'] = [{'id': self.data['7zkr_GABARAP_relax.pdb'][0]['id'], 'src': 'hda'}]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    # ============================================================
    # filtering/desity (有测试数据: filter_density/)
    # ============================================================

    def test_global_rmsd_desity(self):
        tool_id = 'global_rmsd_desity'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        data = [f'sample_{i}.pdb' for i in range(2, 9)]
        tool_input['input_files'] = [{'id': self.data[data_name][0]['id'], 'src': 'hda'} for data_name in data]
        tool_input['r']['id'] = self.data['sample_1.pdb'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_motif_rmsd_desity(self):
        tool_id = 'motif_rmsd_desity'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        data = [f'sample_{i}.pdb' for i in range(1, 9)]
        tool_input['input_files'] = [{'id': self.data[data_name][0]['id'], 'src': 'hda'} for data_name in data]
        tool_input['motif_rmsd_r']['id'] = self.data['5ius_ref.pdb'][0]['id']
        tool_input['motif_d']['id'] = self.data['motif.txt'][0]['id']
        tool_input['motif_r']['id'] = self.data['motif.txt'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_net_charge_desity(self):
        tool_id = 'net_charge_desity'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        data = [f'sample_{i}.pdb' for i in range(1, 9)]
        tool_input['input_files'] = [{'id': self.data[data_name][0]['id'], 'src': 'hda'} for data_name in data]
        tool_input['reference_pdb']['id'] = self.data['5ius_ref.pdb'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_polar_score_desity(self):
        tool_id = 'polar_score_desity'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        data = [f'sample_{i}.pdb' for i in range(1, 9)]
        tool_input['input_files'] = [{'id': self.data[data_name][0]['id'], 'src': 'hda'} for data_name in data]
        tool_input['reference_pdb']['id'] = self.data['5ius_ref.pdb'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_rg_desity(self):
        tool_id = 'rg_desity'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        data = [f'sample_{i}.pdb' for i in range(1, 9)]
        tool_input['input_files'] = [{'id': self.data[data_name][0]['id'], 'src': 'hda'} for data_name in data]
        tool_input['reference_pdb']['id'] = self.data['5ius_ref.pdb'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_sap_desity(self):
        tool_id = 'sap_desity'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        data = [f'sample_{i}.pdb' for i in range(1, 9)]
        tool_input['input_files'] = [{'id': self.data[data_name][0]['id'], 'src': 'hda'} for data_name in data]
        tool_input['reference_pdb']['id'] = self.data['5ius_ref.pdb'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    # ============================================================
    # structure_prediction
    # ============================================================

    def test_af2(self):
        tool_id = 'af2'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input']['id'] = self.data['af2.fasta'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_af3(self):
        tool_id = 'af3'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_files'] = [{'id': self.data['2PV7.json'][0]['id'], 'src': 'hda'}]
        tool_input['input_bin']['id'] = self.data['af3.bin.zst'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_boltz(self):
        tool_id = 'boltz'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['antibody_protein']['id'] = self.data['7ZKR.pdb'][0]['id']
        tool_input['input_files'] = [{'id': self.data['7ZKR_lig_3.fasta'][0]['id'], 'src': 'hda'}]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_esmfold(self):
        tool_id = 'esmfold'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_fastas']['id'] = self.data['input.fasta'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_idpfold(self):
        tool_id = 'idpfold'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input']['id'] = self.data['input.fasta'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_omegafold(self):
        tool_id = 'omegafold'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input']['id'] = self.data['input.fasta'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    # ============================================================
    # molecular_dynamics_docking
    # ============================================================

    def test_amber_gpu(self):
        tool_id = 'amber_gpu'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb']['id'] = self.data['af2_sample_1993.pdb'][0]['id']
        tool_input['options|va'] = '120-344'

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    # ============================================================
    # sequence_design
    # ============================================================

    def test_abacus_r(self):
        tool_id = 'abacus_r'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb']['id'] = self.data['5ius_ref.pdb'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_gpd_multi(self):
        tool_id = 'gpd_multi'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        data = [f'sample_{i}.pdb' for i in range(1, 5)]
        tool_input['input_files'] = [{'id': self.data[dn][0]['id'], 'src': 'hda'} for dn in data]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_protein_mpnn(self):
        tool_id = 'protein_mpnn'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb'] = [{'id': self.data['rfdiffusion_2.pdb'][0]['id'], 'src': 'hda'}]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    # ============================================================
    # unit
    # ============================================================

    def test_gemmi_cif2pdb(self):
        tool_id = 'gemmi_cif2pdb'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_files'] = [{'id': self.data['7ZKR_lig_0_0.pdb'][0]['id'], 'src': 'hda'}]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_extract_protein_sequences(self):
        tool_id = 'extract_protein_sequences'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        data = [f'sample_{i}.pdb' for i in range(1, 9)]
        tool_input['input_files'] = [{'id': self.data[data_name][0]['id'], 'src': 'hda'} for data_name in data]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_extract_complex_protein(self):
        tool_id = 'extract_complex_protein'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        data1 = ['4zgm_complex.pdb', '4zgm_rfdiffusion_0.pdb', '4zgm_rfdiffusion_1.pdb']
        data2 = ['4zgm_rfdiffusion_0.pdb']
        tool_input['input_files'] = [{'id': self.data[dn][0]['id'], 'src': 'hda'} for dn in data1]
        tool_input['input_name_files'] = [{'id': self.data[dn][0]['id'], 'src': 'hda'} for dn in data2]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_extract_seq_from_proteinmpnn(self):
        tool_id = 'extract_seq_from_proteinmpnn'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_files'] = [{'id': self.data['rfdiffusion_0.fasta'][0]['id'], 'src': 'hda'}, {'id': self.data['rfdiffusion_1.fasta'][0]['id'], 'src': 'hda'}]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_fasta_deduplication(self):
        tool_id = 'fasta_deduplication'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_fasta']['id'] = self.data['fd.fasta'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_fasta_rename_new(self):
        tool_id = 'fasta_rename_new'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_fasta']['id'] = self.data['input.fasta'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_autoesm_seqgen(self):
        tool_id = 'autoesm_seqgen'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_fastas']['id'] = self.data['A.fasta'][0]['id']
        tool_input['multimers_0|input_fasta'] = {'id': self.data['B.fasta'][0]['id'], 'src': 'hda'}

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_gpdl_align_merge(self):
        tool_id = 'gpdl_align_merge'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        data = ['4zgm_rfdiffusion_0.pdb', '4zgm_rfdiffusion_1.pdb']
        tool_input['input_files'] = [{'id': self.data[dn][0]['id'], 'src': 'hda'} for dn in data]
        tool_input['rmsd_r']['id'] = self.data['4zgm_complex.pdb'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_protein_monomers(self):
        tool_id = 'protein_monomers'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        data = [f'sample_{i}.pdb' for i in range(1, 5)]
        tool_input['input_files'] = [{'id': self.data[dn][0]['id'], 'src': 'hda'} for dn in data]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_rf_align_merge(self):
        tool_id = 'rf_align_merge'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        data = ['4zgm_rfdiffusion_0.pdb', '4zgm_rfdiffusion_1.pdb']
        tool_input['input_files'] = [{'id': self.data[dn][0]['id'], 'src': 'hda'} for dn in data]
        tool_input['rmsd_r']['id'] = self.data['4zgm_complex.pdb'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')


if __name__ == '__main__':
    unittest.main()
