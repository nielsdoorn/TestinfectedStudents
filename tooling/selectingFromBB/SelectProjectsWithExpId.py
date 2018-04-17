from __future__ import unicode_literals

from Project import Project

class SelectProjectsWithExpId:

    def __init__(self, cursor, expId, start, end, nextBlock):
        self.cursor = cursor
        self.expId = expId
        self.start = start
        self.end = end
        self.sessions = set()
        self.nextBlock = nextBlock
        
    def process(self):
        sql = """SELECT DISTINCT m.project_id, s.id AS session_id
                    FROM (select @experiment:="%s") unused, master_events m 
                    INNER JOIN sessions_for_experiment s ON m.session_id=s.id 
                    INNER JOIN sessions ses ON ses.id=m.session_id 
                    AND project_id IS NOT NULL
                    WHERE ses.created_at BETWEEN '%s' AND '%s'"""
        print(sql % (self.expId, self.start, self.end))
        self.cursor.execute(sql, (self.expId, self.start, self.end))
        projectsResult = self.cursor.fetchall()
        if len(projectsResult) > 0:
            for projectResult in projectsResult:
                print("processing project %s..." % projectResult['project_id'])
                project = Project(-1, projectResult['session_id'], projectResult['project_id'])
                self.nextBlock.process(project)