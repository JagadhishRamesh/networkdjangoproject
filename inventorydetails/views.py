from django.shortcuts import render, redirect
from inventorydetails.forms import SSHBaseForm
from inventorydetails.custom_functions import InventoryDetails, change_user_form

def inventory(request):
	if request.method == 'POST':
		form = SSHBaseForm(request.POST)
		if form.is_valid():
			user_input_args = change_user_form(form)
			userinput = InventoryDetails(**user_input_args)
			outputargs = userinput.execute_priv()
			request.session['outputargs'] = outputargs
			return redirect("ssh-summary")
	else:
		form = SSHBaseForm()
	return render(request, 'inventorydetails/inventory.html', {'form': form})
