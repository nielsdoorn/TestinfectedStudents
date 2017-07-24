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

from SourceFile import SourceFile

class ProjectTestCheckerBlock:

    def __init__(self, cursor, minClasses, nextBlock):
        self.cursor = cursor
        self.minClasses = minClasses
        self.nextBlock = nextBlock
        
    def process(self, project):
        sql = "SELECT * FROM source_files WHERE project_id=%s AND name LIKE %s"
        self.cursor.execute(sql, (project.projectId, '_%Test.java'))
        testFilesInProject = self.cursor.fetchall()
        if len(testFilesInProject) > 0:      
            sql = "SELECT * FROM source_files WHERE project_id=%s"
            self.cursor.execute(sql, project.projectId)
            filesInProject = self.cursor.fetchall()
            if len(filesInProject) >= self.minClasses:
                for file in filesInProject:
                    project.files.add(SourceFile(file['id'], file['name']))
                self.nextBlock.process(project)
        
        
    
   
