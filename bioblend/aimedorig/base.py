import os
import json

from dataclasses import dataclass

from bioblend.galaxy import GalaxyInstance

@dataclass
class GalaxyCtx:
    gi: GalaxyInstance
    history_id: str

class History:
    def __init__(self, ctx: GalaxyCtx):
        self.ctx = ctx

    def create(self, name: str = None):
        # 创建一个新的历史记录，并设为当前历史记录
        new_history = self.ctx.gi.histories.create_history(name=name)
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
        res = self.ctx.gi.tools.upload_file(file_path, self.ctx.history_id, file_type=file_type)
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
                print(f'{tool["id"]},\t {tool["name"]},\t {tool["description"]}')

    def _get_tool_dict(self):
        tool_dict = {}
        for tool_section in self.tools:
            for tool in tool_section['elems']:
                tool_dict[tool['name']] = tool['id']
        return tool_dict

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
    
    def selct(self, workflow_id: str):
        if workflow_id not in self.workflow_id_dict:
            raise ValueError(f"workflow_id {workflow_id} not found, please check workflow id in workflow list: {self.workflow_dict}")
        
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
        # 运行工作流
        outputs = self.ctx.gi.workflows.invoke_workflow(history_id=self.ctx.history_id, workflow_id=self.workflow_id, inputs=inputs)

        return outputs
