from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from index.models import *

# Create your views here.
def home(request):
	tag = getTag(request.get_full_path())
	if(tag):
		link = getLink(tag)
		if(not link):
			raise Http404
		return redirect(link)
	if request.method == 'POST':
		ans = addLink(request.POST.get("url", "0"))
		if(ans):
			return HttpResponse(ans)
	return render(request, 'index/index.html')