import json
from pymongo import MongoClient
from Course import Course
from Credit import Credit
from Schedule import Schedule
from itertools import product, combinations

class User:

    def __init__(self, semester, *codes):
        self.codes = codes
        self.semester = semester
        self.creditHours = []
        self.population = []

    def getCredits(self, code):
        
        with open('config.json') as config:
            cred = json.load(config)
            
        client = MongoClient(cred['connection'])

        sections = []
        tutorials = []
        labs = []

        results = client[cred['database']][cred['collection']].find({"code": "{} {}".format(code, self.semester)})
        
        for course in results:  
            del course['_id']

            if course['section'][0] == "T":
                tutorials.append(Course(**course))
            elif course['section'][0] == "B":
                labs.append(Course(**course))
            else:
                sections.append(Course(**course))
        
        courses = []

        if sections:
            courses.append(sections)
        
        if labs:
            courses.append(labs)

        if tutorials:
            courses.append(tutorials)

        creditHours = []

        for courses in product(*courses):
            creditHours.append(Credit(code, *courses))

        return creditHours

    def generateInitialPopulation(self):
        for code in self.codes:
            creditHours = self.getCredits(code)
            self.creditHours.append(creditHours)

    def crossover(self, *schedules):
        return self.crossover(*schedules)

    def evaluate(self, schedules):
        for schedule in schedules:
            schedule.evaluate()

    def select(self):
       
        combos = list(product(*self.creditHours))
        
        matingPool = []
        for courses in combos:
            matingPool.append(Schedule(*courses))
        
        self.evaluate(matingPool)

        for schedule in matingPool:
            if schedule.fitness == 1:
                self.population.append(schedule)

    """def mutate(self, schedule):
        
        pass"""
    
    """def terminate(self):
        if self.population:
            for schedule in self.population:
                if len(schedule) == len(self.codes):
                    return True
        else:
            return True"""

    def draw(self):
        self.generateInitialPopulation()
        self.select()
        
        if self.population:
            results = []
            for schedule in self.population:
                crns = []
                for credit in schedule.creditHours:
                    for course in credit.courses:
                        crns.append(course.crn)

                results.append(crns)
        else:
            result = "There are no possible options with the current set provided."
        
        print(self.population)
        
        #self.mutate()
        #self.terminate()


user = User("S", "CSCI1105")
user.draw()
