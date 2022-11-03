from django.contrib import admin
from compliancecheck.models import ComplianceTemplates, LatestRunningConfiguration
from django.db import models
from django.forms import Textarea 


class ComplianceTemplatesAdmin(admin.ModelAdmin):
	formfield_overrides = {
		models.CharField: {'widget': Textarea(attrs={'rows':10, 'cols':50})},
	}
admin.site.register(ComplianceTemplates, ComplianceTemplatesAdmin)

class RunningConfigAdmin(admin.ModelAdmin):
	list_display = ('Hostname', 'downloaded_at')
	formfield_overrides = {
		models.TextField: {'widget': Textarea(attrs={'rows':50, 'cols':100})},
	}
admin.site.register(LatestRunningConfiguration, RunningConfigAdmin)

admin.site.site_header = 'Jagadhish Network Site Administration'
admin.site.site_title = 'Jagadhish Network Site Administration'
admin.site.index_title = 'Jagadhish Network Site Administration'