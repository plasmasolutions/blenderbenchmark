#encoding: UTF-8
import DataProvider_Xml
import subprocess, os
import hashlib
import BlenderUtils
import ResultSet

class BlenderBenchmarkClass(object):
	"""Represents the heart of this script. It can fetch Blenders version information,
	run Blender, add render tasks and parse Blenders result strings"""
	def __init__(self):
		self.DebugMode = True
		self.BuildInformation = []
		self._renderTasks = []
		self._executables = []
		self._scriptDir = os.path.dirname(os.path.realpath(__file__))

		#self._dataProvider = DataProvider_Xml.XmlDataProviderClass('test.xml')
		#self._dataProvider.Initialize()
		

	def _createPopenFriendlyPath(self,Path):
		return Path.replace(' ',self._spaceMarker)

	def AddExecutable(self,Path):
		self._executables.append(Path)

	def AddRenderTask(self,PathAndFile, Frame = 1):
		self._renderTasks.append([PathAndFile, Frame])

	def Render(self):
		# Loop trough all blender versions
		for (index, executable) in enumerate(self._executables):

			#Create a result container and create a new result set
			resultSet = ResultSet.ResultSetClass()
			
			# and get the build information
			resultSet.SetBuildInformation(BlenderUtils.GetBlenderVersionInformation(self._executables[index]))

			# then render all files, one after another
			for renderTask in self._renderTasks:

				print(">> Rendering "+ renderTask[0] + " with Blender version " + resultSet.BuildInformation["release"])
				
				# --engine CYCLES BLENDER_RENDER
				md5 = hashlib.md5(open(renderTask[0],'rb').read()).hexdigest()
				imageoutput = "../images/results/"+ md5 + "_" + resultSet.BuildInformation["hash"] + "_"

				for line in BlenderUtils.RunCommand(executable + 
					" -b " + renderTask[0] + 
					#" -o " + imageoutput +
					" -F PNG  -x 1 -f "+ str(renderTask[1])):

					#print(line.decode("utf-8"))

					# And look if the result is available already
					# btw. this is pretty weak - if "Saved:" is not recognized, the complete test result will vanish :(
					if line.decode("utf-8").find('Saved: ') > -1:
						consoleLine = line.decode("utf-8").split()
						resultSet.AddResult({"filename":os.path.basename(renderTask[0]), "rendertime": consoleLine[3], "savetime":consoleLine[5].replace('(', '').replace(')', ''), "md5":md5, "frame": str(renderTask[1]).zfill(4)})
						
			print(resultSet.Results)
			#Add the results
			#self._resultSetHandler.AddResultSet(resultSet)

		# All done, save result
		# self._resultSetHandler.WriteToXml('../data/results.xml');

	def DownloadNewestOfficialBlender(self, Path):
		# Path is existant?
		# Download file depending on platform
		# Extract it
		pass

# Create a new Benchmark object
Benchmark = BlenderBenchmarkClass()

# Add as many blender versions as you'd like to test
Benchmark.AddExecutable("/opt/Blender/Official/blender-2.70-linux-glibc211-x86_64/blender")
Benchmark.AddExecutable("/opt/Blender/Official/blender-2.70a-linux-glibc211-x86_64/blender")

#Add as many files as you'd like to render. And keep in mind: every file is rendered with every executable
Benchmark.AddRenderTask("/mnt/iData/Projekte/Grafik/3D/BlenderTests/LEGO/StoneCollection.blend")
Benchmark.AddRenderTask("/mnt/iData/Projekte/Grafik/3D/BlenderTests/Cycles/Christmas.blend")

# Finally, Render
Benchmark.Render()

# Ideas:

# RenderTask -> Blender Projekt-Datei
  # task = Benchmark.AddRenderTask(Blendfile [Frame, Length])
  # Benchmark.RemoveRenderTask(Blendfile) # Removes the given file from the task list
  # Benchmark.ReRender() # Renders every file, no matter if it has been rendered before
  # Benchmark.Render() # Renders only the file that have not been rendered yet

# RenderTarget -> Blenderversion
  # target = AddRenderTarget(Path) ## fügt neue Blenderversion in Provider ein,
  #  Provider muss dabei alle Informationen über Blender herausfinden. Falls bereits selbe Version an anderem Ort existiert
