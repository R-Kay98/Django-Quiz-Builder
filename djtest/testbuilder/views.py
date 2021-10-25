from django.shortcuts import render
from django.http import HttpResponse

posts = [

	{
	
		'author': 'hello',
		'title': 'yes'
	
	},
	{
	
		'author': 'bye',
		'title': 'no'
	
	}

]

def home(request):
	
	context = {
		'posts': posts
	}
	
	return render(request, 'testbuilder/home.html', context)
