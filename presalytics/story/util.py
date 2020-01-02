"""
Utility functions for the presalytics.story module
"""
import re
import logging
import typing

logger = logging.getLogger('presalytics.story.util')


def to_snake_case(camel_case_str):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_case_str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def to_title_case(name_string):
    try:
        components = re.split('_| ', name_string)
        return ''.join(x[0].upper() + x[1:] for x in components)
    except Exception:
        return name_string.replace(" ", "")


def camel_case_split(str): 
    words = [[str[0]]] 
  
    for c in str[1:]: 
        if words[-1][-1].islower() and c.isupper(): 
            words.append(list(c)) 
        else: 
            words[-1].append(c) 
  
    return [''.join(word) for word in words] 
