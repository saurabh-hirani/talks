# custom exception class for no docstring
class NoDocstrError(Exception): pass

def has_docstr(entity):
    """ Check whether this entity has a docstring """
    docstr = entity.__doc__
    return docstr != None and docstr.strip() != ''

import inspect

def get_entity_type(entity):
    """ Check whether entity is supported for docstring heck """
    for entity_type in ['module', 'function', 'class', 'method'] :
        # inspect module has inspect.ismodule, inspect.isfunction - leverage that
        inspect_func = getattr(inspect, 'is' + entity_type)
        if inspect_func(entity): return entity_type
    raise ValueError('Invalid entity: %s passed' % entity)
