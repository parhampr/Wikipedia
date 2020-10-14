from django.shortcuts import render
import markdown2, random
from . import util
from django.http import HttpResponseRedirect
from django import forms
from django.contrib import messages 

class NewPage(forms.Form):
    title = forms.CharField(max_length=30)
    content = forms.CharField(widget=forms.Textarea(attrs={"placeholder":'Type your MarkDown Content Here'}))
    ty = forms.BooleanField(initial=True, widget=forms.HiddenInput(), required=False)
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search":''
    })

def WikiPage(request, name):
    if name not in util.list_entries():
      return render(request,"encyclopedia/PageNotFound.html")
    return render(request, "encyclopedia/page.html",{
        "title":name.capitalize(),
        "page" : markdown2.markdown(util.get_entry(name))
    })

def random_page(request):
    selected = random.choice(util.list_entries())
    return HttpResponseRedirect(f"/wiki/{selected}")

def newpage(request):
    if request.method == "POST": 
        form = NewPage(request.POST)
        if form.is_valid():
            title = (form.cleaned_data["title"]).strip()
            content = (form.cleaned_data["content"]).strip()
            print(form.cleaned_data["ty"])
            if  (form.cleaned_data["ty"]) and (title in util.list_entries()) :
                return render(request, "encyclopedia/newpage.html", {
                    "form":form,
                    "valid":False,
                    "message":'Provided Page Title Already Exists'
                })
            else:
                util.save_entry(title,content)
                return HttpResponseRedirect(f"/wiki/{title}")

    return render(request, "encyclopedia/newpage.html",{
        "form": NewPage(),
        "valid":True
        })

def edit_page(request,name):
    entryPage = util.get_entry(name)
    Nform = NewPage()
    Nform.fields["title"].initial = name   
    Nform.fields["content"].initial = entryPage.strip()
    Nform.fields["ty"].initial = False
    return render(request, "encyclopedia/newpage.html",{
        "form": Nform,
        "valid":True,
        "name":name
    })

def search(request):
    entries = util.list_entries()
    value = (request.GET.get('q',''))
    if value in entries:
        return HttpResponseRedirect(f"/wiki/{value}")
    new_entries = []
    value = value.strip().lower()
    for entry in entries:
        if value in entry.lower():
            new_entries.append(entry)
    if not new_entries:
        new_entries.append("No Results Found")
    return render(request, "encyclopedia/index.html",{
        "entries":new_entries,
        "search":value
    })
    


