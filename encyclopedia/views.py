from django.shortcuts import render
from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
 })

def view_entry(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return HttpResponse("Title not found.", status=404)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": entry
    })


def search(request):
    query = request.GET.get('q', '')
    entry = util.get_entry(query)
    if entry:
        return render(request, "encyclopedia/entry.html", {
            "title": query,
            "content": entry
        })
    else:
        entries = util.list_entries()
        matching_entries = [entry for entry in entries if query.lower() in entry.lower()]
        
        if not matching_entries:        
            return HttpResponse("No entry found for the given query.", status=404)
        
        return render(request, "encyclopedia/index.html", {
            "entries": matching_entries 
        })
       


    


