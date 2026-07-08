import os
import yaml

from bioblend.galaxy import GalaxyInstance

from .base import GalaxyCtx, BaseTool, create_session, ToolNotAvailableError

import importlib.resources as res  # Py3.9+

# 一次性把 tools 目录当成"资源目录"
TRANSMOLECULE_TOOLS = str(res.files(__package__) / "transmolecule_tools")


class TransMolecule:
    def __init__(self, url, key):
        self.ctx, self.history, self.tool, self.dataset, self.workflow = \
            create_session(url, key, TRANSMOLECULE_TOOLS)

    def login(self, url, key):
        return GalaxyInstance(url, key)
