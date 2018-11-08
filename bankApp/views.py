from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView
from django.core import serializers
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Banks, Branches


def index(request):
    return render(request, 'index.html', {})


def autocomplete(request):
    search_term = request.GET.get('query', None)

    banks = Banks.objects.all()
    if search_term:
        banks = banks.filter(name__istartswith=search_term)

    response = serializers.serialize("json", banks[:6])
    return HttpResponse(response, content_type='application/json')


def cityautocomplete(request):
    search_term = request.GET.get('query', None)

    city = Branches.objects.distinct('city')
    if search_term:
        city = city.filter(city__istartswith=search_term)

    response = serializers.serialize("json", city[:6])
    return HttpResponse(response, content_type='application/json')


class IfscView(DetailView):

    model = Branches
    template_name = 'ifsc.html' 

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        ifsc = self.kwargs.get('ifsc')
        if ifsc:
            queryset = queryset.filter(pk=ifsc.upper())
        else:
            obj = {}
            obj['object'] = None
            obj['error'] ='Enter IFSC to get details'
            return obj

        try:
            obj = queryset.get()
        except:
            obj = {}
            obj['object'] = None
            obj['error'] ='Entered IFSC does not exist.'
            return obj
        
        return obj


class BranchesListView(ListView):

    template_name = 'branches.html'
    model = Branches
    context_object_name = 'branches'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(BranchesListView, self).get_context_data(**kwargs) 
        bank_id = self.kwargs.get('bank_id', None)
        city = self.kwargs.get('city', None)

        if not bank_id:
            context['branches'] = []
            context['error'] ='Choose a bank'
            return context

        try:
            bank = Banks.objects.get(id=bank_id)
        except:
            context['branches'] = []
            context['error'] ='Chosen bank does not exist.'
            return context

        context['bank'] = bank
        context['city'] = city
        branches_list = Branches.objects.filter(bank=bank).order_by('state')

        if city:
            branches_list = branches_list.filter(city=city).order_by('ifsc')
        paginator = Paginator(branches_list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            branches = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            branches = paginator.page(1)
        except EmptyPage:
            page = paginator.num_pages
            branches = paginator.page(paginator.num_pages)
        context['branches'] = branches
        context['total_pages'] = paginator.num_pages
        context['has_next'] = paginator.num_pages > int(page)
        context['has_previous'] = 1 < int(page)
        context['page'] = int(page)
        return context            
