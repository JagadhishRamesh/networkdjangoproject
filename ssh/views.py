from django.shortcuts import render, redirect
from .forms import SSHBaseForm
from .custom_functions import Priv, Config, change_user_form

global outputargs
outputargs = {}

def home(request):
	return render(request, 'ssh/home.html')

def priv(request):
	if request.method == 'POST':
		form = SSHBaseForm(request.POST)
		if form.is_valid():
			user_input_args = change_user_form(form)
			userinput = Priv(**user_input_args)
			outputargs = userinput.execute_priv()
			request.session['outputargs'] = outputargs
			return redirect("ssh-summary")
	else:
		form = SSHBaseForm()
	return render(request, 'ssh/priv.html', {'form': form})

def config(request):
	if request.method == 'POST':
		form = SSHBaseForm(request.POST)
		if form.is_valid():
			user_input_args = change_user_form(form)
			userinput = Config(**user_input_args)
			outputargs = userinput.execute_config()
			request.session['outputargs'] = outputargs
			return redirect("ssh-summary")
	else:
		form = SSHBaseForm()
	return render(request, 'ssh/config.html', {'form': form})

def summary(request):
	if 'outputargs' in request.session:
		context = request.session['outputargs']
	else:
		context = {}
	return render(request, 'ssh/summary.html', context)

def logs(request):
	if 'outputargs' in request.session:
		context = { 'OutputDict' : request.session['outputargs']['OutputDict'] }
	else:
		context = {}
	return render(request, 'ssh/logs.html', context)