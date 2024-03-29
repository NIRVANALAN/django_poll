from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.urls import reverse
from django.utils import timezone
from django.template import loader
from django.views import generic


# Create your views here.
class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'
	
	def get_queryset(self):
		# return Question.objects.order_by('-pub_date')[:5]
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'


class ResultView(generic.DetailView):
	model = Question
	template_name = 'polls/result.html'


def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	print(latest_question_list[0].question_txt)
	# template = loader.get_template('polls/index.html')
	context = {
		'latest_question_list': latest_question_list
	}
	# output = ','.join([q.question_text for q in latest_question_list])
	# return HttpResponse("Hello, world. You're at the poll index")
	# return HttpResponse(template.render(context, request))
	return render(request, 'polls/index.html', context)


def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	# return HttpResponse("You 're looking at question {}".format(question_id))
	return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
	response = "You are looking at the result of question {}".format(question_id)
	return HttpResponse(response)


def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except(KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': 'You did not select a choice'
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))
