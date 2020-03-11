from Utilities import convertTime

class Course:

    def __init__(self, name, code, crn, section, days, start, end):
        self.name = name
        self.code = code
        self.crn = crn
        self.section = section
        self.days = days
        self.time = (convertTime(start), convertTime(end))

    def __repr__(self):
        return "{}-{}".format(self.code, self.section)