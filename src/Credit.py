class Credit:

    def __init__(self, code, *courses):
        
        self.code = code
        self.courses = set(courses)

    def __repr__(self):
        return repr(self.courses)