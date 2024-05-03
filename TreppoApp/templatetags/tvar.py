import typing

from django import template

register = template.Library()


@register.simple_tag
def tvar(obj: typing.Any) -> typing.Any:
    return vars(obj)


@register.simple_tag
def ttype(obj: typing.Any) -> typing.Any:
    return type(obj)
