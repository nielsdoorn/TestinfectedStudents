from __future__ import unicode_literals

class Project:    
    def __init__(self, userId, sessionId, projectId):
        self.userId = userId
        self.sessionId = sessionId
        self.projectId = projectId
        self.files = set()

    def numOfFiles(self):
        return len(self.files)

    def __str__(self):
        result = u"%s,%s,%s,%s" % (self.userId, self.sessionId, self.projectId, self.files)
	return result
