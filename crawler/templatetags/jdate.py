from django import template
from django.template.defaultfilters import stringfilter
import jdatetime

register = template.Library()


@register.filter
def jdate(date):
    return jdatetime.datetime.fromgregorian(year=date.year, month=date.month, day=date.day,
                                            hour=date.hour, minute=date.minute, second=date.second)
