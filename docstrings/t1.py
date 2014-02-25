from nbcommon import *
import mod1

import inspect
from collections import defaultdict

class ModStruct1(object):
    """ Return a data structure representing all members of the passed
    entity """

    def __init__(self, base_entity):
        self.base_entity = base_entity

    def get_all_members(self):
        """ Get all the members (nested also) of the passed entity """
        return inspect.getmembers(self.base_entity)


class TestDocstr1(object):

    @classmethod
    def test_docstr(self, entity):
        """ Test whether the passed in entity and its children have docstring """
        entity_type = None
        non_docstr_entities = defaultdict(list)
        all_members = ModStruct1(entity).get_all_members()

        # get all the members of the passed entity
        for member in all_members:
            ref = member[1]
            try:
                entity_type = get_entity_type(ref)
                if not has_docstr(ref):
                    non_docstr_entities[entity_type].append(ref)
            except ValueError:
                # invalid entity type - skip it
                continue

        # if any entities without docstring - consolidate and raise error
        if non_docstr_entities.keys():
            errors = []
            for entity_type, refs in non_docstr_entities.iteritems():
                for ref in refs:
                    errors.append('%s %s does not have docstr' % (entity_type,
                                                                  ref.__name__))
            raise NoDocstrError('\n'.join(errors))

        return True

TestDocstr1.test_docstr(mod1)
