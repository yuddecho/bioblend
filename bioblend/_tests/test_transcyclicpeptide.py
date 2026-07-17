import unittest
from bioblend.aimedorig import TransCyclicPeptide
from bioblend.aimedorig.base import ToolNotAvailableError
import os

import importlib.resources as res

_DATA = res.files(__package__) / "transcyclicpeptide_data"


class TestTransCyclicPeptide(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        transcyclicpeptide_url = os.environ["TRANSCYCLICPEPTIDE_URL"]
        transcyclicpeptide_key = os.environ["TRANSCYCLICPEPTIDE_API_KEY"]

        self.tcp = TransCyclicPeptide(transcyclicpeptide_url, transcyclicpeptide_key)

        cache_file = os.path.join(os.path.dirname(__file__), ".transcyclicpeptide_history_id")
        create = os.environ.get("TRANSCYCLICPEPTIDE_CREATE_HISTORY", "false").lower() == "true"

        if create:
            self.tcp.history.create(name='Test')
            history_id = self.tcp.ctx.history_id
            self.tcp.ctx.gi.histories.update_history(history_id, name=f"test-{history_id}")
            self.tcp.dataset.upload(file_dir=_DATA)
            with open(cache_file, 'w') as f:
                f.write(history_id)
            print(f"\n[History] create {history_id}\n")
        elif os.path.exists(cache_file):
            history_id = open(cache_file).read().strip()
            self.tcp.history.select(history_id=history_id)
        else:
            print(f"\n[History] use current (no cache, no create)\n")

        self.data = self.tcp.dataset.get()
        self.tools = self.tcp.tool

    @classmethod
    def tearDownClass(self):
        self.tools.show_warnings()

    def _run_tool(self, tool, tool_input):
        try:
            return tool.run(tool_input)
        except ToolNotAvailableError as e:
            self.skipTest(str(e))

    # ============================================================
    # 环肽设计 (Cyclic Peptide Design)
    # ============================================================

    def test_cphallu(self):
        tool_id = 'cphallu'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_file']['id'] = self.data['PDL1.pdb'][0]['id']
        tool_input['binder_name'] = 'PDL1'
        tool_input['chains'] = 'A'
        tool_input['hotspot'] = 'A'
        tool_input['min_length'] = 55
        tool_input['max_length'] = 65
        tool_input['num_designs'] = 2
        tool_input['max_traj'] = 'false'

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_cpflow(self):
        tool_id = 'cpflow'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_file']['id'] = self.data['7zkr_GABARAP.pdb'][0]['id']
        tool_input['specified_hotspots'] = 'A51,A52,A50,A48,A62,A65'

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    # ============================================================
    # 开源算法 (Open Source Algorithms)
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

    def test_odesign(self):
        tool_id = 'odesign'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_file']['id'] = self.data['PDL1_truncated.pdb'][0]['id']
        tool_input['specified_hotspots'] = 'B/20-133'
        tool_input['chains_0|if_cyc'] = 'false'

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_repeptide_binder(self):
        tool_id = 'repeptide_binder'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb']['id'] = self.data['7zkr_GABARAP.pdb'][0]['id']
        tool_input['hotspot'] = 'A51,A52,A50,A48,A62,A65'

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_repeptide_monomer(self):
        tool_id = 'repeptide_monomer'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb']['id'] = self.data['7zkr_GABARAP.pdb'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    # ============================================================
    # 序列评估 (Sequence Evaluation)
    # ============================================================

    def test_linear_eval(self):
        tool_id = 'linear_eval'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_fasta']['id'] = self.data['peptides_chainB.fasta'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_h2t_eval(self):
        tool_id = 'h2t_eval'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_fasta']['id'] = self.data['peptides_chainB.fasta'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_disulfide_eval(self):
        tool_id = 'disulfide_eval'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_fasta']['id'] = self.data['peptides_chainB.fasta'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_master_eval(self):
        tool_id = 'master_eval'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_fasta']['id'] = self.data['peptides_chainB.fasta'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    # ============================================================
    # 结构预处理 (Structure Preparation)
    # ============================================================

    def test_rename_chains(self):
        tool_id = 'rename_chains'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdbs'] = [{'id': self.data['7zkr_GABARAP.pdb'][0]['id'], 'src': 'hda'}]
        tool_input['chain_map'] = 'A:B,B:A'

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_clean_pdbs(self):
        tool_id = 'clean_pdbs'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdbs'] = [{'id': self.data['7zkr_GABARAP.pdb'][0]['id'], 'src': 'hda'}]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_split_chain(self):
        tool_id = 'split_chain'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdbs'] = [{'id': self.data['7zkr_GABARAP.pdb'][0]['id'], 'src': 'hda'}]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_fastrelax(self):
        tool_id = 'fastrelax'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdbs'] = [{'id': self.data['7zkr_GABARAP.pdb'][0]['id'], 'src': 'hda'}]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_relax_only(self):
        tool_id = 'relax_only'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdbs'] = [{'id': self.data['7zkr_GABARAP.pdb'][0]['id'], 'src': 'hda'}]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    # ============================================================
    # 结构评估 (Structure Evaluation)
    # ============================================================

    def test_clash_score(self):
        tool_id = 'clash_score'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb'] = [
            {'id': self.data['rank0003_klk2_cycpep_disulfide_0259_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0004_klk2_cycpep_disulfide_0265_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0006_klk2_cycpep_disulfide_1281_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0007_klk2_cycpep_disulfide_0056_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0008_klk2_cycpep_disulfide_1149_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0009_klk2_cycpep_disulfide_1696_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0011_klk2_cycpep_disulfide_1146_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0014_klk2_cycpep_disulfide_1882_processed.pdb'][0]['id'], 'src': 'hda'}
        ]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_clash_detail(self):
        tool_id = 'clash_detail'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb'] = [
            {'id': self.data['rank0003_klk2_cycpep_disulfide_0259_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0004_klk2_cycpep_disulfide_0265_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0006_klk2_cycpep_disulfide_1281_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0007_klk2_cycpep_disulfide_0056_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0008_klk2_cycpep_disulfide_1149_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0009_klk2_cycpep_disulfide_1696_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0011_klk2_cycpep_disulfide_1146_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0014_klk2_cycpep_disulfide_1882_processed.pdb'][0]['id'], 'src': 'hda'}
        ]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_buried_sasa(self):
        tool_id = 'buried_sasa'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb'] = [
            {'id': self.data['rank0003_klk2_cycpep_disulfide_0259_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0004_klk2_cycpep_disulfide_0265_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0006_klk2_cycpep_disulfide_1281_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0007_klk2_cycpep_disulfide_0056_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0008_klk2_cycpep_disulfide_1149_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0009_klk2_cycpep_disulfide_1696_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0011_klk2_cycpep_disulfide_1146_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0014_klk2_cycpep_disulfide_1882_processed.pdb'][0]['id'], 'src': 'hda'}
        ]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_directed_clash(self):
        tool_id = 'directed_clash'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb'] = [
            {'id': self.data['rank0003_klk2_cycpep_disulfide_0259_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0004_klk2_cycpep_disulfide_0265_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0006_klk2_cycpep_disulfide_1281_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0007_klk2_cycpep_disulfide_0056_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0008_klk2_cycpep_disulfide_1149_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0009_klk2_cycpep_disulfide_1696_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0011_klk2_cycpep_disulfide_1146_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0014_klk2_cycpep_disulfide_1882_processed.pdb'][0]['id'], 'src': 'hda'}
        ]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_interface_ca_count(self):
        tool_id = 'interface_ca_count'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb'] = [
            {'id': self.data['rank0003_klk2_cycpep_disulfide_0259_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0004_klk2_cycpep_disulfide_0265_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0006_klk2_cycpep_disulfide_1281_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0007_klk2_cycpep_disulfide_0056_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0008_klk2_cycpep_disulfide_1149_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0009_klk2_cycpep_disulfide_1696_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0011_klk2_cycpep_disulfide_1146_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0014_klk2_cycpep_disulfide_1882_processed.pdb'][0]['id'], 'src': 'hda'}
        ]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_interface_composition(self):
        tool_id = 'interface_composition'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb'] = [
            {'id': self.data['rank0003_klk2_cycpep_disulfide_0259_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0004_klk2_cycpep_disulfide_0265_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0006_klk2_cycpep_disulfide_1281_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0007_klk2_cycpep_disulfide_0056_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0008_klk2_cycpep_disulfide_1149_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0009_klk2_cycpep_disulfide_1696_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0011_klk2_cycpep_disulfide_1146_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0014_klk2_cycpep_disulfide_1882_processed.pdb'][0]['id'], 'src': 'hda'}
        ]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_hotspot(self):
        tool_id = 'hotspot'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb'] = [
            {'id': self.data['rank0003_klk2_cycpep_disulfide_0259_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0004_klk2_cycpep_disulfide_0265_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0006_klk2_cycpep_disulfide_1281_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0007_klk2_cycpep_disulfide_0056_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0008_klk2_cycpep_disulfide_1149_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0009_klk2_cycpep_disulfide_1696_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0011_klk2_cycpep_disulfide_1146_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0014_klk2_cycpep_disulfide_1882_processed.pdb'][0]['id'], 'src': 'hda'}
        ]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_non_interacting(self):
        tool_id = 'non_interacting'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb'] = [
            {'id': self.data['rank0003_klk2_cycpep_disulfide_0259_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0004_klk2_cycpep_disulfide_0265_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0006_klk2_cycpep_disulfide_1281_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0007_klk2_cycpep_disulfide_0056_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0008_klk2_cycpep_disulfide_1149_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0009_klk2_cycpep_disulfide_1696_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0011_klk2_cycpep_disulfide_1146_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0014_klk2_cycpep_disulfide_1882_processed.pdb'][0]['id'], 'src': 'hda'}
        ]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_motif_centroid(self):
        tool_id = 'motif_centroid'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb'] = [
            {'id': self.data['rank0003_klk2_cycpep_disulfide_0259_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0004_klk2_cycpep_disulfide_0265_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0006_klk2_cycpep_disulfide_1281_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0007_klk2_cycpep_disulfide_0056_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0008_klk2_cycpep_disulfide_1149_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0009_klk2_cycpep_disulfide_1696_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0011_klk2_cycpep_disulfide_1146_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0014_klk2_cycpep_disulfide_1882_processed.pdb'][0]['id'], 'src': 'hda'}
        ]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_chain_rmsd(self):
        tool_id = 'chain_rmsd'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_dir1'] = [
            {'id': self.data['rank0003_klk2_cycpep_disulfide_0259_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0004_klk2_cycpep_disulfide_0265_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0006_klk2_cycpep_disulfide_1281_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0007_klk2_cycpep_disulfide_0056_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0008_klk2_cycpep_disulfide_1149_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0009_klk2_cycpep_disulfide_1696_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0011_klk2_cycpep_disulfide_1146_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0014_klk2_cycpep_disulfide_1882_processed.pdb'][0]['id'], 'src': 'hda'}
        ]
        tool_input['input_dir2'] = [
            {'id': self.data['rank0003_klk2_cycpep_disulfide_0259_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0004_klk2_cycpep_disulfide_0265_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0006_klk2_cycpep_disulfide_1281_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0007_klk2_cycpep_disulfide_0056_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0008_klk2_cycpep_disulfide_1149_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0009_klk2_cycpep_disulfide_1696_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0011_klk2_cycpep_disulfide_1146_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0014_klk2_cycpep_disulfide_1882_processed.pdb'][0]['id'], 'src': 'hda'}
        ]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_physics_metrics(self):
        tool_id = 'physics_metrics'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb'] = [
            {'id': self.data['rank0003_klk2_cycpep_disulfide_0259_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0004_klk2_cycpep_disulfide_0265_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0006_klk2_cycpep_disulfide_1281_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0007_klk2_cycpep_disulfide_0056_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0008_klk2_cycpep_disulfide_1149_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0009_klk2_cycpep_disulfide_1696_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0011_klk2_cycpep_disulfide_1146_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0014_klk2_cycpep_disulfide_1882_processed.pdb'][0]['id'], 'src': 'hda'}
        ]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_fnc_score(self):
        tool_id = 'fnc_score'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb'] = [
            {'id': self.data['rank0003_klk2_cycpep_disulfide_0259_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0004_klk2_cycpep_disulfide_0265_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0006_klk2_cycpep_disulfide_1281_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0007_klk2_cycpep_disulfide_0056_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0008_klk2_cycpep_disulfide_1149_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0009_klk2_cycpep_disulfide_1696_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0011_klk2_cycpep_disulfide_1146_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0014_klk2_cycpep_disulfide_1882_processed.pdb'][0]['id'], 'src': 'hda'}
        ]
        tool_input['native_pdb']['id'] = self.data['native.pdb'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_grid_score(self):
        tool_id = 'grid_score'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb'] = [
            {'id': self.data['rank0003_klk2_cycpep_disulfide_0259_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0004_klk2_cycpep_disulfide_0265_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0006_klk2_cycpep_disulfide_1281_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0007_klk2_cycpep_disulfide_0056_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0008_klk2_cycpep_disulfide_1149_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0009_klk2_cycpep_disulfide_1696_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0011_klk2_cycpep_disulfide_1146_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0014_klk2_cycpep_disulfide_1882_processed.pdb'][0]['id'], 'src': 'hda'}
        ]
        tool_input['native_pdb']['id'] = self.data['native.pdb'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_score_minimal(self):
        tool_id = 'score_minimal'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb'] = [
            {'id': self.data['rank0003_klk2_cycpep_disulfide_0259_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0004_klk2_cycpep_disulfide_0265_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0006_klk2_cycpep_disulfide_1281_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0007_klk2_cycpep_disulfide_0056_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0008_klk2_cycpep_disulfide_1149_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0009_klk2_cycpep_disulfide_1696_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0011_klk2_cycpep_disulfide_1146_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0014_klk2_cycpep_disulfide_1882_processed.pdb'][0]['id'], 'src': 'hda'}
        ]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_dg_cross_separated(self):
        tool_id = 'dg_cross_separated'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb'] = [
            {'id': self.data['rank0003_klk2_cycpep_disulfide_0259_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0004_klk2_cycpep_disulfide_0265_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0006_klk2_cycpep_disulfide_1281_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0007_klk2_cycpep_disulfide_0056_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0008_klk2_cycpep_disulfide_1149_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0009_klk2_cycpep_disulfide_1696_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0011_klk2_cycpep_disulfide_1146_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0014_klk2_cycpep_disulfide_1882_processed.pdb'][0]['id'], 'src': 'hda'}
        ]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    # ============================================================
    # 稳定性评估 (Stability Evaluation)
    # ============================================================

    def test_stab_cycpep(self):
        tool_id = 'stab_cycpep'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb'] = [
            {'id': self.data['rank0003_klk2_cycpep_disulfide_0259_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0004_klk2_cycpep_disulfide_0265_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0006_klk2_cycpep_disulfide_1281_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0007_klk2_cycpep_disulfide_0056_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0008_klk2_cycpep_disulfide_1149_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0009_klk2_cycpep_disulfide_1696_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0011_klk2_cycpep_disulfide_1146_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0014_klk2_cycpep_disulfide_1882_processed.pdb'][0]['id'], 'src': 'hda'}
        ]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_stab_linearpep(self):
        tool_id = 'stab_linearpep'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb'] = [
            {'id': self.data['rank0003_klk2_cycpep_disulfide_0259_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0004_klk2_cycpep_disulfide_0265_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0006_klk2_cycpep_disulfide_1281_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0007_klk2_cycpep_disulfide_0056_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0008_klk2_cycpep_disulfide_1149_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0009_klk2_cycpep_disulfide_1696_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0011_klk2_cycpep_disulfide_1146_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0014_klk2_cycpep_disulfide_1882_processed.pdb'][0]['id'], 'src': 'hda'}
        ]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    # ============================================================
    # 可视化 (Visualization)
    # ============================================================

    def test_ppi_analysis(self):
        tool_id = 'ppi_analysis'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdb'] = [
            {'id': self.data['rank0003_klk2_cycpep_disulfide_0259_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0004_klk2_cycpep_disulfide_0265_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0006_klk2_cycpep_disulfide_1281_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0007_klk2_cycpep_disulfide_0056_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0008_klk2_cycpep_disulfide_1149_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0009_klk2_cycpep_disulfide_1696_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0011_klk2_cycpep_disulfide_1146_processed.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['rank0014_klk2_cycpep_disulfide_1882_processed.pdb'][0]['id'], 'src': 'hda'}
        ]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_load_batch(self):
        tool_id = 'load_batch'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdbs'] = [{'id': self.data['7zkr_GABARAP.pdb'][0]['id'], 'src': 'hda'}]
        tool_input['native_pdb']['id'] = self.data['native.pdb'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_color_by_type(self):
        tool_id = 'color_by_type'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    # ============================================================
    # Peptide Forge
    # ============================================================

    def test_cycpep_mpnn(self):
        tool_id = 'cycpep_mpnn'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdbs'] = [
            {'id': self.data['7zkr_GABARAP_1.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['7zkr_GABARAP_15.pdb'][0]['id'], 'src': 'hda'}
        ]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_cycpep_flowpacker(self):
        tool_id = 'cycpep_flowpacker'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdbs'] = [
            {'id': self.data['7zkr_GABARAP_1.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['7zkr_GABARAP_15.pdb'][0]['id'], 'src': 'hda'}
        ]
        tool_input['input_fastas'] = [
            {'id': self.data['7zkr_GABARAP_1.fasta'][0]['id'], 'src': 'hda'},
            {'id': self.data['7zkr_GABARAP_15.fasta'][0]['id'], 'src': 'hda'}
        ]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_cycpep_af3score(self):
        tool_id = 'cycpep_af3score'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_pdbs'] = [{'id': self.data['7zkr_GABARAP.pdb'][0]['id'], 'src': 'hda'}]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_af3_filter(self):
        tool_id = 'af3_filter'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['metrics_csv']['id'] = self.data['AF3_Scoring.csv'][0]['id']
        tool_input['input_pdbs'] = [
            {'id': self.data['7zkr_GABARAP_1_0.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['7zkr_GABARAP_1_1.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['7zkr_GABARAP_1_2.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['7zkr_GABARAP_1_3.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['7zkr_GABARAP_1_4.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['7zkr_GABARAP_1_5.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['7zkr_GABARAP_15_0.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['7zkr_GABARAP_15_1.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['7zkr_GABARAP_15_2.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['7zkr_GABARAP_15_3.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['7zkr_GABARAP_15_4.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['7zkr_GABARAP_15_5.pdb'][0]['id'], 'src': 'hda'},
            {'id': self.data['7zkr_GABARAP_15_6.pdb'][0]['id'], 'src': 'hda'},
        ]
        del tool_input['input_fasta']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    # ============================================================
    # Aux Unit
    # ============================================================

    def test_gemmi_cif2pdb(self):
        tool_id = 'gemmi_cif2pdb'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_files'] = [{'id': self.data['8jjs.cif'][0]['id'], 'src': 'hda'}]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_merge_metrics(self):
        tool_id = 'merge_metrics'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_csvs'] = [{'id': self.data['metrics.csv'][0]['id'], 'src': 'hda'}]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_topk_ranker(self):
        tool_id = 'topk_ranker'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_csv']['id'] = self.data['metrics.csv'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_round_metrics(self):
        tool_id = 'round_metrics'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_csv']['id'] = self.data['metrics.csv'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_prune_structure_metrics(self):
        tool_id = 'prune_structure_metrics'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['metrics_csv']['id'] = self.data['metrics.csv'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_plot_af3score(self):
        tool_id = 'plot_af3score'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['input_csv']['id'] = self.data['AF3_Scoring.csv'][0]['id']

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')

    def test_pep_filter_peptides(self):
        tool_id = 'pep_filter_peptides'
        print(f"\n{'-'*70}")
        print(f"Testing {tool_id}")

        tool = self.tools.get_tool(tool_id=tool_id)
        input_examples = tool.inputs()
        print(f'input_examples: {input_examples}')

        tool_input = input_examples
        tool_input['metrics_csv']['id'] = self.data['metrics.csv'][0]['id']
        tool_input['input_pdbs'] = [{'id': self.data['7zkr_GABARAP.pdb'][0]['id'], 'src': 'hda'}]

        print(f'tool_input: {tool_input}')
        tool_output = self._run_tool(tool, tool_input)
        print(f'tool_output: {tool_output}')


if __name__ == '__main__':
    unittest.main()
