from nbcommon import *
import mod1

import inspect
import sys
from collections import defaultdict

class Modstruct3(object):
    """ Return a data structure representing all members of the passed
    entity """

    def __init__(self, base_entity):
        self.base_entity_type = get_entity_type(base_entity)
        self.base_entity = base_entity
        self.base_module = base_entity
        self.id_name_map = {}
        self.all_members = []
        if self.base_entity_type != 'module':
            # if entity_type is class - know which module it belongs to
            self.base_module = sys.modules[base_entity.__module__]

    def get_entity_name(self, entity):
        """ Return fully qualified name of entity """
        return self.id_name_map.get(id(entity), None)

    def build_id_name_map(self, entity, parent=None):
        """ Map entity id to its fully qualified name """
        entity_name = entity.__name__
        if not parent is None:
            id_parent = id(parent)
            if id_parent in self.id_name_map:
                parent_name = self.id_name_map[id_parent]
                entity_name = '.'.join([parent_name, entity.__name__])
        self.id_name_map[id(entity)] = entity_name

    def extract_entity_members(self):
        """ From all the members extract out member tree of the base 
        entity """
        base_entity_name = self.get_entity_name(self.base_entity)

        base_entity_members = []
        for member in self.all_members:
            if member['name'].startswith(base_entity_name):
                base_entity_members.append(member)
        self.base_entity_members = base_entity_members

    def get_entity_members(self, entity):
        """ Get first level members of the passed entity """
        members = []
        parent_name = self.get_entity_name(entity)
        for member in inspect.getmembers(entity):
            ref = member[1]
            # member has to be of supported entity type
            try:
                ref_type = get_entity_type(ref)
            except ValueError:
                continue
            # member has to be defined in base module
            if ref.__module__ != self.base_module.__name__: continue
            # valid member - append member reference, type and name to the 
            # member  list
            member_data = {
                'type': ref_type, 
                'ref': ref, 
                'parent': entity,
                'name': parent_name + '.' + ref.__name__
            }
            members.append(member_data)
            self.build_id_name_map(ref, entity)
        return members

    def get_all_members(self):
        """ Get all the members (nested also) of the passed entity """

        # add base module as the first element
        all_members = [{'type': 'module',
                        'ref': self.base_module, 
                        'parent_ref': None,
                        'name': self.base_module.__name__}]

        # add base module as first entry to id_name_map - root of all names
        self.build_id_name_map(self.base_module, None)

        # get first level members of the module
        nested_members = self.get_entity_members(self.base_module)
        all_members.extend(nested_members)

        # call get_entity_members repetitively till you reach a stage where 
        # there are no nested members
        while nested_members:
            curr_nested_members = []
            # for member_type, member_ref, member_name in nested_members:
            for member_data in nested_members:
                if member_data['type'] == 'class':
                    # drill nested members only in a class
                    members = self.get_entity_members(member_data['ref'])
                    curr_nested_members.extend(members)
            nested_members = curr_nested_members
            all_members.extend(nested_members)

        self.all_members = all_members

        # if entity is not a module extract the entity members from all 
        # members
        if self.base_entity_type == 'module':
            return all_members

        self.extract_entity_members()
        return self.base_entity_members

class TestDocstr3(object):

    @classmethod
    def test_docstr(self, entity):
        all_members = Modstruct3(entity).get_all_members()

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


TestDocstr3.test_docstr(mod1.SpecFile.Section1)
