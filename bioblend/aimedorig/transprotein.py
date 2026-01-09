import yaml

from bioblend.galaxy import GalaxyInstance

from .base import GalaxyCtx, History, Dataset, BaseTool, Workflow

class Tool(BaseTool):
    def __init__(self, ctx: GalaxyCtx):
        super().__init__(ctx)
    
    def run(self, tool_id: str, inputs: dict) -> dict:    
        tool_outputs = self.ctx.gi.tools.run_tool(history_id=self.ctx.history_id, tool_id=tool_id, tool_inputs=inputs)

        keep = ['id', 'hid', 'name', 'file_ext']
        outputs = [{k: d[k] for k in keep} for d in tool_outputs['outputs']]

        keep = ['id', 'hid', 'name']
        output_collections = [{k: d[k] for k in keep} for d in tool_outputs['output_collections']]

        keep = ['id', 'state', 'tool_id', 'create_time']
        jobs = [{k: d[k] for k in keep} for d in tool_outputs['jobs']]

        return {'jobs': jobs, 'outputs': outputs, 'output_collections': output_collections}
    
class TransProtein:
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
    # {"history_id":"2e2eb5d9fff58821","tool_id":"rf_diffusion","tool_version":"0.0.1","inputs":{"contigs":"50-50","num_designs":"2"}}
    tool_id = 'rf_diffusion'
    print(f"\n----------------------------------------------------------------------")
    print(f"Testing {tool_id}")

    tool_input = {"contigs":"50-50","num_designs":"2"}

    print(f'tool_input: {tool_input}')

    # 运行工具，提取药效团
    tool_output = tools.run(tool_id, tool_input)
    print(f'tool_output: {tool_output}')

if __name__ == '__main__':
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    trans_molecule = TransProtein(config['transprotein_url'], config['transprotein_api_key'])

    trans_molecule.history.select('2e2eb5d9fff58821')

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