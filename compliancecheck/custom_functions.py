from netmiko import ConnectHandler
import time
import concurrent.futures
import datetime
import pytz
from compliancecheck.models import ComplianceTemplates, LatestRunningConfiguration

def change_user_form(form):

	username = form.cleaned_data.get('ssh_username')
	password = form.cleaned_data.get('ssh_password')
	device_type = form.cleaned_data.get('device_type')

	ssh_commands_list = ['sh vrf | i grn200|GRN200', 'sh run | in hostname', 'sh ip int bri | in Loopback200|Lo200', 'sh ip int bri vrf all | in Lo200', 'show running-config']

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
		"Result" : {},
		"RunningConfigDict" : {},
		"CompDevices" : []
	}
	return args

class ComplianceCheck:

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
				if eachcommand == 'sh vrf | i grn200|GRN200':
					if ('grn200' or 'GRN200') in output:
						vrfgrnexists = 'Yes'
					else:
						vrfgrnexists = 'No'
				if eachcommand == 'sh run | in hostname':
					hostname = output.split('hostname')[1].strip()
				if eachcommand == 'sh ip int bri | in Loopback200|Lo200':
					if ('Loopback200' or 'Lo200') in output:
						loopback200exists = 'Yes'
					else:
						loopback200exists = 'No'
				if eachcommand == 'sh ip int bri vrf all | in Lo200':
					if 'Lo200' in output:
						lo200exists = 'Yes'
					else:
						lo200exists = 'No'
				if eachcommand == 'show running-config':
					running_config = output

			if (vrfgrnexists == 'Yes' and (loopback200exists == 'Yes' or lo200exists == 'Yes')):
				classifiedtype = 'Grn200Lo200'
			elif (vrfgrnexists == 'Yes' and (loopback200exists == 'No' and lo200exists == 'No')):
				classifiedtype = 'Grn200NoLo200'
			elif (vrfgrnexists == 'No' and (loopback200exists == 'Yes' or lo200exists == 'Yes')):
				classifiedtype = 'NoGrn200Lo200'
			elif (vrfgrnexists == 'No' and (loopback200exists == 'No' and lo200exists == 'No')):
				classifiedtype = 'NoGrn200NoLo200'
			self.OutputDict[device] = '\nDevice Name: '+ hostname +'\ngrn200 exists: ' + vrfgrnexists +'\nLoopback200 exists: ' + loopback200exists +'\nLo200exists exists: ' + lo200exists +'\nType: ' + classifiedtype
			if device not in self.SuccessDevices:
				self.SuccessDevices.append(device)
				self.CompDevices.append(hostname)

			if device not in self.Result:
				self.Result[device] = "Success"

			self.RunningConfigDict = {"Hostname" : hostname, "compliance_type" : classifiedtype, "running_config" : running_config}
			self.storerunningconfig()
			#self.complianceStatusCheck()
			
			
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
			"Result" : list(self.Result.items()),
			"CompDevices" : self.CompDevices
		}
		return args

	def storerunningconfig(self):
		try:
			device_obj = LatestRunningConfiguration.objects.get(Hostname=self.RunningConfigDict['Hostname'])
			if (device_obj.compliance_type == self.RunningConfigDict['compliance_type']) and (device_obj.running_config == self.RunningConfigDict['running_config']):
				pass
			else:
				device_obj.compliance_type = self.RunningConfigDict['compliance_type']
				device_obj.running_config  = self.RunningConfigDict['running_config']
				device_obj.save()
		except LatestRunningConfiguration.DoesNotExist:
			runningconfig_obj = LatestRunningConfiguration(Hostname=self.RunningConfigDict['Hostname'], compliance_type = self.RunningConfigDict['compliance_type'], running_config = self.RunningConfigDict['running_config'])
			runningconfig_obj.save()
		return

	def complianceStatusCheck(self,comphostname):
		#hostname_obj = LatestRunningConfiguration.objects.get(Hostname=self.RunningConfigDict['Hostname'])
		hostname_obj = LatestRunningConfiguration.objects.get(Hostname=comphostname)
		comp_temp_dict = ComplianceTemplates.objects.get(template_name='Default Template').__dict__

		comp_temp_dict.pop("_state")
		comp_temp_dict.pop("id")
		comp_temp_dict.pop("template_name")
		for section in comp_temp_dict:
		  comp_temp_dict[section] = comp_temp_dict[section].splitlines()

		ComplainceStats = {}
		MissingCmds = {}
		AllSectionDict = {}
		AllSectionDict['TotalCmds'] = 0
		AllSectionDict['PresentCmds'] = 0
		AllSectionDict['AbsentCmds'] = 0
		for eachsection, sectioncommandlist in comp_temp_dict.items():
		    TotalCmdsPerSec = 0
		    PresentCmdsPerSec = 0
		    AbsentCmdsPerSec = 0
		    MissingCmdsPerSec = []
		    SectionDict = {}
		    for eachcommand in sectioncommandlist:
		      TotalCmdsPerSec += 1
		      if eachcommand in hostname_obj.running_config:
		        PresentCmdsPerSec += 1
		      else:
		        AbsentCmdsPerSec += 1
		        MissingCmdsPerSec.append(eachcommand)
		    SectionDict['TotalCmdsPerSec']   = TotalCmdsPerSec
		    SectionDict['PresentCmdsPerSec'] = PresentCmdsPerSec
		    SectionDict['AbsentCmdsPerSec'] = AbsentCmdsPerSec
		    AllSectionDict['TotalCmds'] += TotalCmdsPerSec
		    AllSectionDict['PresentCmds'] += PresentCmdsPerSec
		    AllSectionDict['AbsentCmds'] += AbsentCmdsPerSec
		    ComplainceStats[eachsection] = SectionDict
		    MissingCmds[eachsection] = MissingCmdsPerSec

		args = {
		"ComplainceStats" : ComplainceStats,
		"MissingCmds" : MissingCmds,
		"AllSectionDict" : AllSectionDict
		}
		return args