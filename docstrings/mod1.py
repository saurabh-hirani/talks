class SpecFile(object):
    class Section(object):
        def __init__(self): pass
        def validate(self): pass
        
    class DynamicSection(Section):
        def __init__(self): pass
        
    class StaticSection(Section):
        def __init__(self): pass
        
    class Section1(StaticSection):
        def __init__(self): pass
        def validate(self): pass
        
    class Section2(DynamicSection):
        def __init__(self): pass
        def validate(self): pass
        
def main():
    pass
