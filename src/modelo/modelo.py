import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.model_selection import cross_val_score



class Modelo:
    def __init__(self, label_encoders, scaler):
        self.model = LogisticRegression(max_iter=100)
        self.num_cols = ['past_exam_scores', 'study_hours_per_week']
        self.scaler = scaler
        self.label_encoders = label_encoders


    def evaluar_modelo(self, X, y, X_test, y_test):
        print("Validación cruzada (5 folds):")
        scores = cross_val_score(self.model, X, y, cv=5)
        print("Precisión media:", scores.mean())

        y_pred = self.model.predict(X_test)
        print("\nMatriz de confusión:")
        print(confusion_matrix(y_test, y_pred))
        print("\nReporte de clasificación:")
        print(classification_report(y_test, y_pred))
        print("\nPrecisión:")
        print(accuracy_score(y_test, y_pred))

    def entrenar_modelo(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predecir_nuevo_estudiante(self, estudiante_dict, columnas_modelo):
        nuevo = pd.DataFrame(estudiante_dict)
        for col in ['internet_access_at_home', 'extracurricular_activities']:
            nuevo[col] = self.label_encoders[col].transform(nuevo[col])
        nuevo[self.num_cols] = self.scaler.transform(nuevo[self.num_cols])
        nuevo = nuevo[columnas_modelo]
        pred = self.model.predict(nuevo)
        resultado = self.label_encoders['pass_fail'].inverse_transform(pred)
        return resultado[0]