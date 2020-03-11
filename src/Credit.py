class Credit:

    def __init__(self, code, *courses):
        self.code = code
        self.courses = courses

        self.days = {}

        for course in self.courses:
            for day in course.days:
                if day not in self.days:
                    self.days[day] = []
                self.days[day].append(course.time)

    def __repr__(self):
        return repr(self.courses)

    def __hash__(self):
        return hash(self.code)

    def __eq__(self, other):
        return self.code == other.code