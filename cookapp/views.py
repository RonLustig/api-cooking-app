import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from django.http import JsonResponse
from django.views import View
from django.db.models import Q, Count

from .models import Ingredient, Recipe, UserPreference
from .forms import CreateUserForm
from .decorators import unauthenticated_user

def index(request):
    # Get the most common ingredients
    # works by counting the number of recipes that use each ingredient and ordering by that count
    # annotate adds a new field to each ingredient object with the count
    common_ingredients = Ingredient.objects.annotate(recipe_count=Count('recipe')).order_by('-recipe_count')[:10]

    context = {
        'common_ingredients': common_ingredients,
    }
    return render(request, 'cookapp/index.html', context)

def logout_message(request):
    return render(request, 'registration/logout.html')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            user.save()

            messages.success(request, f'Welcome, {username}!')
            print(f'Messages: {messages.get_messages(request)}')  # Debugging line
            return redirect('index')  # Redirect to the home page
    context = {'form': form}
    return render(request, 'registration/register.html', context)


class RecipeSearch(View):
    def get(self, request):
        query = request.GET.get('term', '').strip()
        blacklist_query = request.GET.get('blacklist', '[]')
        whitelist_query = request.GET.get('whitelist', '[]')
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 10))

        try:
            blacklist = json.loads(blacklist_query)
            whitelist = json.loads(whitelist_query)
        except json.JSONDecodeError:
            blacklist = []
            whitelist = []

        # Initialize the query
        if query:
            recipe_results = Recipe.objects.filter(Q(title__icontains=query) | Q(tags__icontains=query))
        else:
            recipe_results = Recipe.objects.all()

        # Apply whitelist filter (include only recipes with all specified whitelist ingredients)
        if whitelist:
            for ingredient in whitelist:
                try:
                    whitelisted_ingredient = Ingredient.objects.get(name__iexact=ingredient)
                    recipe_results = recipe_results.filter(ingredients=whitelisted_ingredient)
                except Ingredient.DoesNotExist:
                    # If any ingredient in the whitelist is not found, no recipes can match
                    return JsonResponse({
                        'recipes': [],
                    })

        # Apply blacklist filter
        for ingredient in blacklist:
            try:
                blacklisted_ingredient = Ingredient.objects.get(name__iexact=ingredient)
                recipe_results = recipe_results.exclude(ingredients=blacklisted_ingredient)
            except Ingredient.DoesNotExist:
                continue

        # Paginate the results
        recipe_list = list(recipe_results.distinct().values('title', 'id')[offset:offset + limit])

        return JsonResponse({
            'recipes': recipe_list,
        })



@method_decorator(login_required, name='dispatch')
class SavePreferences(View):
    def post(self, request):
        data = json.loads(request.body)
        whitelist = data.get('whitelist', [])
        blacklist = data.get('blacklist', [])
        
        user_preference, created = UserPreference.objects.get_or_create(user=request.user)
        
        # Update whitelist
        user_preference.whitelist.clear()
        for ingredient_name in whitelist:
            ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)
            user_preference.whitelist.add(ingredient)
        
        # Update blacklist
        user_preference.blacklist.clear()
        for ingredient_name in blacklist:
            ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)
            user_preference.blacklist.add(ingredient)
        
        return JsonResponse({'status': 'success'})

class GetPreferences(View):
    def get(self, request):
        if request.user.is_authenticated:
            user_preference, created = UserPreference.objects.get_or_create(user=request.user)
            whitelist = list(user_preference.whitelist.values_list('name', flat=True))
            blacklist = list(user_preference.blacklist.values_list('name', flat=True))
            return JsonResponse({'whitelist': whitelist, 'blacklist': blacklist})
        return JsonResponse({'whitelist': [], 'blacklist': []})


class RecipeDetailView(View):
    def get(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        context = {
            'recipe': recipe
        }
        return render(request, 'cookapp/recipe_detail.html', context)

class MealPlanView(View):
    def get(self, request):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        meals = ["Breakfast", "Lunch", "Snack", "Dinner"]
        context = {
            'days': days,
            'meals': meals,
        }
        return render(request, 'cookapp/mealPlanner.html', context)