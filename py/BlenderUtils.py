#encoding: UTF-8
import subprocess, os #, urllib2
import LogManager

def GetBlenderVersionInformation(Executable):
	result = []
	for line in RunCommand(Executable + ' -v'):
		result.append(line.decode("utf-8"))
	
	return ParseBuildInformation(result)

def IsBlenderFromGit(Major, Minor):
	return (int(Major)>1) and (int(Minor) > 69)

def ParseBuildInformation(VersionArray):
	buildInformation = {}
	releaseInfo = []

	buildInformation['release'] = VersionArray[0].split()[1]
	releaseInfo = buildInformation['release'].split('.')

	if not IsBlenderFromGit(releaseInfo[0], releaseInfo[1]):
		LogManager.Log.abort("This script is for Blender versions >= 2.70 !")

	buildInformation['builddate'] = VersionArray[1].split()[2]
	buildInformation['commitdate'] = VersionArray[3].split()[3]
	buildInformation['committime'] = VersionArray[4].split()[3]
	buildInformation['hash'] = VersionArray[5].split()[2]
	buildInformation['platform'] = VersionArray[6].split()[2]
	buildInformation['type'] = VersionArray[7].split()[2]
	buildInformation['cflags'] = VersionArray[8]
	buildInformation['cppflags'] = VersionArray[9]
	#print(self.BuildInformation)
	return buildInformation

def RunCommand(CommandAndArgs, SpaceMarker= "<"):
	# As we marked our spaces with our spaceMarker, we need to remove it here again to make the paths clean
	LogManager.Log.info("Running command '" + CommandAndArgs.replace(SpaceMarker,' ') + "'")

	myCommandAndArgs = CommandAndArgs.split()
	for (i, item) in enumerate(myCommandAndArgs):
		myCommandAndArgs[i] = item.replace(SpaceMarker,' ')

	# Execute the command
	p = subprocess.Popen(myCommandAndArgs,
						stdout=subprocess.PIPE,
						stderr=subprocess.STDOUT)
						#cwd=self.ExecutablePath)
						#universal_newlines=True)
	
	return iter(p.stdout.readline, b'')

def DownloadFile(Url):
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
	