# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django import template
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe

register = template.Library()


class_re = re.compile(r'(?<=class=["\'])(.*)(?=["\'])')

@register.filter
def add_class(value, css_class):
    value = smart_text(value)
    match = class_re.search(value)
    if match:
        m = re.search(r'^%s$|^%s\s|\s%s\s|\s%s$' % (css_class, css_class,
                                                    css_class, css_class), match.group(1))
        if not m:
            return mark_safe(class_re.sub(match.group(1) + " " + css_class,
                                          value))
    else:
        return mark_safe(value.replace('>', ' class="%s">' % css_class))
    return value
