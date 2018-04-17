from __future__ import unicode_literals

from Project import Project

class SelectProjectsWithExpId:

    def __init__(self, cursor, expId, start, end, nextBlock):
        self.cursor = cursor
        self.expId = expId
        self.start = start
        self.end = end
        self.nextBlock = nextBlock
        
    def process(self):
        sql = """SELECT DISTINCT m.project_id, s.id AS session_id
                    FROM (select @experiment:="%s") unused, master_events m 
                    INNER JOIN sessions_for_experiment s ON m.session_id=s.id 
                    INNER JOIN sessions ses ON ses.id=m.session_id 
                    AND project_id IS NOT NULL
                    --WHERE ses.created_at BETWEEN %s AND %s"""

        data = (self.expId, self.start, self.end)
        print(sql % data)
        projects = set()
        queryResult = self.cursor.execute(sql, data)
        print(queryResult)
        for result in self.cursor.fetchall():
            print(".")
            if result['project_id'] not in projects:
                projects.add(result['project_id'])
                print("processing project %s..." % result['project_id'])
                project = Project(-1, result['session_id'], result['project_id'])
                self.nextBlock.process(project)