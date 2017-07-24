from __future__ import unicode_literals

class UserCheckerBlock:

    def __init__(self, cursor, nextBlock):
        self.cursor = cursor
        self.nextBlock = nextBlock
        self.users = set()
        
    def process(self, project):
        sql = "SELECT user_id FROM projects WHERE id=%s"
        self.cursor.execute(sql, (project.projectId))
        userResult = self.cursor.fetchone()
        userId = userResult['user_id']
        project.userId = userId
        if userId not in self.users:
            self.nextBlock.process(project)
            self.users.add(userId)
    
   
