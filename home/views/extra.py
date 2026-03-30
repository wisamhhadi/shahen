from django.contrib.auth.decorators import user_passes_test, login_required
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from home.forms import *
from core.models import *


# @user_passes_test(lambda user:check_page(user,id=2))
@login_required()
def language_view(request):
    objects = Language.objects.all().order_by('-id')
    form_set = modelformset_factory(Language, form=language_form, extra=18, can_delete=True, can_delete_extra=True)
    form_set2 = form_set(queryset=objects)
    if request.method == "POST":
        formset = form_set(request.POST, queryset=objects)
        if formset.is_valid():
            forms = formset.save(commit=False)
            for object in formset.deleted_objects:
                object.delete()

            for form in forms:
                form.save()
        return redirect('language_view')


    ctx = {
        'forms': form_set2,
    }

    return render(request, "language.html", ctx)

@login_required()
def country_view(request):
    objects = Country.objects.all().order_by('-id')
    form_set = modelformset_factory(Country, form=country_form, extra=18, can_delete=True, can_delete_extra=True)
    form_set2 = form_set(queryset=objects)
    if request.method == "POST":
        formset = form_set(request.POST, queryset=objects)
        if formset.is_valid():
            forms = formset.save(commit=False)
            for object in formset.deleted_objects:
                object.delete()

            for form in forms:
                form.save()
        return redirect('country_view')


    ctx = {
        'forms': form_set2,
    }

    return render(request, "country.html", ctx)

@login_required()
def specialty_view(request):
    objects = Specialty.objects.all().order_by('-id')
    form_set = modelformset_factory(Specialty, form=specialty_form, extra=18, can_delete=True, can_delete_extra=True)
    form_set2 = form_set(queryset=objects)
    if request.method == "POST":
        formset = form_set(request.POST, queryset=objects)
        if formset.is_valid():
            forms = formset.save(commit=False)
            for object in formset.deleted_objects:
                object.delete()

            for form in forms:
                form.save()
        return redirect('specialty_view')


    ctx = {
        'forms': form_set2,
    }

    return render(request, "specialty.html", ctx)

@login_required()
def car_company_view(request):
    objects = CarCompany.objects.all().order_by('-id')
    form_set = modelformset_factory(CarCompany, form=car_company_form, extra=18, can_delete=True, can_delete_extra=True)
    form_set2 = form_set(queryset=objects)
    if request.method == "POST":
        formset = form_set(request.POST, queryset=objects)
        if formset.is_valid():
            forms = formset.save(commit=False)
            for object in formset.deleted_objects:
                object.delete()

            for form in forms:
                form.save()
        return redirect('car_company_view')


    ctx = {
        'forms': form_set2,
    }

    return render(request, "car_company.html", ctx)

@login_required()
def car_model_view(request):
    objects = CarModel.objects.all().order_by('-id')
    form_set = modelformset_factory(CarModel, form=car_model_form, extra=18, can_delete=True, can_delete_extra=True)
    form_set2 = form_set(queryset=objects)
    if request.method == "POST":
        formset = form_set(request.POST, queryset=objects)
        if formset.is_valid():
            forms = formset.save(commit=False)
            for object in formset.deleted_objects:
                object.delete()

            for form in forms:
                form.save()
        return redirect('car_model_view')


    ctx = {
        'forms': form_set2,
    }

    return render(request, "car_model.html", ctx)

@login_required()
def car_color_view(request):
    objects = CarColor.objects.all().order_by('-id')
    form_set = modelformset_factory(CarColor, form=car_color_form, extra=18, can_delete=True, can_delete_extra=True)
    form_set2 = form_set(queryset=objects)
    if request.method == "POST":
        formset = form_set(request.POST, queryset=objects)
        if formset.is_valid():
            forms = formset.save(commit=False)
            for object in formset.deleted_objects:
                object.delete()

            for form in forms:
                form.save()
        return redirect('car_color_view')

    ctx = {
        'forms': form_set2,
    }

    return render(request, "car_color.html", ctx)

