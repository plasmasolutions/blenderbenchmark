import sqlite3
import os.path
import LogManager

from DataProvider import *

class SqliteDataProviderClass(DataProviderClass):
	def __init__(self):
		self._connection = None
		self._cursor = None
		self._dbName = '../db/Benchmark.sqlite3'
		LogManager.Logger.info("------ Not ready yet ... in development! ------")

	def Initialize(self):
		self._connect()
		if not os.path.isfile(self._dbName):
			self._createTables()

	def GetSystem(self, Cpu, Gpu, Cuda):
		c.execute('SELECT * FROM Systems WHERE Cpu=? AND Gpu=? AND Cuda=?', (Cpu,Gpu,Cuda))
		c.fetchone()
		
	def InsertSystem(self, Cpu, Gpu, Cuda, Name):
		cursor.execute('INSERT INTO Systems(Name, Cpu, Gpu, Cuda) VALUES(?,?,?,?)', (Name, Cpu, Gpu, Cuda))
		self._connection.commit();

		
	def _connect(self, Databasename = self._dbName):
		self._connection = sqlite3.connect(Databasename)
		self._cursor = self._connection.cursor()

	def _createTables(self):
		self._createSystemsTable()
		self._createFilesTable()
		self._createExecutablesTable()
		self._createRenderingsTable()

	def _createSystemsTable(self):
		cur = self._cursor.execute("""CREATE TABLE Systems(
			Id INTEGER NOT NULL PRIMARY KEY,
			Name TEXT,
			Cpu TEXT,
			Gpu TEXT,
			Cuda TEXT
		)
		""")

	def _createFilesTable(self):
		cur = self._cursor.execute("""CREATE TABLE Files(
			Id INTEGER NOT NULL PRIMARY KEY,
			Md5 TEXT UNIQUE,
			Name TEXT
		)
		""")

	def _createExecutablesTable(self):
		cur = self._cursor.execute("""CREATE TABLE Executables(
			Id INTEGER NOT NULL PRIMARY KEY,
			MajorNumber INTEGER,
			MinorNumber INTEGER,
			Hash TEXT UNIQUE,
			Platform TEXT,
			BuildDate DATETIME,
			CommitDate DATETIME,
			Type DATETIME,
			CFlags DATETIME,
			CppFlags DATETIME
		)
		""")

	def _createRenderingsTable(self):
		cur = self._cursor.execute("""CREATE TABLE Renderings(
			Id INTEGER NOT NULL PRIMARY KEY,
			SystemId INTEGER,
			FileId INTEGER,
			ExecutableId INTEGER,
			Rendertime DATETIME,
			Savetime DATETIME,
			Frame INTEGER,
			Framecount INTEGER,
			FOREIGN KEY(SystemId) REFERENCES Systems(Id),
			FOREIGN KEY(FileId) REFERENCES Files(Id),
			FOREIGN KEY(ExecutableId) REFERENCES Executables(Id)
		)
		""")