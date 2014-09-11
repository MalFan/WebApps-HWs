from django.shortcuts import render

# Create your views here.
def calculator(request):
	context = {}
	context['num_x'] = '0'
	context['num_y'] = '0'
	context['num_ans'] = '0'
	context['oper'] = '+'
	context['state'] = '0'
	state = "0"
	num_x = 0
	num_y = 0
	num_ans = 0
	oper = "+"

	# first, get those params back 
	if 'num_x' in request.POST:
	    num_x = int(request.POST['num_x'])
	if 'num_y' in request.POST:
	    num_y= int(request.POST['num_y'])
	if 'num_ans' in request.POST:
	    num_ans = int(request.POST['num_ans'])
	if 'oper' in request.POST:
	    oper = request.POST['oper']
	if 'state' in request.POST:
	    state = request.POST['state']

	if 'btn' in request.POST:
	    btn_clicked = request.POST['btn']
	else:
	    btn_clicked = "0"

	# determine btn_clicked_type
	numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
	operators = ["+", "-", "*", "/"]
	if btn_clicked in numbers:
		btn_clicked_type = "number"
		btn_clicked_number = int(btn_clicked)
	elif btn_clicked in operators:
		btn_clicked_type = "operator"
	elif btn_clicked == "=":
		btn_clicked_type = "equal"

	# determine state
	if state == "0": # means entering the first number
		if btn_clicked_type == "number":
			state = "0"
			num_x = num_x * 10 + btn_clicked_number
			num_ans = num_x
		elif btn_clicked_type == "operator":
			state = "1"
			oper = btn_clicked
			num_ans = num_x
		elif btn_clicked_type == "equal":
			state = "3"
			try:
			    	num_ans = eval(str(num_x) + oper + str(num_y))
			except ZeroDivisionError:
			    	state = "4"			

	elif state == "1": # means entering the operator
		if btn_clicked_type == "number":
			state = "2"
			num_y = btn_clicked_number
			num_ans = num_y
		elif btn_clicked_type == "operator":
			state = "1"
			oper = btn_clicked
			num_ans = num_x
		elif btn_clicked_type == "equal":
			state = "3"
			num_y = num_x
			try:
			    	num_ans = eval(str(num_x) + oper + str(num_y))
			except ZeroDivisionError:
			    	state = "4"

	elif state == "2": # means entering the second number
		if btn_clicked_type == "number":
			state = "2"
			num_y = (num_y * 10) + btn_clicked_number
			num_ans = num_y
		elif btn_clicked_type == "operator":
			state = "2"
			try:
			    	num_ans = eval(str(num_x) + oper + str(num_y))
			except ZeroDivisionError:
			    	state = "4"
			if state != "4":
				num_x = num_ans
				oper = btn_clicked
				num_y = 0
		elif btn_clicked_type == "equal":
			state = "3"	
			try:
			    	num_ans = eval(str(num_x) + oper + str(num_y))
			except ZeroDivisionError:
			    	state = "4"
			if state != "4":
				num_x = num_ans

	elif state == "3": # means entering the equal sign
		if btn_clicked_type == "number":
			state = "0"
			num_x = btn_clicked
			num_ans = num_x
		elif btn_clicked_type == "operator":
			state = "1"
			oper = btn_clicked
			num_ans = num_x
		elif btn_clicked_type == "equal":
			state = "3"
			try:
			    	num_ans = eval(str(num_x) + oper + str(num_y))
			except ZeroDivisionError:
			    	state = "4"
			if state != "4":
				num_x = num_ans

	elif state == "4": # means error
		if btn_clicked_type == "number":
			state = "0"
			num_x = btn_clicked
			num_ans = num_x
		elif btn_clicked_type == "operator":
			state = "1"
			num_x = 0
			oper = btn_clicked
			num_ans = num_x
		elif btn_clicked_type == "equal":
			state = "3"
			num_ans = 0
			oper = "+"
			num_x = num_ans

	
	context['num_x'] = str(num_x)
	context['num_y'] = str(num_y)
	if state == "4":
		context['num_ans'] = "Error"
	else:
		context['num_ans'] = str(num_ans)
	context['oper'] = oper
	context['state'] = state

	return render(request, 'calc.html', context)