@login_required()
def car_category_view(request):
    objects = CarCategory.objects.all().order_by('-id')
    form_set = modelformset_factory(CarCategory, form=car_color_form, extra=18, can_delete=True, can_delete_extra=True)
    form_set2 = form_set(queryset=objects)
    if request.method == "POST":
        formset = form_set(request.POST, queryset=objects)
        if formset.is_valid():
            forms = formset.save(commit=False)
            for object in formset.deleted_objects:
                object.delete()

            for form in forms:
                form.save()

        return redirect('car_category_view')


    ctx = {
        'forms': form_set2,
    }

    return render(request, "car_category.html", ctx)

@login_required()
def goods_type_view(request):
    objects = GoodsType.objects.all().order_by('-id')
    form_set = modelformset_factory(GoodsType, form=goods_type_form, extra=18, can_delete=True, can_delete_extra=True)
    form_set2 = form_set(queryset=objects)
    if request.method == "POST":
        formset = form_set(request.POST, queryset=objects)
        if formset.is_valid():
            forms = formset.save(commit=False)
            for object in formset.deleted_objects:
                object.delete()

            for form in forms:
                form.save()
        return redirect('goods_type_view')


    ctx = {
        'forms': form_set2,
    }

    return render(request, "goods_type.html", ctx)

@login_required()
def car_letter_view(request):
    objects = CarLetter.objects.all().order_by('-id')
    form_set = modelformset_factory(CarLetter, form=car_letter_form, extra=18, can_delete=True, can_delete_extra=True)
    form_set2 = form_set(queryset=objects)
    if request.method == "POST":
        formset = form_set(request.POST, queryset=objects)
        if formset.is_valid():
            forms = formset.save(commit=False)
            for object in formset.deleted_objects:
                object.delete()

            for form in forms:
                form.save()
        return redirect('car_letter_view')


    ctx = {
        'forms': form_set2,
    }

    return render(request, "car_letter.html", ctx)

@login_required()
def car_size_view(request):
    objects = CarSize.objects.all().order_by('-id')
    form_set = modelformset_factory(CarSize, form=car_size_form, extra=18, can_delete=True, can_delete_extra=True)
    form_set2 = form_set(queryset=objects)
    if request.method == "POST":
        formset = form_set(request.POST, queryset=objects)
        if formset.is_valid():
            forms = formset.save(commit=False)
            for object in formset.deleted_objects:
                object.delete()

            for form in forms:
                form.save()
        return redirect('car_size_view')


    ctx = {
        'forms': form_set2,
    }

    return render(request, "car_size.html", ctx)

@login_required()
def activity_type_view(request):
    objects = ActivityType.objects.all().order_by('-id')
    form_set = modelformset_factory(ActivityType, form=activity_type_form, extra=18, can_delete=True, can_delete_extra=True)
    form_set2 = form_set(queryset=objects)
    if request.method == "POST":
        formset = form_set(request.POST, queryset=objects)
        if formset.is_valid():
            forms = formset.save(commit=False)
            for object in formset.deleted_objects:
                object.delete()

            for form in forms:
                form.save()
        return redirect('activity_type_view')

    ctx = {
        'forms': form_set2,
    }

    return render(request, "activity_type.html", ctx)


@login_required()
def banner_view(request):
    objects = Banner.objects.all().order_by('-id')
    form_set = modelformset_factory(Banner, form=banner_form, extra=18, can_delete=True, can_delete_extra=True)
    form_set2 = form_set(queryset=objects)
    if request.method == "POST":
        formset = form_set(request.POST, queryset=objects)
        if formset.is_valid():
            forms = formset.save(commit=False)
            for object in formset.deleted_objects:
                object.delete()

            for form in forms:
                form.save()
        return redirect('banner_view')


    ctx = {
        'forms': form_set2,
    }

    return render(request, "banner.html", ctx)

@login_required()
def blog_view(request):
    objects = Blog.objects.all().order_by('-id')
    form_set = modelformset_factory(Blog, form=blog_form, extra=18, can_delete=True, can_delete_extra=True)
    form_set2 = form_set(queryset=objects)
    if request.method == "POST":
        formset = form_set(request.POST, queryset=objects)
        if formset.is_valid():
            forms = formset.save(commit=False)
            for object in formset.deleted_objects:
                object.delete()

            for form in forms:
                form.save()
        return redirect('blog_view')


    ctx = {
        'forms': form_set2,
    }

    return render(request, "blog.html", ctx)