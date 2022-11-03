from django.db import models
from django.utils import timezone
from .choices import ComplianceTypeChoices

class ComplianceTemplates(models.Model):
	template_name            = models.CharField(max_length=2000,default='')
	HOSTNAME                 = models.CharField(max_length=2000,default='')
	LOGGING                  = models.CharField(max_length=2000,default='')
	local_credentials        = models.CharField(max_length=2000,default='')
	TACACS                   = models.CharField(max_length=2000,default='')
	STEALTHWATCH_FLOW_RECORD = models.CharField(max_length=2000,default='')
	NETFLOW_TO_STEALTHWATCH  = models.CharField(max_length=2000,default='')
	IPv4_NETFLOW             = models.CharField(max_length=2000,default='')
	MGMT_ACCESS_ACL          = models.CharField(max_length=2000,default='')
	SNMP_RO_ACL              = models.CharField(max_length=2000,default='')
	SNMP_RW_ACL              = models.CharField(max_length=2000,default='')
	SNMP                     = models.CharField(max_length=2000,default='')
	LINE_CON0                = models.CharField(max_length=2000,default='')
	LINE_AUX0                = models.CharField(max_length=2000,default='')
	LINE_VTY0_4              = models.CharField(max_length=2000,default='')
	LINE_VTY5_15             = models.CharField(max_length=2000,default='')
	def __str__(self):
		return f'{self.template_name}'

class LatestRunningConfiguration(models.Model):
	Hostname        = models.CharField(max_length=255,default='')
	compliance_type = models.CharField(
	    max_length=25,
	    choices=ComplianceTypeChoices.TYPE_CHOICES,
	    default=ComplianceTypeChoices.Grn200Lo200,
	)
	running_config  = models.TextField(max_length=100000,default='')
	downloaded_at   = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return f'{self.Hostname}'
#CurrentDateTime = datetime.datetime.now(pytz.timezone('US/Pacific')).strftime("%B %d, %Y %I:%M:%S %p PT")