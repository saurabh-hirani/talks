from nbcommon import *
import mod1

import inspect
import sys
from collections import defaultdict

class TestDocstr3(object):

    # update __init__ to load entity at startup as there a few more
    # params being initialized 
    def __init__(self, base_entity):
        self.base_entity_type = get_entity_type(base_entity)
        self.base_entity = base_entity
        self.base_module = base_entity
        if self.base_entity_type != 'module':
            # if entity_type is class - know which module it belongs to
            self.base_module = sys.modules[base_entity.__module__]

    def get_entity_members(self, entity):
        """ Get first level members of the passed entity """
        members = []
        for member in inspect.getmembers(entity):
            ref = member[1]
            # member has to be of supported entity type
            try:
                ref_type = get_entity_type(ref)
            except ValueError:
                continue
            # member has to be defined in base module
            if ref.__module__ != self.base_module.__name__: continue
            # valid member - append member reference and type to the member 
            # list
            members.append((ref_type, ref))
        return members

    def get_all_members(self):
        """ Get all the members (nested also) of the passed entity """
        all_members = [(self.base_entity_type, self.base_entity)]
        # get first level members of the main entity
        nested_members = self.get_entity_members(self.base_entity)
        all_members.extend(nested_members)

        # call get_entity_members repetitively till you reach a stage where 
        # there are no nested members
        while nested_members:
            curr_nested_members = []
            for member_type, member_ref in nested_members:
                if member_type == 'class':
                    # drill nested members only in a class
                    members = self.get_entity_members(member_ref)
                    curr_nested_members.extend(members)
            nested_members = curr_nested_members
            all_members.extend(nested_members)

        return all_members

    def test_docstr(self):

        non_docstr_entities = defaultdict(list)

        # get all the nested members of root entity
        for member_type, member_ref in self.get_all_members():
            # consolidate members based on type
            if not has_docstr(member_ref):
                non_docstr_entities[member_type].append(member_ref)

        if non_docstr_entities.keys():
            errors = []
            # create error string
            for entity_type, refs in non_docstr_entities.iteritems():
                for ref in refs:
                    errors.append('%s: %s does not have docstr' % (entity_type,
                                                                ref.__name__))
            raise NoDocstrError('\n' + '\n'.join(errors))

        return True

t3 = TestDocstr3(mod1)
t3.test_docstr()
