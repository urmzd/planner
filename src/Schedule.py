from Credit import Credit
from Class import Class


class Schedule:

    def __init__(self, codes, creditHours):
        self.codes = set(codes)
        self.creditHours = set(creditHours)
        self.fitness = -1

    def evaluate(self):

        if self.isConflicted():
            self.fitness = 0
        else:
            self.fitness = 1

    def crossover(self, scheduleB):
        creditHours = self.creditHours.union(scheduleB.creditHours)
        codes = self.codes.union(scheduleB.codes)

        return Schedule(codes, creditHours)

    def isConflicted(self, schedule=None):

        if schedule is None:
            creditHours = self.creditHours
        else:

            if not self.codes.difference(schedule).codes:
                # Check to see if there is no difference between two sets.
                return True
            else:
                creditHours = self.creditHours.union(schedule.creditHours)

        days = {}

        for credit in creditHours:
            for course in credit.courses:
                for day in course.days:
                    if day not in days:
                        days[day] = []

                    if course.time in days[day]:
                        return True
                    else:
                        days[day].append(course.time)

        for day in days:
            days[day] = sorted(days[day], key=lambda time: time[0])

            for index in range(1, len(days[day])):
                if days[day][index - 1][1] > days[day][index][0]:
                    return True

        return False

    def __repr__(self):
        return "{} : {}".format(self.codes, self.creditHours)

    def __hash__(self):
        return hash((repr(self.codes), repr(self.creditHours)))

    def __eq__(self, other):
        return self.codes == other.codes and self.creditHours == other.creditHours