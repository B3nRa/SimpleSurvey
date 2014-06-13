__author__ = 'Benjamin'

import ExerciseHandler

ExerciseHandler.setCsvPath("./exercises.csv")
ExerciseHandler.readCsv()
for ex in ExerciseHandler.exercises:
    print str(ex.id) + " " + ex.exerciseText
    for corAnswer in ex.correctAnswers:
        print corAnswer
    for wrongAnswer in ex.wrongAnswers:
        print wrongAnswer