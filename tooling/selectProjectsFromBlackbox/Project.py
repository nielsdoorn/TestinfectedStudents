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
