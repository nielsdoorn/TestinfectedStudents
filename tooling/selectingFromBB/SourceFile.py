from __future__ import unicode_literals

class SourceFile:    
    def __init__(self, sourceFileId, name, masterEventId=None):
        self.sourceFileId = sourceFileId
        self.name = unicode(name)
        self.masterEventId = masterEventId

    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return "sourcefileid: %s mastereventid: %s" % (self.sourceFileId, self.masterEventId)
