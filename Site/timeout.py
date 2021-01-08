import threading, datetime

from flask import g
from _datetime import datetime
import os

active = False
localTime = {}
base = "/home/finnk/Programming/Projects/python/Streaming Server Frontend"
archiveLocation = "/archive"
liveLocation = "/live"

class _liveCheck(threading.Thread):
    def __init__(self, thread_name, thread_ID):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID= thread_ID
        self.localTimes = {}
    
    def run(self):
        while True:
            now = datetime.datetime.now()
            for streamLive in g.streamsLife:
                if streamLive[0] in self.localTimes:
                    elapsedTime = now - self.localTimes[streamLive[0]]
                    if elapsedTime.total_seconds() > 20:
                        del(self.localTimes,streamLive[0])
                        del(g.streamsLife,streamLive)
                        self._remove_stream_from_live(uid)
                    
            
    def _remove_stream_from_live(self, uid):
        pass
        

def checkforStreams():
    if not active:
        _liveCheck("checkForConnections","83").run()