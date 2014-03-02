from nbcommon import *
import mod1

import inspect
import sys
from collections import defaultdict

class Modstruct2(object):
    """ Return a data structure representing all members of the passed
    entity """

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
        parent_name = entity.__name__
        for member in inspect.getmembers(entity):
            ref = member[1]
            # member has to be of supported entity type
            try:
                ref_type = get_entity_type(ref)
            except ValueError:
                continue

            # we will not inspect modules imported in base module
            if inspect.ismodule(ref): continue

            # member has to be defined in base module
            if ref.__module__ != self.base_module.__name__: continue

            # valid member - construct member data
            member_data = {
                'type': ref_type, 
                'ref': ref, 
                'name': entity.__name__ + '.' + ref.__name__,
                'parent_ref': entity,
                'parent_name': parent_name,
            }
            members.append(member_data)
        return members

    def get_all_members(self):
        """ Get all the members (nested also) of the passed entity """
        # add base module as the first element
        all_members = [{'type': 'module',
                        'ref': self.base_module, 
                        'name': self.base_module.__name__,
                        'parent_ref': None,
                        'parent_name': None}]

        # get first level members of the main entity
        nested_members = self.get_entity_members(self.base_entity)
        all_members.extend(nested_members)

        # call get_entity_members repetitively till you reach a stage where 
        # there are no nested members
        while nested_members:
            curr_nested_members = []
            for member_data in nested_members:
                if member_data['type'] == 'class':
                    # drill nested members only in a class
                    members = self.get_entity_members(member_data['ref'])
                    curr_nested_members.extend(members)
            nested_members = curr_nested_members
            all_members.extend(nested_members)

        return all_members

class TestDocstr2(object):

    @classmethod
    def test_docstr(self, entity):
        all_members = Modstruct2(entity).get_all_members()

        non_docstr_entities = defaultdict(list)

        # get all the nested members of root entity
        for member_data in all_members:
            # consolidate members based on type
            if not has_docstr(member_data['ref']):
                member_name = member_data['name']
                non_docstr_entities[member_data['type']].append(member_name)

        if non_docstr_entities.keys():
            errors = []
            # create error string
            for entity_type, refs in non_docstr_entities.iteritems():
                for refname in refs:
                    errors.append('%s: %s does not have docstr' % (entity_type,
                                                                   refname))
            raise NoDocstrError('\n' + '\n'.join(errors))
        return True

TestDocstr2.test_docstr(mod1)
