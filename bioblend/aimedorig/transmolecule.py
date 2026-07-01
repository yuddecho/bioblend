import os
import yaml

from bioblend.galaxy import GalaxyInstance

from .base import GalaxyCtx, BaseTool, create_session

import importlib.resources as res  # Py3.9+

# # 一次性把 tools 目录当成“资源目录”
TRANSMOLECULE_TOOLS = res.files(__package__) / "transmolecule_tools"
# TRANSMOLECULE_TOOLS = "./transmolecule_tools"

class Tool(BaseTool):
    def __init__(self, ctx: GalaxyCtx):
        super().__init__(ctx)

    def get_tool(self, tool_id: str = None, tool_name: str = None) -> "RunTool":
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
        return self.tool_config['input_examples']
    
    def run(self, inputs: dict) -> dict:
        try:
            tool_outputs = self.ctx.gi.tools.run_tool(
                history_id=self.ctx.history_id, tool_id=self.tool_config['id'], tool_inputs=inputs
            )
        except Exception as e:
            raise RuntimeError(f"运行工具 {self.tool_config['id']} 失败: {e}") from e

        keep = ['id', 'hid', 'name', 'file_ext']
        outputs = [{k: d[k] for k in keep} for d in tool_outputs['outputs']]

        keep = ['id', 'hid', 'name']
        output_collections = [{k: d[k] for k in keep} for d in tool_outputs['output_collections']]

        keep = ['id', 'state', 'tool_id', 'create_time']
        jobs = [{k: d[k] for k in keep} for d in tool_outputs['jobs']]

        return {'jobs': jobs, 'outputs': outputs, 'output_collections': output_collections}
    
class TransMolecule:
    def __init__(self, url, key):
        self.ctx, self.history, self.tool, self.dataset, self.workflow = \
            create_session(url, key, Tool)

    def login(self, url, key):
        return GalaxyInstance(url, key)
