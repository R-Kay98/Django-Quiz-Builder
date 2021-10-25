from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import IntegrityError
from django.views.generic import ListView
from .forms import UserRegisterForm
from .testTaker import student
from testbuilder.models import Quiz, Profiles, Question, Choice, ShortAnswer

func = lambda x: True if x == 'on' else False

def register(request):

	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			occupation = form.cleaned_data.get('occupation')
			user = User.objects.get(username=username)
			profile = Profiles(user=user, occupation=occupation)
			profile.save()
			messages.success(request, f'Account created for {username}!')
			return redirect('login')
	else:
		form = UserRegisterForm()
		
	return render(request, 'users/register.html', {'form': form})

@login_required(login_url='/login/')
def profile(request):
	
	occupation = Profiles.objects.get(user__username=request.user.username).occupation
	
	if occupation == 0: #student login
		return render(request, 'users/student.html', {'Quizzes': Quiz.objects.all()})
	elif occupation == 1: #teacher login
		return render(request, 'users/teacher.html', {'Quizzes': Quiz.objects.all()}) 
	return render(request, 'users/logout.html')
	
@login_required(login_url='/login/')
def choose_question(request):
	
	data = request.POST.get("passfield")
	
	if (data == ''):
		return redirect('profile')
		
	if (data == None):
		data = request.session['test']
	
	try:
		Quiz(
		title = request.POST.get("textfield"),
		question_count = 0,
		passcode = request.POST.get("passfield"),
		author = Profiles.objects.get(user__username=request.user.username).user
		).save()
	except IntegrityError as e:
		pass
		
	return render(request, 'users/choosequestion.html', {'passfield': data, 'Questions': Question.objects.filter(quiz__passcode=data)})

@login_required(login_url='/login/')
def new_mc_question(request, parameter):
	return render(request, 'users/multiplechoice.html', {'passfield': parameter})

@login_required(login_url='/login/')	
def mc_complete(request):
	
	if request.POST.get("Question") == None or request.POST.get("Question") == '':
		request.session['test'] = request.POST.get("passfield")
		return redirect('choose_question')
	
	try:
		Question(
		question = request.POST.get("Question"),
		quiz = Quiz.objects.get(passcode=request.POST.get("passfield"))
		).save()
		
		Choice(
		question = Question.objects.get(question=request.POST.get("Question")),
		choice = request.POST.get("A"),
		isCorrect = func(request.POST.get("answer_A"))
		).save()
		
		Choice(
		question = Question.objects.get(question=request.POST.get("Question")),
		choice = request.POST.get("B"),
		isCorrect = func(request.POST.get("answer_B"))
		).save()
		
		Choice(
		question = Question.objects.get(question=request.POST.get("Question")),
		choice = request.POST.get("C"),
		isCorrect = func(request.POST.get("answer_C"))
		).save()
		
		Choice(
		question = Question.objects.get(question=request.POST.get("Question")),
		choice = request.POST.get("D"),
		isCorrect = func(request.POST.get("answer_D"))
		).save()
		
	except IntegrityError as e:
		print(e)
	
	request.session['test'] = request.POST.get("passfield")
	return redirect('choose_question')

@login_required(login_url='/login/')
def new_sa_question(request, parameter):
	return render(request, 'users/shortanswer.html', {'passfield': parameter})
	
login_required(login_url='/login/')	
def sa_complete(request):
	
	if request.POST.get("Question") == None or request.POST.get("Question") == '':
		request.session['test'] = request.POST.get("passfield")
		return redirect('choose_question')
	
	try:
		Question(
		question = request.POST.get("Question"),
		quiz = Quiz.objects.get(passcode=request.POST.get("passfield"))
		).save()
		
		ShortAnswer(
		question = Question.objects.get(question=request.POST.get("Question")),
		answer = request.POST.get("Answer")
		).save()
		
	except IntegrityError as e:
		pass
	
	request.session['test'] = request.POST.get("passfield")
	return redirect('choose_question')
	
@login_required(login_url='/login/')
def delete_quiz(request, parameter):
	Quiz.objects.get(passcode=parameter).delete()
	return redirect('profile')
	
@login_required(login_url='/login/')
def delete_question(request, parameter):
	Question.objects.get(question=parameter).delete()
	return redirect('choose_question')
	
@login_required(login_url='/login/')
def start_quiz(request):
	
	count = 0
	QID = None
	qNum = None
	numCorrect = None
	retQuestion = None
	retChoices = []
	retTruths = [] #For multiple choice
	retAnswer = [] #For short answer
	
	if request.GET.get('QID') != None: #Came from student.html
		QID = request.GET.get('QID')
		qNum = 0
		numCorrect = 0
	else:
		print(type(request.POST.get('Choice')))
		print(request.POST.get('Answer'))
		QID = request.session.get('student')['QID']
		qNum = request.session.get('student')['qNum'] + 1
		numCorrect = request.session.get('student')['numCorrect']
		if (request.POST.get('Answer') == request.session.get('student')['retAnswer']) or request.POST.get('Choice') == 'True':
			numCorrect = numCorrect + 1
	
	quiz = Quiz.objects.get(passcode=QID)
	questions = Question.objects.filter(quiz=Quiz.objects.get(passcode=QID))
	
	for question in questions:
		if count == qNum:
			retQuestion = question.question
			choices = Choice.objects.filter(question=question.question)
			shortanswers = ShortAnswer.objects.filter(question=question.question)
			
			for choice in choices:
				retChoices.append(choice.choice)
				retTruths.append(choice.isCorrect)
			for sa in shortanswers:
				retAnswer = sa.answer
		count = count + 1
	
	if len(retChoices) > 0: #Multiple choice question
		format = 'MC'
	elif len(retAnswer) > 0: #Short answer question
		format = 'SA'
	else: #Either end of questions or no questions available
		format = 'NA'
		#return redirect('profile')
	
	request.session['student'] = {
		'QID': QID,
		'retQuestion': retQuestion,
		'qNum': qNum,
		'numCorrect': numCorrect,
		'retChoices': retChoices,
		'retTruths': retTruths, #Multiple choice t or f values
		'retAnswer': retAnswer, #Short answer value
		'format': format
	}
	
	return render(request, 'users/quizquestion.html')
	