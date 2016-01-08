class ResultSetClass(object):
	"""Represents a result set with rendering result(s) for a specific blender version"""
	def __init__(self):
		self.Results = []
		self.BuildInformation = {"hash":None,"platform":None, "release":None, "builddate":None, "commitdate": None, "committime":None}

	def SetBuildInformation(self,BuildInformation):
		self.BuildInformation = BuildInformation

	def AddResult(self,Result):
		self.Results.append(Result)
