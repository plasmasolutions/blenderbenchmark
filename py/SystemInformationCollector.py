import platform
import dbus
import LogManager

class SystemInformationCollectorClass(object):
	""" This class holds information about every GPU and CPU in the system.
		If you need some GPU information then use the GPUs array. It holds every value as a dbus dict.
		Use f.e. gpu[0]['pci.vendor'] to get the vendor of the first GPU in your system """

	def __init__(self):
		LogManager.Log.warning("This is atm only tested on Linux machines - as hal/dbus is multiplatform it should work on Mac/Win too though")
		self.GPUs = self.GetGPUsProperties()
		self.SystemInformation = self.GetSystemInformation()

		#for key, value in self.SystemInformation.items():
		#	print(key, value)
	
	# Returns all the GPUs in an associative array. Use f.e. gpu[0]['pci.vendor'] to get the vendor of the first GPU in your system 
	def GetGPUsProperties(self):
		LogManager.Log.warning("Reading system information about GPUs")
		gpus = dict()
		i = 0
		bus = dbus.SystemBus()
		hal_manager_object = bus.get_object('org.freedesktop.Hal', '/org/freedesktop/Hal/Manager')
		prop = 'pci.device_class'
		for device in hal_manager_object.get_dbus_method('GetAllDevices', 'org.freedesktop.Hal.Manager')():
			dev = bus.get_object('org.freedesktop.Hal', device)
			interface = dbus.Interface(dev, dbus_interface='org.freedesktop.Hal.Device')
			if interface.PropertyExists(prop):
				if interface.GetProperty(prop) == 3:
					gpus[i] = interface.GetAllProperties()
					i += 1
		return gpus
	
	#Returns all the CPUs in a dict. Use f.e. Cpu[0]['processor'] to get the vendor of the first GPU in your system
	def GetSystemInformation(self):
		LogManager.Log.warning("Reading system information about CPUs")
		results = dict()
		results['Processor'] = platform.processor()
		results['ProcessorType'] = platform.machine()
		results['OS'] = platform.system()
		results['OSRelease'] = platform.release()
		results['OSVersion'] = platform.version()
		results['OSAlias'] = platform.system_alias(results['OS'], results['OSVersion'], results['OSVersion'])
		return results

# Use this singleton to access all system information.
Sys = SystemInformationCollectorClass()
