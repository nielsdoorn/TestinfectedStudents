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
    
   
