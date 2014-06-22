__author__ = 'Benjamin'

import csv
import re

csvPath = ""
exercises = []


def setCsvPath(path):
    global csvPath
    csvPath = path


def readCsv():
    with open(csvPath, "rb") as csvfile:
        exerciseReader = csv.reader(csvfile, delimiter=";")
        exerciseId = 0
        for row in exerciseReader:
            exercise = createExercise(exerciseId, row)
            exercises.insert(exerciseId, exercise)
            exerciseId += 1


def createExercise(exerciseId, row):
    exercise = Exercise(exerciseId, row[0], row[1])
    for num in range(0, len(row), 1):
        extractAnswers(exercise, row[num])
    return exercise


def extractAnswers(exercise, answer):
    correctAnswerIndex = answer.find("r:=")
    falseAnswerIndex = answer.find("f:=")
    if correctAnswerIndex > -1:
        exercise.setCorrectAnswer(answer[3:])
    elif falseAnswerIndex > -1:
        exercise.setWrongAnswer(answer[3:])


def checkAnswer(questionId, answer):
    if answer in exercises[questionId].correctAnswers:
        print "Correct"
        return True
    else:
        for correctAnswer in exercises[questionId].correctAnswers:
            correctAnswerRegex = buildRegexOfAnswer(correctAnswer)
            print correctAnswerRegex
            matches = re.findall(r''+correctAnswerRegex, answer, re.IGNORECASE)
            if len(matches) > 0:
                print "Correct"
                return True
        print "Incorrect"
        return False

def buildRegexOfAnswer(str):
    str = re.escape(str)
    print str
    str = str.replace('\ ', '\s+')
    str += '([^0-9a-zA-Z])*$'
    return str

class Exercise():
    def __init__(self, exerciseId, exerciseText, type):
        self.id = exerciseId
        self.exerciseText = exerciseText
        self.type = type
        self.correctAnswers = []
        self.wrongAnswers = []

    def setCorrectAnswer(self, correctAnswer):
        self.correctAnswers.append(correctAnswer)

    def setWrongAnswer(self, wrongAnswer):
        self.wrongAnswers.append(wrongAnswer)