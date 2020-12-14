from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

import markdown2
import random2

from . import util, form_class

# All these functions have in common the following: 
# Given a request (ordered by urls.py file) from a template, it returns an HttpResponse. This template calls to urls.py and 
# urls.py calls to one of the functions described below 

# index(request): Main page. Show the list of entries 
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": form_class.EntrySearchForm()
    })

# Given the url, it gets the page the user has selected
def read_page(request, title):
    page = util.get_entry(title)
    if request.method == "GET":
        if page is not None:
            html_page = markdown2.markdown(page)
            return render(request, "encyclopedia/inputs.html", {
                "context": html_page,
                "title": title,
                "form": form_class.EntrySearchForm()
            })
        else:
            return render(request, "encyclopedia/inputs.html", {
                "context": "<h1>Page not found. Try again</h1>",
                "title": title,
                "form": form_class.EntrySearchForm()
            })
    
# Using navegation bar, when it press the button it takes that search form and it shows the results, if the search matches with
# some of the entries, then it redirects to that page. If not, show in an unordered list the results
def search_page(request):
    form = form_class.EntrySearchForm()
    result_list = []
    if request.method == "GET":
        form = form_class.EntrySearchForm(request.GET)
        if form.is_valid():
            for item in util.list_entries():
                existingResults = form.cleaned_data["entry"].casefold() == item.casefold()
                subexistingResults = form.cleaned_data["entry"].casefold() in item.casefold()
                if existingResults:
                    return HttpResponseRedirect(reverse("wiki", kwargs={
                        "title": item
                    }))
                if subexistingResults:
                        result_list.append(item)
            
    context = {
        "form": form,
        "results": result_list
    }
    return render(request, "encyclopedia/search.html", context)

# When the user, select new page. A new form appears to fullfill. If they save it then it saves and it redirects
# to that new page. After selecting "Home", the user will see the new page in the list of entries
def new_page(request):
    if request.method == "GET": # Select new page
        form_new = form_class.EntryForm(request.GET)
        title = form_new["title"]
        content = form_new["textarea"]
        return render(request, "encyclopedia/newpage.html", {
            "title": title,
            "context": content,
            "form": form_class.EntrySearchForm()
        })
    elif request.method == "POST":  # Save the new page
        form_new = form_class.EntryForm(request.POST)
        if form_new.is_valid():
            for it in util.list_entries():
                same_entry = form_new.cleaned_data["title"].casefold() == it.casefold()
                if same_entry:
                    return render(request, "encyclopedia/inputs.html", {
                        "context": "<h3>Page already found in wiki. Add a new one</h3>",
                        "title": it,
                        "form": form_class.EntrySearchForm()
                    })
                else:
                    title = form_new.cleaned_data["title"]
                    content = form_new.cleaned_data["textarea"]
                    util.save_entry(title, content)
                    return HttpResponseRedirect(reverse("wiki", kwargs={
                        "title": title
                    }))

# When an user select Edit from one page it renders to edit template and appear initial markdown values with the existing content of the file
# When an user save those changes it saves and it redirects to the html page that has been changed
def edit_page(request, title):
    if request.method == "GET":
        content = util.get_entry(title)    
        form_edit = form_class.EntryForm(initial={'title':title, 'textarea':content})
        return render(request,  "encyclopedia/edit.html", {
                "title": title,
                "form_edit": form_edit,
                "form": form_class.EntrySearchForm()
            })   
    elif request.method == "POST":
        form_edit = form_class.EntryForm(request.POST)
        if form_edit.is_valid():
            title = form_edit.cleaned_data["title"]
            text = form_edit.cleaned_data["textarea"]
            util.save_entry(title,text)
            return HttpResponseRedirect(reverse("wiki", kwargs={
                "title": title
            }))
        else:
            return render(request,  "encyclopedia/inputs.html", {
                "title": title,
                "context": "<h6>Not valid form</h6>",
                "form": form_class.EntrySearchForm()
            })

# When it selects Random page, one random page of the list of entries is selected and it redirects to that page
def random_page(request):
    random_selected = random2.choice(util.list_entries())
    return HttpResponseRedirect(reverse("wiki", kwargs={
        "title": random_selected
    }))