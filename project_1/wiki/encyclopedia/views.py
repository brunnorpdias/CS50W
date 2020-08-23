from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render
from . import util
from django import forms
import markdown2


class Search(forms.Form):
    query = forms.CharField(label="Search")


def index(request):
    return render(request, "encyclopedia/index.html", 
        {"entries": util.list_entries(), "form":Search()}
    )

def getpage(request, page):
    if util.get_entry(page) == None:
        return render(request, "encyclopedia/page.html", 
        {"content":"<h1>Error(404): Page not found</h1>", "form":Search()}
        )
    return render(request, "encyclopedia/page.html",
    {"content":markdown2.markdown(util.get_entry(page)), "page":page, "form":Search()}
    )

def search(request):
    query = request.GET.urlencode().split("=")
    searched = []
    for i in query:
        if i is not "query":
            query = i
    for i in util.list_entries():
        if i.lower() == query:
            return getpage(request, query)
        else:
            if i.lower().find(query) is not -1:
                searched.append(i)
    if not searched:
        return getpage(request, query)
    else:
        return render(request, "encyclopedia/search.html",
        {"results":searched}
        )