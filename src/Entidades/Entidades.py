class Estudiantes:
    def __init__(self, past_exam_scores, study_hours_per_week, attendance_rate,
                 internet_access_at_home, extracurricular_activities, prediccion):
        self._past_exam_scores = past_exam_scores
        self._study_hours_per_week = study_hours_per_week
        self._attendance_rate = attendance_rate
        self._internet_access_at_home = internet_access_at_home
        self._extracurricular_activities = extracurricular_activities
        self._prediccion = prediccion

        # Getters

    def get_past_exam_scores(self):
        return self._past_exam_scores

    def get_study_hours_per_week(self):
        return self._study_hours_per_week

    def get_attendance_rate(self):
        return self._attendance_rate

    def get_internet_access_at_home(self):
        return self._internet_access_at_home

    def get_extracurricular_activities(self):
        return self._extracurricular_activities

    def get_prediccion(self):
        return self._prediccion

        # Setters

    def set_past_exam_scores(self, value):
        self._past_exam_scores = value

    def set_study_hours_per_week(self, value):
        self._study_hours_per_week = value

    def set_attendance_rate(self, value):
        self._attendance_rate = value

    def set_internet_access_at_home(self, value):
        self._internet_access_at_home = value

    def set_extracurricular_activities(self, value):
        self._extracurricular_activities = value

    def set_prediccion(self, value):
        self._prediccion = value
