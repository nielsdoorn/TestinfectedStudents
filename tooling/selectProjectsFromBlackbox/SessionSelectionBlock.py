#
# Copyright 2017 Niels Doorn Licensed under the Educational
# Community License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License at
# 
# http://opensource.org/licenses/ECL-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
from __future__ import unicode_literals

from random import randint
from Project import Project

class SessionSelectionBlock:

    def __init__(self, cursor, firstTime, lastTime, nextBlock, firstSession=None, lastSession=None):
        self.cursor = cursor
        self.firstTime = firstTime
        self.lastTime = lastTime
        
        if firstSession is None:
            self.firstSession = self.getFirstSessionId()
        else:
            self.firstSession = firstSession
        if lastSession is None:
            self.lastSession = self.getLastSessionId()
        else:
            self.lastSession = lastSession
            
        self.sessions = set()
        self.nextBlock = nextBlock
        
    def process(self):
        id = randint(self.firstSession, self.lastSession)
        if id not in self.sessions:
            self.sessions.add(id)
            sql = "SELECT DISTINCT project_id FROM master_events WHERE session_id=%s AND project_id IS NOT NULL"
            self.cursor.execute(sql, id)
            projectsResult = self.cursor.fetchall()
            if len(projectsResult) > 0:
                for projectResult in projectsResult:
                    project = Project(-1, id, projectResult['project_id'])
                    self.nextBlock.process(project)
        
    
    def getFirstSessionId(self):
        print ("finding first session for timeframe %s-%s" % (self.firstTime, self.lastTime))
        sql = "SELECT s.id FROM sessions s WHERE s.created_at >= %s ORDER BY s.id ASC LIMIT 0,1;" 
        self.cursor.execute(sql, self.firstTime)
        project = self.cursor.fetchone()
        firstId = project['id']
        print("first id is %s" % firstId)
        return firstId
    
    def getLastSessionId(self):
        print ("finding last session for timeframe %s-%s" % (self.firstTime, self.lastTime))
        sql = "SELECT s.id FROM sessions s WHERE s.created_at <= %s ORDER BY s.id DESC LIMIT 0,1;"    
        self.cursor.execute(sql, self.lastTime)
        project = self.cursor.fetchone()
        lastId = project['id']
        print("last id is %s" % lastId)
        return lastId    
