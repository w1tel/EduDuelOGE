from typing import TypedDict


class Question(TypedDict):
    title: str
    statement: str
    question: str
    difficulty: str
    answerFormat: str
    correctAnswer: str
    sequenceNumber: int
    code: str
    solutionExplanation: str


class Statistic(TypedDict):
    total_tests: int
    correct_answers: int
    success_rate: int


class User(TypedDict):
    username: str
    statistic: Statistic
    number_of_tests: int
    state: str
    correct_answer_question: str | None
    seria_of_questions: list[Question]
    solutionExplanation: str

# Тип для словаря пользователей
Users = dict[int, User] 