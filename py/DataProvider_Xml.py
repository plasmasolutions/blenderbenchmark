from DataProvider import *
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
import sys, ResultSet

class XmlDataProviderClass(DataProviderClass):
	"""Writes and reads test results"""
	def __init__(self, PathAndFilename):
		self.PathAndFilename = PathAndFilename
		self._resultSets = [] # This will hold all results read from the existing file into memory
		self.ReadFromXml(PathAndFilename)
		
	def Initialize(self):
		pass
		
	def AddResultSet(self,NewResultSet):
		hashFound = False
		for existingResultset in self._resultSets:
			print(existingResultset)
			if existingResultset.BuildInformation["hash"] == NewResultSet.BuildInformation["hash"]:
				hashFound = True
				for newResult in NewResultSet.Results:
					md5Found = False
					for existingResult in existingResultset.Results:
						if newResult["md5"] == existingResult["md5"]:
							# TODO this should not be needed -> an existingResult = newResult should do it
							existingResult["filename"] = newResult["filename"]
							existingResult["rendertime"] = newResult["rendertime"]
							existingResult["savetime"] = newResult["savetime"]
							existingResult["md5"] = newResult["md5"]
							md5Found = True
					if not md5Found:
						existingResultset.AddResult(newResult)
							

		#If we didn't found a md5 but we found a hash then we can add the new result
		if not hashFound:
			self._resultSets.append(NewResultSet)
		
	def WriteToXml(self, Filename):
		if Filename == None:
			Filename = self.PathAndFilename
		self._root = ET.Element("benchmark")

		results = ET.Element("results")
		for resultSet in self._resultSets:
			blender = ET.Element("blender")
			blender.set("hash",resultSet.BuildInformation["hash"])
			blender.set("platform",resultSet.BuildInformation["platform"])
			blender.set("release",resultSet.BuildInformation["release"])
			blender.set("builddate",resultSet.BuildInformation["builddate"])
			blender.set("commitdate",resultSet.BuildInformation["commitdate"])
			blender.set("committime",resultSet.BuildInformation["committime"])

			for result in resultSet.Results:
				resultset = ET.Element("resultset")
				filename = ET.Element("filename")
				filename.text = result["filename"]
				md5 = ET.Element("md5")
				md5.text = result["md5"]
				rendertime = ET.Element("rendertime")
				rendertime.text = result["rendertime"]
				savetime = ET.Element("savetime")
				savetime.text = result["savetime"]
				frame = ET.Element("frame")
				frame.text = result["frame"]
				
				blender.append(resultset)
				resultset.append(filename)
				resultset.append(frame)
				resultset.append(md5)
				resultset.append(rendertime)
				resultset.append(savetime)

				results.append(blender)

		self._root.append(results)
		self._indent(self._root)

		tree = ET.ElementTree(self._root)
		tree.write(Filename , xml_declaration=True, encoding='utf-8', method="xml")	

	def _indent(self, elem, level=0):
		"""This will bring the XML file in a proper form ... makes it easier to read it """
		i = "\n" + level*"  "
		if len(elem):
			if not elem.text or not elem.text.strip():
				elem.text = i + "  "
			if not elem.tail or not elem.tail.strip():
				elem.tail = i
			for elem in elem:
				self._indent(elem, level+1)
			if not elem.tail or not elem.tail.strip():
				elem.tail = i
		else:
			if level and (not elem.tail or not elem.tail.strip()):
				elem.tail = i	


	def ReadFromXml(self,Filename):
		""" This method reads a render result xml file and processes all data"""
		try:
			tree = ET.parse(Filename)
			root = tree.getroot()
			root = root.find("results")
			# Get all Blender versions
			for blender in root.findall('blender'):
				resultset = ResultSet.ResultSetClass()
				resultset.BuildInformation['builddate'] = blender.get('builddate')
				resultset.BuildInformation['commitdate'] = blender.get('commitdate')
				resultset.BuildInformation['committime'] = blender.get('committime')
				resultset.BuildInformation['release'] = blender.get('release')
				resultset.BuildInformation['hash'] = blender.get('hash')
				resultset.BuildInformation['platform'] = blender.get('platform')
				# Get all test results that have been rendered with this release
				for result in blender.findall("resultset"):
					entries = {}
					for entry in result:
						entries[entry.tag] = entry.text
					# print(entries)
					# Add them to the Resultset
					resultset.AddResult(entries)
				self.AddResultSet(resultset)
			return True
		except:
			print(sys.exc_info())
			return False
		
