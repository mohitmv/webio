import time, datetime

class Object(dict):
  def __init__(self, initial_value={}, **kwargs):
    self.__dict__ = self;
    dict.__init__(self, initial_value, **kwargs);

def GetEpochTimenow():
  return int(time.mktime(datetime.datetime.now().timetuple()));


