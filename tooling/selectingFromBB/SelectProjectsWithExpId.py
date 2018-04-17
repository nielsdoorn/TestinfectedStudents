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
                    WHERE ses.created_at BETWEEN %s AND %s"""

        data = (self.expId, self.start, self.end)
        print(sql % data)
        projects = set()
        with self.cursor as cursor:
            queryResult = cursor.execute(sql, data)
            results = cursor.fetchall()
        print(results)
        if len(results) > 0:
            for result in results:
                print(".")
                if result['project_id'] not in projects:
                    projects.add(result['project_id'])
                    print("processing project %s..." % result['project_id'])
                    project = Project(-1, result['session_id'], result['project_id'])
                    self.nextBlock.process(project)
        else:
            print("no results")