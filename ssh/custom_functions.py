from netmiko import ConnectHandler
import time
import concurrent.futures
import datetime
import pytz

def change_user_form(form):

	username = form.cleaned_data.get('ssh_username')
	password = form.cleaned_data.get('ssh_password')
	device_type = form.cleaned_data.get('device_type')

	ssh_commands = form.cleaned_data.get('ssh_commands')
	ssh_commands_list = ssh_commands.splitlines()

	devices = form.cleaned_data.get('devices')
	devices_list = devices.splitlines()
	devices_list = ' '.join(devices_list).split()

	args = {
		"username": username , 
		"password" : password , 
		"device_type" : device_type, 
		"ssh_commands_list" : ssh_commands_list, 
		"devices_list" : devices_list, 
		"OutputDict" : {}, 
		"SuccessDevices" : [], 
		"FailureDevices" : [],
		"Result" : {}
	}
	return args

class Config:

	def __init__(self,**kwargs):
		self.__dict__.update(kwargs)

	def sendssh_commands_list(self,device):
		cisco_config = {
	    'device_type': self.device_type,
	    'host':   device,
	    'username': self.username,
	    'password': self.password
		}
		try:
			net_connect = ConnectHandler(**cisco_config)
			output = net_connect.send_config_set(self.ssh_commands_list)
			#net_connect.save_config()
			
			net_connect.disconnect()
			self.OutputDict[device] = output
			self.SuccessDevices.append(device)
			self.Result[device] = "Success"
			
		except Exception as e:
			self.FailureDevices.append(device)
			self.Result[device] = str(e)

	def execute_config(self):
		start = time.perf_counter()
		with concurrent.futures.ThreadPoolExecutor() as executor:
		    executor.map(self.sendssh_commands_list, self.devices_list)

		finish = time.perf_counter()
		CompletionTime = f'Finished in {round(finish-start, 2)} second(s)'
		CurrentDateTime = datetime.datetime.now(pytz.timezone('US/Pacific')).strftime("%B %d, %Y %I:%M:%S %p PT")
		args = {
			"TotalDevicesCount" : len(self.devices_list),
			"SuccessDevicesCount" : len(self.SuccessDevices),
			"FailureDevicesCount" : len(self.FailureDevices),
			"CurrentDateTime" : CurrentDateTime, 
			"CompletionTime" : CompletionTime ,
			"OutputDict" : list(self.OutputDict.items()), 
			"Result" : list(self.Result.items())
			
		}
		return args

class Priv:

	def __init__(self,**kwargs):
		self.__dict__.update(kwargs)

	def user_priv(self,device):
		cisco_config = {
	    'device_type': self.device_type,
	    'host':   device,
	    'username': self.username,
	    'password': self.password
		}
		try:
			net_connect = ConnectHandler(**cisco_config)
			for eachcommand in self.ssh_commands_list:
				output = net_connect.send_command(eachcommand)
				if device not in self.OutputDict:
					self.OutputDict[device] = eachcommand + ':\n' + output + '\n'
				else:
					self.OutputDict[device] = self.OutputDict[device] + '\n\n' + eachcommand + ':\n' + output 
				if device not in self.SuccessDevices:
					self.SuccessDevices.append(device)
				if device not in self.Result:
					self.Result[device] = "Success"
			
			net_connect.disconnect()
			
		except Exception as e:
			self.FailureDevices.append(device)
			self.Result[device] = str(e)

	def execute_priv(self):
		start = time.perf_counter()
		with concurrent.futures.ThreadPoolExecutor() as executor:
		    executor.map(self.user_priv, self.devices_list)

		finish = time.perf_counter()
		CompletionTime = f'Finished in {round(finish-start, 2)} second(s)'
		CurrentDateTime = datetime.datetime.now(pytz.timezone('US/Pacific')).strftime("%B %d, %Y %I:%M:%S %p PT")
		args = {
			"TotalDevicesCount" : len(self.devices_list),
			"SuccessDevicesCount" : len(self.SuccessDevices),
			"FailureDevicesCount" : len(self.FailureDevices),
			"CurrentDateTime" : CurrentDateTime, 
			"CompletionTime" : CompletionTime ,
			"OutputDict" : list(self.OutputDict.items()), 
			"Result" : list(self.Result.items())
			
		}
		return args
