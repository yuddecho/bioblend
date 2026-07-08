import os
import json
import yaml

from dataclasses import dataclass

from bioblend.galaxy import GalaxyInstance


class ToolNotAvailableError(Exception):
    """工具在 Galaxy 服务器上不可用"""
    pass


def create_session(url, key, tools_dir):
    """创建 Galaxy 会话，返回 (ctx, history, tool, dataset, workflow)"""
    gi = GalaxyInstance(url, key)
    try:
        history = gi.histories.get_most_recently_used_history()
    except Exception as e:
        raise ConnectionError(f"无法获取最近使用的历史记录: {e}") from e
    print(f"[History] now {history['id']}: {history['name']}")
    ctx = GalaxyCtx(gi, history['id'])
    return ctx, History(ctx), Tool(ctx, tools_dir), Dataset(ctx), Workflow(ctx)


@dataclass
class GalaxyCtx:
    gi: GalaxyInstance
    history_id: str

class History:
    def __init__(self, ctx: GalaxyCtx):
        self.ctx = ctx

    def create(self, name: str = None):
        try:
            new_history = self.ctx.gi.histories.create_history(name=name)
        except Exception as e:
            raise RuntimeError(f"创建历史记录失败: {e}") from e
        self.ctx.history_id = new_history['id']
        print(f"[History] create {self.ctx.history_id}: {new_history['name']}")

    def select(self, history_id: str):
        # 选择一个历史记录作为当前历史记录
        self.ctx.history_id = history_id
        history_name = self.ctx.gi.histories.show_history(history_id, contents=False)['name']
        print(f"[History] select {self.ctx.history_id}: {history_name}")
    
    def open(self):
        # 打开web, 并选择当前历史记录
        self.ctx.gi.histories.open_history(self.ctx.history_id)

    def delete(self, history_id: str = None, purge=False):
        # 删除历史记录; purge=True时，删除所有相关内容，不可恢复
        # history_id 为 None 时，删除当前历史记录
        if history_id is None:
            # 当前历史记录
            history_id = self.ctx.history_id

            # 将最近历史记录 设为 当前历史记录
            self.ctx.history_id = self.ctx.gi.histories.get_most_recently_used_history()['id']

        self.ctx.gi.histories.delete_history(history_id, purge=purge)

        print(f"[History] delete {history_id}: {self.ctx.gi.histories.show_history(history_id, contents=False)['name']}")
        
        print(f"[History] now {self.ctx.history_id}: {self.ctx.gi.histories.show_history(self.ctx.history_id, contents=False)['name']}")

    def info(self):
        # 打印所有历史记录信息
        print("id,\t name,\tcount(items),\t update_time")
        for h in self.ctx.gi.histories.get_histories():
            print(f"{h['id']},\t {h['name']},\t {h['count']},\t {h['update_time']}")

    def content(self, contents=True):
        # 获取历史记录信息; 
        # contents=False （默认值），则只会得到历史记录中包含的数据集的 ID 列表
        # contents=True ，则会得到每个数据集的元数据
        history_id = self.ctx.history_id
        history_info = self.ctx.gi.histories.show_history(history_id, contents=contents)

        if contents:
            if len(history_info) > 0:
                print("id,\t hid,\t deleted,\t name,\t create_time")
                for h in history_info:
                    print(f"{h['id']},\t {h['hid']},\t {h['deleted']},\t {h['name']},\t {h['create_time']}")
            else:
                print(f"No contents in this history: {self.ctx.history_id}")
        else:
            print(json.dumps(history_info, indent=4, ensure_ascii=False))

        return history_info
    
