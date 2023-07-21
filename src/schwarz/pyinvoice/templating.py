
from decimal import Decimal
import re


__all__ = ['templated_text']

def is_number(value):
    return isinstance(value, (int, float, Decimal))

def templated_text(text, dbobj, formatter):
    regex = re.compile(r'\{.+?\}')
    matches = tuple(regex.finditer(text))
    if not matches:
        return text

    result = ''
    tmpl_vars = {**dbobj.meta}
    last_pos = 0
    for match in matches:
        _s, _e = match.span()
        result += text[last_pos:_s]
        tmpl_text = text[_s+1:_e-1]
    
        var_and_filter = re.split(r'\s*\|\s*', tmpl_text, maxsplit=1)
        if len(var_and_filter) == 2:
            tmpl_var, tmpl_filter = var_and_filter
        else:
            tmpl_var, = var_and_filter
            tmpl_filter = None
    
        tmpl_value = tmpl_vars[tmpl_var]
        if tmpl_filter:
            fn = getattr(formatter, tmpl_filter)
            generated_str = fn(tmpl_value)
        elif is_number(tmpl_value):
            generated_str = formatter.number(tmpl_value)
        else:
            generated_str = str(tmpl_value)
        result += generated_str
        last_pos = _e

    result += text[last_pos:]
    return result
