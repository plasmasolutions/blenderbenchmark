import logging
import logging.handlers

"""	This class initializes and generates all needed loggers (a system and a file logger)
	After instantiation the normal log commands apply f.e.:	LogManager.Logger.info("Message")
"""
class LogManagerClass(object):
	def __init__(self):
		#self.InfoLogger = logging.getLogger('InfoLogger')
		#self.InfoLogger.setLevel(logging.INFO)
		self.Logger = logging.getLogger('DebugLogger')
		self.Logger.setLevel(logging.DEBUG)
		
		# create a current and a rotating file handler
		currentFileHandler = logging.FileHandler('Benchmark.log','w')
		currentFileHandler.setLevel(logging.INFO)
		continousFileHandler = logging.handlers.RotatingFileHandler('BenchmarkContinous.log','a',1024*1024)
		continousFileHandler.setLevel(logging.DEBUG)

		# create a logging format  -|- %(name)s
		formatter = logging.Formatter('%(asctime)s | %(levelname)8s | %(funcName)30s:%(lineno)4s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
		currentFileHandler.setFormatter(formatter)
		continousFileHandler.setFormatter(formatter)

		# add the handlers to the logger
		#self.InfoLogger.addHandler(currentFileHandler)
		self.Logger.addHandler(continousFileHandler)
		self.Logger.addHandler(currentFileHandler)

Log = LogManagerClass().Logger