from rango.forms import CategoryForm
from typing import ContextManager
from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from django.shortcuts import redirect


from django.http import HttpResponse

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list=Page.objects.order_by('-views')[:5]
   # return HttpResponse("Rango says hey there partner!<a href='/rango/about/'>About</a>")
   # Construct a dictionary to pass to the template engine as its context
   # Note the key boldmessage matches to {{ boldmessage }} in the template

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list
    #context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
   
   # Return a rendered response to send to the client. 
   # We make use of the shortcut function to make our lives easier
   # Note that the first parameter is the template we wish to use
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    
    return render(request, 'rango/category.html', context=context_dict)

def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print(form.errors)
    
    return render(request, 'rango/add_category.html', {'form': form})

    


   