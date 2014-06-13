import BaseHTTPServer
import sys
import json
import time
import urlparse
import ExerciseHandler
import UserHandler

HOST_NAME = sys.argv[1]
PORT = int(sys.argv[2])

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    escapeSQL = False

    def do_GET(self):
        print "in do_get"
        self.setHeaders([{'type': 'Access-Control-Allow-Origin', 'value': 'http://localhost'}, {'type': 'CONTENT-TYPE', 'value': 'application/json'}])
        path = self.path.split("?")[0]
        if path == '/questions/':
            self.sendQuestion()
        elif path == '/numberExercises/':
            self.sendNumberOfExercises()
        elif path == '/results/':
            self.sendResults()

    def do_POST(self):
        print "path " + self.path
        self.setHeaders([{'type': 'Access-Control-Allow-Origin', 'value': 'http://localhost'}, {'type': 'CONTENT-TYPE', 'value': 'application/json'}])
        path = self.path.split("?")[0]
        if path == '/questionAnswer/':
            self.giveAnswer()

    def setHeaders(self, headers):
        self.send_response(200)
        for header in headers:
            self.send_header(header['type'], header['value'])
        self.end_headers()

    def readPayload(self):
        contentLength = int(self.headers.getheader('content-length'))
        postBody = self.rfile.read(contentLength)
        jsonBody = json.loads(postBody)
        return jsonBody

    def sendNumberOfExercises(self):
        self.wfile.write(json.dumps({'numberExercises': len(ExerciseHandler.exercises)}))

    def sendQuestion(self):
        parameters = urlparse.parse_qs(urlparse.urlparse(self.path).query)
        print parameters
        exercise = ExerciseHandler.exercises[int(parameters['questionNumber'][0])]

        user = UserHandler.getUserByName(parameters['user'][0])
        userAnswer = ''

        if user is not None:
            questionAnswer = user.checkIfAlreadyAnswered(exercise.id)
            if questionAnswer is not None:
                userAnswer = questionAnswer['answer']

        if exercise.type == 'freeText':
            self.wfile.write(json.dumps({'id': exercise.id, 'type': 'freeText', 'question': exercise.exerciseText, 'givenAnswer': userAnswer}))
        elif exercise.type == 'multipleChoice':
            answerSelection = []
            for correctAnswer in exercise.correctAnswers:
                answerSelection.append(correctAnswer)
            for wrongAnswer in exercise.wrongAnswers:
                answerSelection.append(wrongAnswer)
            self.wfile.write(json.dumps({'id': exercise.id, 'type': 'multipleChoice', 'question': exercise.exerciseText,
                                         'answerSelection': answerSelection, 'givenAnswer': userAnswer}))

    def giveAnswer(self):
        self.setHeaders([{'type': 'CONTENT-TYPE', 'value': 'application/json'}])
        jsonBody = self.readPayload()
        isCorrect = ExerciseHandler.checkAnswer(jsonBody['questionId'], jsonBody['answer'])
        parameters = urlparse.parse_qs(urlparse.urlparse(self.path).query)
        UserHandler.setQuestionAnswer(parameters['user'][0], parameters['questionNumber'][0], jsonBody['answer'], isCorrect)

    def sendResults(self):
        questions = []

        for exercise in ExerciseHandler.exercises:
            answeredCounter = 0
            answeredCorrectlyCounter = 0
            answers = []

            for user in UserHandler.users:
                for answeredExercise in user.questionAnswerMap:
                    if answeredExercise['id'] == exercise.id:
                        answeredCounter += 1
                        if answeredExercise['isCorrect'] == True:
                            answeredCorrectlyCounter += 1
                        answers.append({'user': user.userName, 'answer': answeredExercise['answer'], 'isCorrect': answeredExercise['isCorrect']})

            question = {'exercise': exercise.exerciseText, 'correctAnswers': exercise.correctAnswers,
                        'answeredCorrectlyCounter': answeredCorrectlyCounter, 'answeredCounter': answeredCounter, 'answers': answers}
            questions.append(question)

        self.wfile.write(json.dumps(questions))

if __name__ == '__main__':
    exercisesPath = "./exercises.csv"
    ExerciseHandler.setCsvPath(exercisesPath)
    ExerciseHandler.readCsv()
    print "Read exercises from " + exercisesPath

    httpServer = BaseHTTPServer.HTTPServer
    myServer = httpServer((HOST_NAME, PORT), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT)
    try:
        myServer.serve_forever()
    except KeyboardInterrupt:
        pass
    myServer.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT)