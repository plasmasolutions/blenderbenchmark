#encoding: UTF-8
import DataProvider_Sqlite
import subprocess, os
import hashlib

class BlenderBenchmarkClass(object):
	"""Represents the heart of this script. It can fetch Blenders version information,
	run Blender, add render tasks and parse Blenders result strings"""
	def __init__(self):
		self.DebugMode = True
		self.BuildInformation = []
		self._renderTasks = []
		self._executables = []
		self._scriptDir = os.path.dirname(os.path.realpath(__file__))
		self._dataProvider = DataProvider_Sqlite.DataProviderClass()
		self._dataProvider.Initialize()
		
	# Fancy workaround for Popen: As the command + parameters has to be split in parts and paths with 
	# a space would therefore be split too I mark those spaces with "<". This should be replaced whenever
	# a path is to be used
	def _createPopenFriendlyPath(self,Path):
		return Path.replace(' ',self._spaceMarker)

	def AddExecutable(self,Path):
		self._executables.append(Path)
   
	def AddRenderTask(self,PathAndFile, Frame = 1):
		self._renderTasks.append([PathAndFile, Frame])
	   
	def Render(self):
		# Loop trough all blender versions
		for (index, executable) in enumerate(self._executables):
			# Search in db for the current executable, get the id back.
			# Insert in db if not found

			#Create a result container and assign a new result set
			resultSet = ResultSet.ResultSetClass()
			
			# and get the build information
			resultSet.AddBuildInformation(BlenderUtils.GetBlenderVersionInformation(index))

			# then render all files, one after another
			for project in self._renderTasks:
				renderInfo ='Error'

				print(">> Rendering "+ project[0] + " with " + resultSet.BuildInformation["release"])
				
				# --engine CYCLES BLENDER_RENDER
				md5 = hashlib.md5(open(project[0]).read()).hexdigest()
				imageoutput = "../images/results/"+ md5 + "_" + resultSet.BuildInformation["hash"] + "_"
				for line in self._runCommand(executable + " -b " + self._createPopenFriendlyPath(project[0]) + " -o " + self._createPopenFriendlyPath(imageoutput) + " -F PNG  -x 1 -f "+ str(project[1]), self._spaceMarker ):
					# and look if the result is available already
					if line.find('Saved: ') > -1:
						renderInfo = line.decode("utf-8").split()
						#create md5 hash
						resultSet.AddResult({"filename":os.path.basename(project[0]), "rendertime": renderInfo[3], "savetime":renderInfo[5].replace('(', '').replace(')', ''), "md5":md5, "frame": str(project[1]).zfill(4)})
					print(line.strip())
			
			#Add the results
			#self._resultSetHandler.AddResultSet(resultSet)

		# All done, save result
		#self._resultSetHandler.WriteToXml('../data/results.xml');

	def DownloadFile(self, Url):
		file_name = Url.split('/')[-1]
		u = urllib2.urlopen(Url)
		f = open(file_name, 'wb')
		meta = u.info()
		file_size = int(meta.getheaders("Content-Length")[0])
		print("Downloading: %s kBytes: %s" % (file_name, file_size/1024))

		file_size_dl = 0
		block_sz = 8192
		while True:
			buffer = u.read(block_sz)
			if not buffer:
				break

			file_size_dl += len(buffer)
			f.write(buffer)
			status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
			status = status + chr(8)*(len(status)+1)
			print(status,)

		f.close()

	def DownloadNewestBuildbot(self, Path):
		# Path is existant?
		# Download file depending on platform
		# Extract it

		pass

# Setup
Benchmark = BlenderBenchmarkClass()
Benchmark.AddExecutable("/opt/Blender/Official/blender-2.70a-linux-glibc211-x86_64/blender")
Benchmark.AddExecutable("/opt/Blender/Official/blender-2.70-linux-glibc211-x86_64/blender")

Benchmark.AddRenderTask("/mnt/iData/Projekte/Grafik/3D/BlenderTests/LEGO/StoneCollection.blend")
Benchmark.AddRenderTask("/mnt/iData/Projekte/Grafik/3D/BlenderTests/Cycles/Christmas.blend")

# Render
Benchmark.Render()

# RenderTask -> Blender Projekt-Datei
  # task = Benchmark.AddRenderTask(Blendfile [Frame, Length])
  # Benchmark.RemoveRenderTask(Blendfile)
  # Benchmark.ReRender() # Rendert alle Dateien, egal ob bereits gerendert wurde
  # Benchmark.Render() # Rendert nur die Dateien die noch nicht gerendert wurden

# RenderTarget -> Blenderversion
  # target = AddRenderTarget(Path) ## fügt neue Blenderversion in Provider ein,
  #  Provider muss dabei alle Informationen über Blender herausfinden. Falls bereits selbe Version an anderem Ort existiert
