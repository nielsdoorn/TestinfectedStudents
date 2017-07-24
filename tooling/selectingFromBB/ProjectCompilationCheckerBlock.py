from __future__ import unicode_literals

from SourceFile import SourceFile

class ProjectCompilationCheckerBlock:

    def __init__(self, cursor, firstTime, lastTime, nextBlock):
        self.cursor = cursor
        self.firstTime = firstTime
        self.lastTime = lastTime        
        self.nextBlock = nextBlock
        
    def process(self, project):
        projectCompiles = True
        for f in project.files:
            # compiled successfully in the given timeframe
            sql = """
            SELECT 
                CE.success AS compiles,
                CE.id AS compileEventId,
                ME.id AS masterEventId
            FROM
                compile_inputs CI,
                compile_events CE,
                master_events ME
            WHERE
                CI.source_file_id=%s AND
                CE.id = CI.compile_event_id AND
                ME.event_id=CE.id AND
                ME.created_at BETWEEN %s AND %s
            ORDER BY CI.id DESC
            LIMIT 0,1
            """
            
            self.cursor.execute(sql, (f.sourceFileId, self.firstTime, self.lastTime))
            
            compileResult = self.cursor.fetchone()
            if compileResult is not None:
                if compileResult['compiles'] == 0:
                    projectCompiles = False 
                    break
                else:
                    f.masterEventId = compileResult['masterEventId']
            else:
                projectCompiles = False 
                break                
        if projectCompiles:
            self.nextBlock.process(project)
        
        
    
   
