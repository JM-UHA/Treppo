import typing

from django.db import models
from django.urls import reverse


class Card(models.Model):
    id = models.AutoField(primary_key=True)

    title = models.CharField(max_length=80)
    description = models.CharField(max_length=300)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    category: models.ForeignKey["Category"] = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="cards"
    )
    
    @property
    def url(self) -> str:
        return reverse("card.show", kwargs={"project_id": self.category.project.id, "category_id": self.category.id, "card_id": self.id})

    def __str__(self) -> str:
        return self.title


class Category(models.Model):
    id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=80)
    description = models.CharField(max_length=300)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    project: models.ForeignKey["Project"] = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="categories"
    )
    
    cards: typing.Any

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    categories: typing.Any

    def __str__(self) -> str:
        return self.name


MODELS = [Card, Category, Project]
