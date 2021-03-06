from __future__ import unicode_literals

from SourceFile import SourceFile

class ProjectSizeCheckerBlock:

    def __init__(self, cursor, minClasses, nextBlock):
        self.cursor = cursor
        self.minClasses = minClasses
        self.nextBlock = nextBlock
        
    def process(self, project):
        sql = "SELECT * FROM source_files WHERE project_id=%s"
        self.cursor.execute(sql, project.projectId)
        filesInProject = self.cursor.fetchall()
        if len(filesInProject) >= self.minClasses:
            for file in filesInProject:
                project.files.add(SourceFile(file['id'], file['name']))
            self.nextBlock.process(project)
        
        
    
   
