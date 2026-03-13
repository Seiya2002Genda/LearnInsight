from .intent_classifier import IntentClassifier
from .student_ai import StudentAI
from .teacher_ai import TeacherAI
from .admin_ai import AdminAI
from .recommendation_ai import RecommendationAI


class LocalLLMEngine:

    def __init__(self):

        self.classifier = IntentClassifier()

        self.student_ai = StudentAI()

        self.teacher_ai = TeacherAI()

        self.admin_ai = AdminAI()

        self.recommend_ai = RecommendationAI()

    def generate(self, message, context=None):

        if context is None:
            context = {}

        message = message.strip()

        if message == "":
            return "Please enter a message."

        intent = self.classifier.classify(message)

        if intent == "student":
            return self.student_ai.answer(message, context)

        if intent == "teacher":
            return self.teacher_ai.generate_assignment("General", message)

        if intent == "admin":
            return self.admin_ai.school_performance(context)

        if intent == "recommendation":
            return self.recommend_ai.recommend(context)

        return self.student_ai.answer(message, context)