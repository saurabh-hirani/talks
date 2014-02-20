from nbcommon import *
import mod1

import inspect
from collections import defaultdict

class TestDocstr2(object):
    def test_docstr(self, entity):
        """ Test whether the passed in entity and its children have docstring """
        entity_type = None
        non_docstr_entities = defaultdict(list)

        # get all the members of the passed entity
        for member in inspect.getmembers(entity):
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

t2 = TestDocstr2()

print "testing mod1"
print "-----------"
try:
    t2.test_docstr(mod1)
except NoDocstrError as e:
    print e
print "-----------"

print "\ntesting mod1.SpecFile"
print "-----------"
try:
    t2.test_docstr(mod1.SpecFile)
except NoDocstrError as e:
    print e
print "-----------"
