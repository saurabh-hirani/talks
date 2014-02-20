from nbcommon import *
import mod1

class TestDocstr1(object):
    """ Test whether the passed entity has a docstring """
    def test_docstr(self, entity):
        if not has_docstr(entity):
            raise NoDocstrError("%s does not have docstr" % entity.__name__)
        return True
        
t1 = TestDocstr1()
t1.test_docstr(mod1)
t1.test_docstr(mod1.SpecFile)
t1.test_docstr(mod1.SpecFile.Section)
t1.test_docstr(mod1.SpecFile.DynamicSection)
t1.test_docstr(mod1.SpecFile.StaticSection)
t1.test_docstr(mod1.SpecFile.Section1)
t1.test_docstr(mod1.SpecFile.Section2)
t1.test_docstr(mod1.main)
