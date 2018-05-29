from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.views.generic import FormView, CreateView, DetailView
User = get_user_model()

from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm, NewListForm


class  HomePageView(FormView):
    template_name = 'home.html'
    form_class = ItemForm

class NewListView(CreateView):
    template_name = 'home.html'
    form_class = NewListForm

    def form_valid(self, form):
        list_ = form.save(owner=self.request.user)
        return redirect(list_)

class ViewAndAddToList(DetailView, CreateView):
    model = List
    template_name = 'list.html'
    form_class = ExistingListItemForm

    def get_form(self):
        self.object = self.get_object()
        return self.form_class(for_list=self.object, data=self.request.POST)


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(list_)
    return render(request, 'list.html', {'list': list_, 'form': form})

def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})

def share_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    if 'sharee' not in request.POST:
        return redirect(list_)
    email = request.POST['sharee']
    user = User.objects.get(email=email)
    list_.shared_with.add(user)
    return redirect(list_)