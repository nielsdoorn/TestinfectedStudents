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
        
        
    
   
