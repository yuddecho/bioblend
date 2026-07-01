from bioblend.galaxy import GalaxyInstance

from .base import GalaxyCtx, BaseTool, create_session

class Tool(BaseTool):
    def __init__(self, ctx: GalaxyCtx):
        super().__init__(ctx)
    
    def run(self, tool_id: str, inputs: dict) -> dict:
        try:
            tool_outputs = self.ctx.gi.tools.run_tool(history_id=self.ctx.history_id, tool_id=tool_id, tool_inputs=inputs)
        except Exception as e:
            raise RuntimeError(f"运行工具 {tool_id} 失败: {e}") from e

        keep = ['id', 'hid', 'name', 'file_ext']
        outputs = [{k: d[k] for k in keep} for d in tool_outputs['outputs']]

        keep = ['id', 'hid', 'name']
        output_collections = [{k: d[k] for k in keep} for d in tool_outputs['output_collections']]

        keep = ['id', 'state', 'tool_id', 'create_time']
        jobs = [{k: d[k] for k in keep} for d in tool_outputs['jobs']]

        return {'jobs': jobs, 'outputs': outputs, 'output_collections': output_collections}
    
class TransProtein:
    def __init__(self, url, key):
        self.ctx, self.history, self.tool, self.dataset, self.workflow = \
            create_session(url, key, Tool)

    def login(self, url, key):
        return GalaxyInstance(url, key)