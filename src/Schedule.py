from Credit import Credit
from Course import Course
from Utilities import isDisjoint, union, intersection
from random import choice

class Schedule:

    def __init__(self, *creditHours):
        self.creditHours = list(creditHours)
        self.codes = []
        for credit in self.creditHours:
            self.codes.append(credit.code)
        self.fitness = 0

    def crossover(self, *others):
        creditHours = union(self.creditHours, *others)

        return Schedule(*creditHours)

    def evaluate(self):
        
        if isDisjoint(self.codes) and isDisjoint(self.creditHours):

            days = {}

            for credit in self.creditHours:
                for day, times in credit.days.items():
                    if day not in days:
                        days[day] = []
                    
                    if any(time in days[day] for time in times):
                        fitness = 0
                        return
                    
                    days[day].extend(times)
            
            for day in days:
                days[day] = sorted(days[day], key=lambda time: time[0])

                for index in range(1, len(days[day])):
                    if days[day][index - 1][1] > days[day][index][0]:
                        self.fitness = 0
                        return

            self.fitness = 1
        else:
            self.fitness = 0

    """def swap(self, credit):
        self.creditHours.remove(choice(self.creditHours))
        self.creditHours.append(credit)
        self.codes = []
        for credit in self.creditHours:
            self.codes.append(credit.code)"""

    def __repr__(self):
        return "{}".format(self.creditHours)
    
    def __hash__(self):

        return hash(tuple(sorted(self.codes)))

    def __eq__(self, other):
        return intersection(self.codes, other.codes) and intersection(self.creditHours, other.creditHours)
