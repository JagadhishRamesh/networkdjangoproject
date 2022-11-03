from django.shortcuts import render, redirect
from compliancecheck.forms import SSHBaseForm
from compliancecheck.custom_functions import ComplianceCheck, change_user_form

def compliancehome(request):
	if request.method == 'POST':
		form = SSHBaseForm(request.POST)
		if form.is_valid():
			user_input_args = change_user_form(form)
			userinput = ComplianceCheck(**user_input_args)
			outputargs = userinput.execute_priv()
			request.session['outputargs'] = outputargs
			return redirect("compliance-status")
			#return redirect("compliance-check-summary")
	else:
		form = SSHBaseForm()
	return render(request, 'compliancecheck/compliance_home.html', {'form': form})

def compliancestatus(request):
	if 'outputargs' in request.session:
		context = request.session['outputargs']
		context["overallstats"] = {}
		Comp_Obj = ComplianceCheck()
		for device in request.session['outputargs']['CompDevices']:
			statuscheck = Comp_Obj.complianceStatusCheck(device)
			context["overallstats"][device] = statuscheck
		context["overallstats"] = list(context["overallstats"].items())
		print(context)
	else:
		context = {}
	return render(request, 'compliancecheck/compliance_status.html', context)


def compliancesummary(request):
	if 'outputargs' in request.session:
		context = request.session['outputargs']
	else:
		context = {}
	return render(request, 'compliancecheck/compliance_summary.html', context)

def compliancelogs(request):
	if 'outputargs' in request.session:
		context = { 'OutputDict' : request.session['outputargs']['OutputDict'] }
	else:
		context = {}
	return render(request, 'compliancecheck/compliance_logs.html', context)
