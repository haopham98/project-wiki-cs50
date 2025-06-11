from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from markdown2 import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
 })

def view_entry(request, title):
    markdowner = Markdown()
    entry = util.get_entry(title)
    if entry is None:
        return HttpResponse("Title not found.", status=404)
    return render(request, "encyclopedia/entry.html", {
        "title": title.capitalize(),
        "content": markdowner.convert(entry)
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
       

def create_entry(request):
    if request.method == "GET":
        return render(request, "encyclopedia/form_entry.html")
    
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        
        title_entries = [entry.lower() for entry in util.list_entries()]
        title = title.strip().title()  # Normalize title
        content = content.strip()
        
        if title.lower() in title_entries: # Check if title already exists
            return render(request, "encyclopedia/form_entry.html", {
                "error": "An entry with this title already exists.",
                "title": title,
                "content": content
            })
        
        elif title and content:
            util.save_entry(title, content)
            # return redirect("view", title=title)
            return render(request, "encyclopedia/form_entry.html", {
                "success": f"{title} Entry created successfully!",
                "title": title
            })
        else:
            return HttpResponse("Title and content cannot be empty.", status=400)
        
    return HttpResponse("Method not allowed.", status=405)
    


