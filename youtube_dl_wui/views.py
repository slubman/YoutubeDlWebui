
from django.template import Context, RequestContext, Template
from django.shortcuts import render_to_response
from django import forms

class VideoForm(forms.Form):
	url = forms.URLField(label='Video URL')
	email = forms.EmailField(label='Your email')

def home(request):
	if request.method == 'POST':
		form = VideoForm(request.POST)
	else:
		form = VideoForm()
	return render_to_response('index.html', {'video': form}, context_instance=RequestContext(request))
