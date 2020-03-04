from pymongo import MongoClient
from Class import Class
from Credit import Credit
from Schedule import Schedule
from itertools import product, combinations
from math import ceil

class User:

    def __init__(self, *courses):
        self.courses = set(courses)  # String of Class Names, etc..
        self.maxCourses = len(self.courses)  # Number of categories to reach.
        self.population = set()
        self.generations = 0

    def evaluate(self):

        for schedule in self.population:
            schedule.evaluate()

    def select(self):
        matingPool = set()
        newPopulation = set()

        for parent in self.population:
            if parent.fitness == 1:
                matingPool.add(parent)

        combos = list(combinations(matingPool, 2))

        for combination in combos:
            if combination[0].codes != combination[1].codes:
                crossover = self.crossover(combination[0], combination[1])
                newPopulation.add(crossover)

        self.population = newPopulation

    def crossover(self, scheduleA, scheduleB):

        return scheduleA.crossover(scheduleB)

    def draw(self):
        self.select()
        self.evaluate()
        self.generations += 1

    def getCredits(self, code):
        username = input("Username: ")
        password = input("Password: ")

        client = MongoClient(
            "mongodb+srv://{}:{}@coursica-ylslv.mongodb.net/test?retryWrites=true&w=majority".format(username, password))
        db = client.Coursica
        collection = db.DSU

        courses = collection.find({"code": code})

        sections = []
        tutorials = []
        labs = []

        for course in courses:

            del course["_id"]

            if course['section'][0] == "B":
                labs.append(Class(**course))
            elif course['section'][0] == "T":
                tutorials.append(Class(**course))
            else:
                sections.append(Class(**course))

        classes = []

        if sections:
            classes.append(sections)

        if tutorials:
            classes.append(tutorials)

        if labs:
            classes.append(labs)

        credit = []

        for courses in product(*classes):
            credit.append(Credit(code, *courses))

        return credit

    def generateInitialPopulation(self):
        initial_population = set()

        for courses in self.courses:
            creditHours = self.getCredits(courses)

            for credit in creditHours:
                initial_population.add(Schedule([courses], [credit]))

        self.population = initial_population
        self.evaluate()

    def output(self):
        schedules = []

        if self.population:
            for schedule in self.population:
                crns = []

                for credit in schedule.creditHours:
                    for course in credit.courses:
                        crns.append(course.crn)

                schedules.append(crns)
        else:
            return "Failure"

        return schedules

    def isComplete(self):
        
        if self.generations >= ceil(self.maxCourses / 2):
            return True
        
        if not self.population:
            return True
        
        return False

    def getSchedules(self):
        self.generateInitialPopulation()

        while not self.isComplete():
            self.draw()

        return self.output()