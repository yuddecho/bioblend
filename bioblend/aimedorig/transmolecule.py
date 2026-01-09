import os
import ast
import yaml

from bioblend.galaxy import GalaxyInstance

from .base import GalaxyCtx, History, Dataset, BaseTool, Workflow

import importlib.resources as res  # Py3.9+

# # 一次性把 tools 目录当成“资源目录”
TRANSMOLECULE_TOOLS = res.files(__package__) / "transmolecule_tools"
# TRANSMOLECULE_TOOLS = "./transmolecule_tools"

class Tool(BaseTool):
    def __init__(self, ctx: GalaxyCtx):
        super().__init__(ctx)
        self.tool_path = os.path.join(TRANSMOLECULE_TOOLS, "transmolecule.yaml")

    def get_tool(self, tool_id: str = None, tool_name: str = None) -> BaseTool:
        # tool_id 和 tool_name 至少需要提供一个
        if tool_id is None and tool_name is None:
            raise ValueError("tool_id or tool_name should be provided")
        
        if tool_name:
            _tool_id = self.tool_dict.get(tool_name, None)
            if _tool_id is None:
                raise ValueError(f"tool_name {_tool_id} not found, please check tool name in tool panel: {self.tool_dict}")
            elif tool_id and tool_id != _tool_id:
                raise ValueError(f"tool_name {tool_name} not match tool_id {tool_id}, please check tool name in tool panel: {self.tool_dict}")
            
            tool_id = _tool_id
        
        tool_path = f"{TRANSMOLECULE_TOOLS}/{tool_id}.yaml"
        if not os.path.exists(tool_path):
            raise ValueError(f"tool_id {tool_id}.yaml not found, please check tool id in tool panel: {self.tool_dict}")
        
        return RunTool(self.ctx, tool_path)
    
class RunTool():
    def __init__(self, ctx: GalaxyCtx, tool_path: str):
        self.ctx = ctx
        with open(tool_path, encoding='utf-8') as f:
            self.tool_config = yaml.safe_load(f)

    def info(self):
        # print(json.dumps(self.tool_config, indent=4, ensure_ascii=False))
        return self.tool_config

    def inputs(self):
        return ast.literal_eval(self.tool_config['input_exampels'])
    
    def run(self, inputs: dict) -> dict:    
        tool_outputs = self.ctx.gi.tools.run_tool(history_id=self.ctx.history_id, tool_id=self.tool_config['id'], tool_inputs=inputs)

        keep = ['id', 'hid', 'name', 'file_ext']
        outputs = [{k: d[k] for k in keep} for d in tool_outputs['outputs']]

        keep = ['id', 'hid', 'name']
        output_collections = [{k: d[k] for k in keep} for d in tool_outputs['output_collections']]

        keep = ['id', 'state', 'tool_id', 'create_time']
        jobs = [{k: d[k] for k in keep} for d in tool_outputs['jobs']]

        return {'jobs': jobs, 'outputs': outputs, 'output_collections': output_collections}
    
class TransMolecule:
    def __init__(self, url, key):
        gi = self.login(url, key)
        history = gi.histories.get_most_recently_used_history()
        print(f"[History] now {history['id']}: {history['name']}")

        self.ctx = GalaxyCtx(gi, history['id'])
        self.history = History(self.ctx)
        self.tool = Tool(self.ctx)
        self.dataset = Dataset(self.ctx)
        self.workflow = Workflow(self.ctx)

    def login(self, url, key):
        return GalaxyInstance(url, key)
    
def test_pharma(tools, data):
    tool_id = 'pharma'
    print(f"\n----------------------------------------------------------------------")
    print(f"Testing {tool_id}")

    # 获取工具，传入id或者name
    tool = tools.get_tool(tool_id=tool_id)

    # 获取工具输入示例
    input_exampels = tool.inputs()
    print(f'input_exampels: {input_exampels}')

    # 构建输入，将上传的文件数据的id放到对应value
    tool_input = input_exampels

    tool_input['pdb_file']['id'] = data['receptor.pdb'][0]['id']
    tool_input['sdf_file']['id'] = data['ligand.sdf'][0]['id']

    print(f'tool_input: {tool_input}')

    # 运行工具，提取药效团
    tool_output = tool.run(tool_input)
    print(f'tool_output: {tool_output}')

if __name__ == '__main__':
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    trans_molecule = TransMolecule(config['transmolecule_url'], config['transmolecule_api_key'])

    trans_molecule.history.select('9082c3dc6588cf4d')

    # trans_molecule.history.create(name='test_history1')

    # 获取当前用户所有历史记录信息
    trans_molecule.history.info()

    # 获取当前历史记录数据信息
    # trans_molecule.history.content()
    
    # 获取工具信息
    # trans_molecule.tool.info()

    tools = trans_molecule.tool
    data = trans_molecule.dataset.get()
    print(f"data: {data}")
    test_pharma(tools, data)