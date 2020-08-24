from django.shortcuts import render
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpRequest
from django.http import HttpResponseRedirect
import markdown2
import numpy as np



class Search(forms.Form):
    q = forms.CharField(label="Search")

class NewPage(forms.Form):
    name = forms.CharField(label="Page Name")
    text = forms.CharField(widget=forms.Textarea)

class EditPage(forms.Form):
    name = forms.CharField(label="Page Name")
    text = forms.CharField(widget=forms.Textarea)



def index(request):
    return render(request, "encyclopedia/index.html", 
        {"entries": util.list_entries(), "sform":Search()}
    )

def getpage(request, page):
    if util.get_entry(page) == None:
        return render(request, "encyclopedia/page.html", 
        {"content":"<h1>Error(404): Page not found</h1>", "sform":Search()}
        )
    return render(request, "encyclopedia/page.html",
    {"content":markdown2.markdown(util.get_entry(page)), "page":page, "sform":Search()}
    )

def search(request):
    query = request.GET.get("q", "")
    searched = []
    for i in util.list_entries():
        if i.lower() == query:
            return HttpResponseRedirect(reverse("wiki:wiki")+i)
        else:
            if i.lower().find(query) is not -1:
                searched.append(i)
    if not searched:
        return getpage(request, query)
    else:
        return render(request, "encyclopedia/search.html",
        {"results":searched}
        )

def newpage(request):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            content = form.cleaned_data["text"]
            util.save_entry(name, content)
    return render(request, "encyclopedia/newpage.html",
    {"nform":NewPage()}
    )
    
def random(request):
    size = len(util.list_entries())
    item = np.random.randint(1, size) - 1
    entries = util.list_entries()[:]
    page = entries[item]
    return getpage(request, page)

def edit(request, page):
    return render(request, "encyclopedia/edit.html",
    {"page":page, "eform":EditPage({'name':page, 'text':util.get_entry(page)}), "sform":Search()}
    )

def save(request):
    if request.method == "POST":
        form = EditPage(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            content = form.cleaned_data["text"]
            util.save_entry(name, content)
            return HttpResponseRedirect(reverse("wiki:wiki")+name)
