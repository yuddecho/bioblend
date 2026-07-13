import importlib.resources as res

from bioblend.galaxy import GalaxyInstance

from .base import create_session

TRANSCYCLICPEPTIDE_TOOLS = str(res.files(__package__) / "transcyclicpeptide_tools")


class TransCyclicPeptide:
    def __init__(self, url, key):
        self.ctx, self.history, self.tool, self.dataset, self.workflow = \
            create_session(url, key, TRANSCYCLICPEPTIDE_TOOLS)

    def login(self, url, key):
        return GalaxyInstance(url, key)
