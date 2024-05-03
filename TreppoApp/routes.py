from django.urls import path

from . import views

urlpatterns = [
    # View all project
    path("", views.projects, name="projects"),
    # Create a project
    path("project/create/", views.project_create, name="project.create"),
    # View a single project (Get into categories)
    path("project/<int:project_id>/", views.project_ProjectID, name="project.show"),
    # Edit a project
    path(
        "project/<int:project_id>/edit/",
        views.project_ProjectID_edit,
        name="project.edit",
    ),
    # Delete a project
    path(
        "project/<int:project_id>/delete/",
        views.project_ProjectID_delete,
        name="project.delete",
    ),
    # Categories
    # Create a category
    path(
        "project/<int:project_id>/category/create/",
        views.project_ProjectID_category_create,
        name="category.create",
    ),
    # Edit a category
    path(
        "project/<int:project_id>/category/<int:category_id>/edit/",
        views.project_ProjectID_category_CategoryID_edit,
        name="category.edit",
    ),
    # Delete a category
    path(
        "project/<int:project_id>/category/<int:category_id>/delete/",
        views.project_ProjectID_category_CategoryID_delete,
        name="category.delete",
    ),
    # Cards
    # Create a card
    path(
        "project/<int:project_id>/category/<int:category_id>/card/create/",
        views.project_ProjectID_category_CategoryID_card_create,
        name="card.create",
    ),
    # Show a card
    path(
        "project/<int:project_id>/category/<int:category_id>/card/<int:card_id>/",
        views.project_ProjectID_category_CategoryID_card_CardID,
        name="card.show",
    ),
    # Edit a card
    path(
        "project/<int:project_id>/category/<int:category_id>/card/<int:card_id>/edit/",
        views.project_ProjectID_category_CategoryID_card_CardID_edit,
        name="card.edit",
    ),
    # Delete a card
    path(
        "project/<int:project_id>/category/<int:category_id>/card/<int:card_id>/delete/",
        views.project_ProjectID_category_CategoryID_card_CardID_delete,
        name="card.delete",
    ),
]
