from typing import TypedDict

class Question(TypedDict):
    title: str
    question: str
    correctAnswer: str
    sequenceNumber: int 