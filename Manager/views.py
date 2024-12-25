from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from Manager import models
from .models import Account, Expense
from .forms import ExpenseForm
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import ListView
from datetime import datetime  # Fixed typo here
from dateutil.relativedelta import relativedelta
from django.utils.safestring import mark_safe
from django.db.models import Sum, Count, F
import plotly.express as px
from plotly.graph_objs import *

# Create your views here.
# @login_required(login_url='/signin')

def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in
            login(request, user)
            return redirect('home')  
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def generate_graph(data):
    fig = px.bar(data, x='months', y='expenses', title='Monthly Expenses')
    fig.update_layout(
        xaxis=dict(rangeslider=dict(visible=True)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='rgba(0,0,0,1)'
    )
    
    # Fix the color by adding a '#' before the color code
    fig.update_traces(marker_color='#008c41')  # Note the '#' here
    
    graph_json = fig.to_json()
    return graph_json


class ExpenseListView(FormView):
    model = Expense
    template_name = 'expense_list.html'
    form_class = ExpenseForm
    success_url = '/expenses/'  # Update this with the correct URL

    def form_valid(self, form):
        # Retrieve the user's account
        account, _ = Account.objects.get_or_create(user=self.request.user)
        
        # Create a new liability instance and link it to the user's account
        expense = Expense(
            name=form.cleaned_data['name'],
            amount=form.cleaned_data['amount'],
            interest_rate=form.cleaned_data['interest_rate'],
            end_date=form.cleaned_data['end_date'],
            user=self.request.user
        )
        expense.save()
        account.expense_list.add(expense)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Retrieve user's account data and related liabilities
        accounts = Account.objects.filter(user=user)
        expense_data_graph = {}  # Fixed indentation and variable definition
        # Create a dictionary to store expense data grouped by month
        expense_data = {}

        for account in accounts:
            expenses = account.expense_list.all()
            for expense in expenses:
                if expense.long_term and expense.monthly_expenses:  # Fixed the typo here (extra space in `expense.long_term`)
                    current_date = expense.date
                    while current_date <= expense.end_date:
                        year_month = current_date.strftime('%Y-%m')
                        if year_month not in expense_data_graph:
                            expense_data_graph[year_month] = []
                        
                        expense_data_graph[year_month].append({
                            'name': expense.name,
                            'amount': expense.monthly_expenses,
                            'date': expense.date,
                            'end_date': expense.end_date,
                        })
                        
                        current_date = current_date + relativedelta(months=1)  # Fixed typo: `current_datecurrent_date`
                    else:
                        year_month = expense.date.strftime('%Y-%m')
                        if year_month not in expense_data_graph:
                            expense_data_graph[year_month] = []
                        expense_data_graph[year_month].append({
                            'name': expense.name,
                            'amount': expense.amount,
                            'date': expense.date,
                        })

        aggregated_data = [{'year_month': key, 'expenses': sum(item['amount'] for item in value)}
                           for key, value in expense_data_graph.items()]
        
        context['expense_data'] = expense_data
        context['aggregated_data'] = aggregated_data
        graph_data = {
            'months': [item['year_month'] for item in aggregated_data],
            'expenses': [item['expenses'] for item in aggregated_data]
        }
        
        graph_data['chart'] = generate_graph(graph_data)
        context['graph_data'] = mark_safe(graph_data['chart'])  # Fixed typo: 'char' -> 'chart'
        
        return context
