from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.template.loader import render_to_string
from . import util
from django.shortcuts import redirect
from markdown2 import Markdown
from django import forms
import random


"""
Forms
    - general form for searching entries
    - form for creating new entries + edit entries
"""
class SearchEntryForm(forms.Form):
    entry_search = forms.CharField(
                                   widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    

class NewEntry(forms.Form):
    title_entry = forms.CharField(max_length=100, label='',
                                   widget=forms.TextInput(attrs={'placeholder': 'Title',
                                                                 'class': 'form-control mb-3',
                                                                 'style': 'width:600px;'
                                                                 }))
    text_entry = forms.CharField(label='',
                                   widget=forms.Textarea(attrs={
                                       'placeholder': 'Text',
                                       'class': 'form-control mb-3',
                                       'style': 'width:600px; height:300px;'
                                       }))
    

# redirect root / to /wiki/
def index(request):
    return redirect('encyclopedia:main_page')


# render main page
def main_page(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchEntryForm()
    })


# validate entries
def page(request, valid_entry):
    """
    Check if the entry (like CSS, HTML etc) exist

    - If exist = convert markdown text to HTML and redirect to corresponding entry
    - If not exist = render error page
    """
    markdowner = Markdown()

    if util.get_entry(valid_entry) != None:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(util.get_entry(valid_entry)),
            "entry_name": valid_entry
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "entry_name": valid_entry
        })



def search(request):
    """
    Searching for the entry from the form on the left side of the page

    - 100% match query == entry, redirect to searched entry
    - Partly match (like ython in Python), list all the entries containing the searched substring
    - No match = redirect to error page and warn user about bad query
    """
    if request.method == "POST":
        form = SearchEntryForm(request.POST)
        entries = util.list_entries()

        # check form validity
        if form.is_valid():

            # store validated value
            search_value = form.cleaned_data["entry_search"]
            
            # 100% match
            if search_value in entries:
                # redirect to wiki/entry_page   # use kwargs!
                return HttpResponseRedirect(reverse("encyclopedia:page", kwargs={"valid_entry": search_value}))
            

            # Partly match
            elif len(util.check_substring(search_value)) > 0:

                finded_values = util.check_substring(search_value)
                return render(request, "encyclopedia/search_find.html", {
                    "entries": finded_values,
                    "entry_name": search_value
                })
                
            # No match
            else:
                return render(request, "encyclopedia/error.html", {
                    "entry_name": search_value
                })

        # Generate empty form (show this before submitting the form)
        else:
            render(request, "encoclopedia/index.html", {
                "form": form
            })


def new(request):
    """
    Create new entry page

    - When clicking on "Create New Page = empty form appears. User can specify title a write markdown text
    - If entry not exist yet = entry can be saved to entries/
    - If entry already exist = render error
    """
    if request.method == "POST":
        form = NewEntry(request.POST)

        # is data valid -> True, not valid ->  False
        if form.is_valid():

            # get values from form
            title = form.cleaned_data["title_entry"]
            text_entry = form.cleaned_data["text_entry"]

            # get list of existing entries
            entry_list = util.list_entries()

            # if entry exist = redirect to error page
            if title in entry_list:
                return render(request, "encyclopedia/error_already_exist.html", {
                    "entry_name": title
                })
            
            # if entry not exist yet = save it to entries/ and redirect to this new entry
            else:
                util.save_entry(title, text_entry)
                return HttpResponseRedirect(reverse("encyclopedia:page", kwargs={"valid_entry": title}))
            
    # Base page = show empty form
    return render(request, "encyclopedia/new_entry.html", {
        "create_entry": NewEntry()
    })


def edit_page(request, valid_entry):
    """
    In entry page, you can click "Edit" button and then be redirected to edit form page
    - Existing entry can be edited 
    - Form should be pre-populated with existing text
    - When editing is done -> redirect to this new edited entry
    """
    # pre-fill the form with values from entries/
    pre_populated = NewEntry(initial={'title_entry': valid_entry,
                                      'text_entry': util.get_entry(valid_entry)})
    
    # Form edited:
    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():

            title = form.cleaned_data["title_entry"]
            text_entry = form.cleaned_data["text_entry"]

            # save edited entry to entries/----.md
            util.save_entry(title, text_entry)
            return HttpResponseRedirect(reverse("encyclopedia:page", kwargs={"valid_entry": title}))    

    # By default render form page with prepopulated form  
    return render(request, "encyclopedia/edit_page.html", {
        "edit_entry": pre_populated
    })


def random_entry(request):
    """
    When clicked on "Random page" you should be redirected to random entry from entry list
    - Random library used
    """
    get_entries = util.list_entries()
    selected_entry = random.choice(get_entries)

    # redirect to random entry
    return HttpResponseRedirect(reverse("encyclopedia:page", kwargs={"valid_entry": selected_entry}))