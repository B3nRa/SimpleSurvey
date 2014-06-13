__author__ = 'Benjamin'

users = []

def getUserByName(name):
    for user in users:
        if user.userName == name:
            return user
    return None

def setQuestionAnswer(userName, questionId, answer, isCorrect):
    questionId = int(questionId)
    foundUser = False
    for user in users:
        if user.userName == userName:
            questionAnswer = user.checkIfAlreadyAnswered(questionId)

            if questionAnswer is None:
                user.setQuestionAnswer(questionId, answer, isCorrect)
            else:
                user.updateQuestionAnswer(questionAnswer, answer, isCorrect)

            foundUser = True
            print "used old"

    if foundUser == False:
        userObj = User(len(users)+1, userName)
        userObj.setQuestionAnswer(questionId, answer, isCorrect)
        users.append(userObj)
        print "created newly"

    print userName + str(questionId) + answer + str(isCorrect)


class User():
    def __init__(self, userId, userName):
        self.userId = userId
        self.userName = userName
        self.answeredQuestionIds = []
        self.questionAnswerMap = []

    def setAnsweredQuestionId(self, answeredQuestionId):
        self.answeredQuestionIds.append(answeredQuestionId)

    def setQuestionAnswer(self, questionId, answer, isCorrect):
        self.setAnsweredQuestionId(questionId)
        questionAnswer = {'id': questionId, 'answer': answer, 'isCorrect': isCorrect}
        self.questionAnswerMap.append(questionAnswer);

    def updateQuestionAnswer(self, questionAnswer, answer, isCorrect):
        questionAnswer['answer'] = answer
        questionAnswer['isCorrect'] = isCorrect

    def checkIfAlreadyAnswered(self, questionId):
        for questionAnswer in self.questionAnswerMap:
            if questionAnswer['id'] == questionId:
                return questionAnswer
        return None