class Dataset:
    def __init__(self, ctx: GalaxyCtx):
        self.ctx = ctx
        self.data_type = ['pdb', 'mol2', 'sdf', 'smi', 'pdf', 'csv', 'cif', 'fasta', 'fastq', 'txt', 'xml', 'json', 'yaml', 'tsv', 'gff', 'gff3', 'bed', 'tar', 'zip', 'gz', 'bz2']

    def _upload_file(self, file_path: str):
        # 上传文件到当前历史记录
        file_type = file_path.split('.')[-1]
        if file_type not in self.data_type:
            file_type = 'auto'

        # 文件类型指定不起作用
        try:
            res = self.ctx.gi.tools.upload_file(file_path, self.ctx.history_id, file_type=file_type)
        except Exception as e:
            raise RuntimeError(f"上传文件失败 {file_path}: {e}") from e
        return res['outputs'][0]

    def upload(self, file_path: str = None, file_dir: str = None):
        # 上传文件到当前历史记录
        if file_path is None and file_dir is None:
            raise ValueError("file_path or file_dir should be provided")
        
        files = []
        
        if file_path:
            files.append(self._upload_file(file_path))

        if file_dir:
            # 上传目录下所有文件到当前历史记录
            for _root, _, _files in os.walk(file_dir):
                for file_name in _files:
                    if file_name.endswith('.md') or file_name == '.DS_Store':
                        continue
                    file_path = os.path.join(_root, file_name)
                    files.append(self._upload_file(file_path))

        data = {}
        for file in files:
            if file['name'] not in data:
                data[file['name']] = []

            data[file['name']].append({'hid': file['hid'], 'id': file['id'], 'file_ext': file['file_ext']})

        return data
    
    def download(self, dataset_id: str, file_path: str):
        # 下载数据集到本地
        self.ctx.gi.datasets.download_dataset(dataset_id, file_path)
    
    def delete(self, dataset_id: str):
        # 删除数据集
        self.ctx.gi.datasets.delete_dataset(dataset_id)
    
    def info(self, dataset_id: str):
        # 获取数据集信息
        dataset_info = self.ctx.gi.datasets.show_dataset(dataset_id)
        return dataset_info
    
    def get(self):
        # 获取当前历史记录中的所有数据集信息
        history_id = self.ctx.history_id
        history_info = self.ctx.gi.histories.show_history(history_id, contents=True)
        data = {}
        if len(history_info) > 0:
            for h in history_info:
                if h['name'] not in data:
                    data[h['name']] = []

                data[h['name']].append({'hid': h['hid'], 'id': h['id'], 'content_type': h['history_content_type'], 'file_type': h.get('extension', None)})

        return data

class BaseTool:
    def __init__(self, ctx: GalaxyCtx):
        self.ctx = ctx
        self.tools = self.ctx.gi.tools.get_tool_panel()
        self.tool_dict = self._get_tool_dict()

    def info(self):
        print('id,\t name,\t description')
        for tool_section in self.tools:
            for tool in tool_section['elems']:
                name = tool.get('name') or tool.get('text', 'N/A')
                desc = tool.get('description', 'N/A')
                print(f'{tool["id"]},\t {name},\t {desc}')

    def _get_tool_dict(self):
        tool_dict = {}
        for tool_section in self.tools:
            for tool in tool_section['elems']:
                name = tool.get('name')
                if name:
                    tool_dict[name] = tool['id']
        return tool_dict

class Tool(BaseTool):
    def __init__(self, ctx: GalaxyCtx, tools_dir: str):
        super().__init__(ctx)
        self.tools_dir = tools_dir
        self.warnings = []

    def get_tool(self, tool_id: str = None, tool_name: str = None) -> "RunTool":
        if tool_id is None and tool_name is None:
            raise ValueError("tool_id or tool_name should be provided")

        if tool_name:
            _tool_id = self.tool_dict.get(tool_name, None)
            if _tool_id is None:
                raise ValueError(f"tool_name {tool_name} not found, please check tool name in tool panel: {self.tool_dict}")
            elif tool_id and tool_id != _tool_id:
                raise ValueError(f"tool_name {tool_name} not match tool_id {tool_id}, please check tool name in tool panel: {self.tool_dict}")

            tool_id = _tool_id

        if tool_id not in self.tool_dict.values():
            msg = f"[WARNING] tool_id {tool_id} 未在 Galaxy 工具面板中找到，可能未安装"
            self.warnings.append(msg)

        tool_path = os.path.join(self.tools_dir, f"{tool_id}.yaml")
        if not os.path.exists(tool_path):
            raise ValueError(f"YAML 配置 {tool_id}.yaml 不存在")

        return RunTool(self.ctx, tool_path)

    def show_warnings(self):
        if self.warnings:
            print(f"\n{'='*60}")
            print(f"工具面板警告汇总 ({len(self.warnings)} 个)")
            print(f"{'='*60}")
            for w in self.warnings:
                print(w)
            print(f"{'='*60}\n")


