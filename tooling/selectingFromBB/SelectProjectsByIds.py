from __future__ import unicode_literals

from Project import Project

class SelectProjectsByIds:

    def __init__(self, projects, nextBlock):
        self.projects = projects
        self.nextBlock = nextBlock
        
    def process(self):
        for project in self.projects:
            project = Project(-1, -1, project)
            self.nextBlock.process(project)
        print("done")