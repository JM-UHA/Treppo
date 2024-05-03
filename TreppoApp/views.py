from django.http import HttpRequest
from django.shortcuts import redirect, render

from TreppoApp import commands, models
from TreppoApp.forms import CategoryForm, ProjectForm
from TreppoApp.forms.card import CardForm, CardFormNoCategory


def not_found(request: HttpRequest, obj: type[object], obj_id: object | None):
    return render(
        request,
        "common/not_found.jinja",
        {"object": obj.__name__, "id": obj_id},
        status=404,
    )

ALL_COMMANDS = commands.ProjectCommandBuilder().create("Create a project").build()

# Create your views here.


def projects(request: HttpRequest):
    projects = models.Project.objects.all()

    return render(
        request, "projects/all.jinja", {"projects": projects, "commands": ALL_COMMANDS}
    )


def project_create(request: HttpRequest):
    if request.method == "GET":
        return render(request, "projects/create.jinja", {"form": ProjectForm()})
    elif request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            form.save()

    return redirect("projects")


def project_ProjectID(request: HttpRequest, project_id: int):
    try:
        project = models.Project.objects.get(pk=project_id)
    except models.Project.DoesNotExist:
        return not_found(request, models.Project, project_id)

    return render(
        request,
        "projects/show.jinja",
        {
            "project": project,
            "commands": commands.ProjectCommandBuilder()
            .set_context({"id": str(project.id)})
            .all("Go back")
            .edit("Edit project")
            .delete("Delete project")
            .also_add(
                commands.CategoryCommandBuilder()
                .set_context({"pid": str(project.id)})
                .create("Create a category")
                .build()
            )
            .build(),
        },
    )


def project_ProjectID_delete(request: HttpRequest, project_id: int):
    try:
        project = models.Project.objects.get(pk=project_id)
    except models.Project.DoesNotExist:
        return not_found(request, models.Project, project_id)

    project.delete()

    return redirect("projects")


def project_ProjectID_edit(request: HttpRequest, project_id: int):
    try:
        project = models.Project.objects.get(pk=project_id)
    except models.Project.DoesNotExist:
        return not_found(request, models.Project, project_id)

    # TODO: Logic to be done

    if request.method == "GET":
        return render(
            request,
            "projects/edit.jinja",
            {"project": project, "form": ProjectForm(project.__dict__)},
        )

    elif request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()

    return redirect("project.show", project_id=project.id)


# Categories


def project_ProjectID_category_create(request: HttpRequest, project_id: int):
    try:
        project = models.Project.objects.get(pk=project_id)
    except models.Project.DoesNotExist:
        return not_found(request, models.Project, project_id)

    if request.method == "GET":
        return render(
            request,
            "category/create.jinja",
            {
                "form": CategoryForm(),
                "project_id": project.id,
            },
        )
    elif request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category: models.Category = form.save(commit=False)
            category.project = project
            category.save()

    return redirect("project.show", project_id=project.id)


def project_ProjectID_category_CategoryID_edit(
    request: HttpRequest, project_id: int, category_id: int
):
    try:
        category = models.Category.objects.get(pk=category_id)
    except models.Category.DoesNotExist:
        return not_found(request, models.Category, category_id)

    if request.method == "GET":
        return render(
            request,
            "category/edit.jinja",
            {
                "form": CategoryForm(instance=category),
                "project_id": project_id,
                "category_id": category.id,
            },
        )
    elif request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()

    return redirect("project.show", project_id=project_id)


def project_ProjectID_category_CategoryID_delete(
    request: HttpRequest, project_id: int, category_id: int
):
    try:
        category = models.Category.objects.get(pk=category_id)
    except models.Category.DoesNotExist:
        return not_found(request, models.Category, category_id)

    category.delete()
    return redirect("project.show", project_id=project_id)


def project_ProjectID_category_CategoryID_card_create(
    request: HttpRequest, project_id: int, category_id: int
):
    try:
        category = models.Category.objects.get(pk=category_id)
    except models.Project.DoesNotExist:
        return not_found(request, models.Project, category_id)

    if request.method == "GET":
        return render(
            request,
            "card/create.jinja",
            {
                "form": CardFormNoCategory(),
                "project_id": project_id,
                "category_id": category_id,
            },
        )
    elif request.method == "POST":
        form = CardFormNoCategory(request.POST)
        if form.is_valid():
            card: models.Card = form.save(commit=False)
            card.category = category
            card.save()

    return redirect("project.show", project_id=project_id)

def project_ProjectID_category_CategoryID_card_CardID(
    request: HttpRequest, project_id: int, category_id: int, card_id: int
):
    try:
        card = models.Card.objects.get(pk=card_id)
    except models.Card.DoesNotExist:
        return not_found(request, models.Card, card_id)

    return render(
        request,
        "card/show.jinja",
        {
            "card": card,
            "project_id": project_id,
            "category_id": category_id,
            "commands": commands.CardCommandBuilder()
                .set_context({"pid": str(project_id), "cid": str(category_id), "id": str(card_id)})
                .edit("Edit card")
                .delete("Delete card")
                .also_add(
                    commands.ProjectCommandBuilder()
                    .set_context({"id": str(project_id)})
                    .show("Go back")
                    .build()
                )
                .build()
        },
    )
    
def project_ProjectID_category_CategoryID_card_CardID_edit(
    request: HttpRequest, project_id: int, category_id: int, card_id: int
):
    try:
        card = models.Card.objects.get(pk=card_id)
    except models.Card.DoesNotExist:
        return not_found(request, models.Card, card_id)
    
    if request.method == "GET":
        return render(
            request,
            "card/edit.jinja",
            {
                "form": CardForm(instance=card),
                "project_id": project_id,
                "category_id": category_id,
                "card": card
            }
        )
    elif request.method == "POST":
        form = CardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
    
    return redirect("card.show", project_id=project_id, category_id=category_id, card_id=card_id)

def project_ProjectID_category_CategoryID_card_CardID_delete(
    request: HttpRequest, project_id: int, category_id: int, card_id: int
):
    try:
        card = models.Card.objects.get(pk=card_id)
    except models.Card.DoesNotExist:
        return not_found(request, models.Card, card_id)

    card.delete()
    return redirect("project.show", project_id=project_id)