class RunTool:
    def __init__(self, ctx: GalaxyCtx, tool_path: str):
        self.ctx = ctx
        with open(tool_path, encoding='utf-8') as f:
            self.tool_config = yaml.safe_load(f)

    def info(self):
        return self.tool_config

    def inputs(self):
        return self.tool_config['input_examples']

    def _clean_inputs(self, inputs):
        """递归清理 id 为 None 的可选 data 输入，避免 Galaxy 400 错误"""
        if isinstance(inputs, dict):
            if inputs.get('id') is None and 'src' in inputs:
                return None
            return {k: v for k, v in ((k, self._clean_inputs(v)) for k, v in inputs.items()) if v is not None}
        elif isinstance(inputs, list):
            return [item for item in (self._clean_inputs(i) for i in inputs) if item is not None]
        return inputs

    def run(self, inputs: dict) -> dict:
        try:
            tool_outputs = self.ctx.gi.tools.run_tool(
                history_id=self.ctx.history_id, tool_id=self.tool_config['id'],
                tool_inputs=self._clean_inputs(inputs)
            )
        except Exception as e:
            error_msg = str(e)
            if "Tool not found" in error_msg:
                raise ToolNotAvailableError(f"工具 {self.tool_config['id']} 在服务器上不可用") from e
            raise RuntimeError(f"运行工具 {self.tool_config['id']} 失败: {e}") from e

        keep = ['id', 'hid', 'name', 'file_ext']
        outputs = [{k: d[k] for k in keep} for d in tool_outputs['outputs']]

        keep = ['id', 'hid', 'name']
        output_collections = [{k: d[k] for k in keep} for d in tool_outputs['output_collections']]

        keep = ['id', 'state', 'tool_id', 'create_time']
        jobs = [{k: d[k] for k in keep} for d in tool_outputs['jobs']]

        return {'jobs': jobs, 'outputs': outputs, 'output_collections': output_collections}


class Workflow:
    def __init__(self, ctx: GalaxyCtx):
        self.ctx = ctx
        self.workflow_id = None
        self.workflow_content = None
        self.workflow_id_dict = []
        self.init()

    def init(self):
        workflows = self.ctx.gi.workflows.get_workflows()
        if len(workflows) > 0:
            self.workflow_id = workflows[0]['id']
            self.workflow_content = self.ctx.gi.workflows.show_workflow(self.workflow_id)

            print(f"[Workflow] now {self.workflow_id}: {self.workflow_content['name']}")

            for w in workflows:
                self.workflow_id_dict.append(w['id'])

        else:
            print("No workflow found")

    def info(self):
        workflows = self.ctx.gi.workflows.get_workflows()
        if len(workflows) > 0:
            print("\nid\tname\tupdate_time")
            for w in workflows:
                print(f"{w['id']}\t{w['name']}\t{w['update_time']}")
        else:
            print("No workflow found")
    
    def select(self, workflow_id: str):
        if workflow_id not in self.workflow_id_dict:
            raise ValueError(f"workflow_id {workflow_id} not found, please check workflow id in workflow list: {self.workflow_id_dict}")
        
        self.workflow_id = workflow_id
        self.workflow_content = self.ctx.gi.workflows.show_workflow(self.workflow_id)

        print(f"[Workflow] select {self.workflow_id}: {self.workflow_content['name']}")

    def content(self):
        return self.workflow_content
    
    def export(self, file_path: str = 'workflow.json'):
        workflow_json = self.ctx.gi.workflows.export_workflow_dict(self.workflow_id)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(workflow_json, f, ensure_ascii=False, indent=4)

        print(f"[Workflow] export {self.workflow_id}: {self.workflow_content['name']} to {file_path}")
    
    def load(self, file_path: str):
        if not os.path.exists(file_path):
            raise ValueError(f"file_path {file_path} not found")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            workflow_json = json.load(f)

        res = self.ctx.gi.workflows.import_workflow_dict(workflow_json)

        self.workflow_id = res['id']
        self.workflow_content = self.ctx.gi.workflows.show_workflow(self.workflow_id)

        print(f"[Workflow] load {self.workflow_id}: {self.workflow_content['name']}")


    def run(self, inputs: dict) -> dict:
        try:
            outputs = self.ctx.gi.workflows.invoke_workflow(
                history_id=self.ctx.history_id, workflow_id=self.workflow_id, inputs=inputs
            )
        except Exception as e:
            raise RuntimeError(f"运行工作流失败: {e}") from e
        return outputs
