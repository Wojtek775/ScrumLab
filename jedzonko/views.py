from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views import View
from random import shuffle

from jedzonko.models import Recipe, Schedule, DayName, RecipePlan


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


def main(request):
    schedule_count = Schedule.objects.count()
    count = Recipe.objects.count()
    plan = Schedule.objects.order_by('-pk').first()
    if plan is not None:
        recipe_plan = RecipePlan.objects.filter(plan_id=plan.id).order_by('day_name_id')
        days = {}
        for rec_plan in recipe_plan:
            day_name = rec_plan.day_name
            if day_name not in days:
                days[day_name] = [rec_plan]
            else:
                days[day_name].append(rec_plan)
        return render(request, 'dashboard.html',
                      {'count_recipes': count, 'last_plan': plan, 'count_plan': schedule_count,
                       'days': days})
    else:
        return render(request, 'dashboard.html',
                      {'count_recipes': count, 'last_plan': 'Brak planów żywieniowych', 'count_plan': schedule_count})


def index(request):
    recipe = list(Recipe.objects.all())
    if len(recipe) >= 3:
        shuffle(recipe)
        return render(request, 'index.html', {'recipes': recipe[0], "recipes2": recipe[1], "recipes3": recipe[2]})
    else:
        return render(request, 'index.html')


def recipes(request):
    recipes = Recipe.objects.all().order_by('-votes', 'created')
    paginator = Paginator(recipes, 50)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if request.method == 'GET':
        return render(request, 'app-recipes.html', {"recipes": page, 'all': recipes})
    elif request.method == 'POST':
        recipe_id = request.POST['name']
        recipe_to_del = Recipe.objects.get(pk=recipe_id)
        recipe_to_del.delete()
        return render(request, 'app-recipes.html', {"recipes": page})


class Landing_page(View):
    def get(self, request):
        return render(request, '__base__.html')


class Schedule_list_view(View):
    def get(self, request):
        ordered_schedules = Schedule.objects.all().order_by('name')
        paginator = Paginator(ordered_schedules, 50)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request, 'app-schedules.html', {'ord_schedules': page})

    def post(self, request):
        plan_id = request.POST['plan_name']
        plan_to_del = Schedule.objects.get(pk=plan_id)
        plan_to_del.delete()
        return redirect('/plan/list/')


class Add_recipe_view(View):
    def get(self, request):
        return render(request, 'app-add-recipe.html')

    def post(self, request):

        name = request.POST.get("name")
        description = request.POST.get("description")
        preparation_time = request.POST.get("preparation_time")
        ingredients = request.POST.get("ingredients")
        directions = request.POST.get("directions")
        if not name:
            return render(request, "app-add-recipe.html", context={"error": "Wypełnij poprawnie wszystkie pola"})
        elif not description:
            return render(request, "app-add-recipe.html", context={"error": "Wypełnij poprawnie wszystkie pola"})
        elif not preparation_time:
            return render(request, "app-add-recipe.html", context={"error": "Wypełnij poprawnie wszystkie pola"})
        elif not ingredients:
            return render(request, "app-add-recipe.html", context={"error": "Wypełnij poprawnie wszystkie pola"})
        elif not directions:
            return render(request, "app-add-recipe.html", context={"error": "Wypełnij poprawnie wszystkie pola"})
        a = Recipe(name=name, description=description, preparation_time=preparation_time, ingredients=ingredients,
                   directions=directions)
        a.save()

        return redirect(f'/recipes/list/')


class Add_schedule_view(View):
    def get(self, request):
        return render(request, 'app-add-schedules.html')

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        new_plan = Schedule(name=name, description=description)
        new_plan.save()
        return redirect(f'/plan/{new_plan.id}/details/')


class Recipe_to_plan_view(View):
    def get(self, request):
        plans = Schedule.objects.all()
        recipes = Recipe.objects.all()
        days = DayName.objects.all()
        return render(request, 'app-schedules-meal-recipe.html', {
            'plans': plans,
            'recipes': recipes,
            'days': days})

    def post(self, request):
        try:
            selected_plan = Schedule.objects.get(name=request.POST.get('selected_plan'))
            meal_name = request.POST.get('meal_name')
            order = request.POST.get('order')
            recipe = Recipe.objects.get(name=request.POST.get('recipe'))
            day_name = DayName.objects.get(name=request.POST.get('day_name'))
            s = RecipePlan(meal_name=meal_name, recipe=recipe, plan=selected_plan, order=order, day_name=day_name)
            s.save()
            return redirect(f'/plan/{selected_plan.id}/details/')
        except IntegrityError as e:
            return render(request, 'app-schedules-meal-recipe.html', {'alert': e})


class Recipe_details_view(View):
    def get(self, request, id):
        recipe_id = Recipe.objects.get(pk=id)
        return render(request, 'app-recipe-details.html', {'recipe': recipe_id})

    def post(self, request, id):
        recipe = Recipe.objects.get(pk=id)
        like = request.POST.get('like')
        if like == "vote":
            recipe.votes += 1
            recipe.save()
        if like == "unvote":
            recipe.votes -= 1
            recipe.save()
        return redirect(f'/recipe/{id}/')


class Recipe_edit_view(View):
    def get(self, request, id):
        recipe_id = get_object_or_404(Recipe, pk=id)
        return render(request, 'app-edit-recipe.html', {'recipe': recipe_id})

    def post(self, request, id):
        recipe_id = get_object_or_404(Recipe, pk=id)
        recipe_id.name = request.POST['name']
        recipe_id.description = request.POST['description']
        recipe_id.preparation_time = request.POST['prep_time']
        recipe_id.ingredients = request.POST['ingredients']
        recipe_id.directions = request.POST['directions']
        recipe_id.save()
        return redirect('/recipes/list/')


class Schedule_details_view(View):
    def get(self, request, id):
        plan_id = Schedule.objects.get(pk=id)
        recipe_plan = RecipePlan.objects.filter(plan_id=plan_id.id).order_by('day_name_id')
        days = {}
        for rec_plan in recipe_plan:
            day_name = rec_plan.day_name
            if day_name not in days:
                days[day_name] = [rec_plan]
            else:
                days[day_name].append(rec_plan)
        return render(request, 'app-details-schedules.html', {
            'schedule': plan_id,
            'recipe_plan': recipe_plan,
            'days': days})

    def post(self, request, id):
        recipe = int(request.POST['recipe_id'])
        day = int(request.POST['day_id'])
        order = request.POST['order']
        recipe_to_delete = RecipePlan.objects.get(recipe_id=recipe, day_name_id=day, order=order)
        recipe_to_delete.delete()
        return redirect(f'/plan/{id}/details/')


class Schedule_modify_view(View):
    def get(self, request, id):
        plan_id = Schedule.objects.get(pk=id)
        return render(request, 'app-edit-schedules.html', {'schedule': plan_id})

    def post(self, request, id):
        plan_to_modify = Schedule.objects.get(pk=id)
        plan_to_modify.name = request.POST['plan_name']
        plan_to_modify.description = request.POST['plan_description']
        plan_to_modify.save()
        return redirect(f'/plan/{id}/details/')


def search(request):
    try:
        response = request.GET['recipes']
        obj_id = Recipe.objects.get(name=response).id
        return redirect(f'/recipe/{obj_id}/')
    except ObjectDoesNotExist as d:
        return render(request, 'app-recipes.html', {'exist': d})

