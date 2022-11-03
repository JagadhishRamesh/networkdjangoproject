class NetmikoSupportedDevices:
	CISCO_IOS='cisco_ios'
	CISCO_NX_OS='cisco_nxos'
	CISCO_ASA='cisco_asa'
	CISCO_IOS_XE='cisco_xe'
	CISCO_IOS_XR='cisco_xr'
	CISCO_SG300='cisco_s300'
	JUNIPER_JUNOS='juniper_junos'
	ARISTA_VEOS='arista_eos'
	HP_PROCURVE='hp_procurve'
	LINUX='linux'
	DEVICETYPES_CHOICES = [
		(CISCO_IOS,'Cisco IOS'),
		(CISCO_NX_OS,'Cisco NX-OS'),
		(CISCO_ASA,'Cisco ASA'),
		(CISCO_IOS_XE,'Cisco IOS-XE'),
		(CISCO_IOS_XR,'Cisco IOS-XR'),
		(CISCO_SG300,'Cisco SG300'),
		(JUNIPER_JUNOS,'Juniper Junos'),
		(ARISTA_VEOS,'Arista vEOS'),
		(HP_PROCURVE,'HP ProCurve'),
		(LINUX,'Linux')
	]