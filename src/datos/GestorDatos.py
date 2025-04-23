from sklearn.preprocessing import LabelEncoder, StandardScaler
from BaseDatos.BaseDatos import BaseDatos
from sklearn.model_selection import train_test_split, cross_val_score

class GestorDatos:
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.num_cols = ['past_exam_scores', 'study_hours_per_week']
        self.BD = BaseDatos()
        self.df = self.BD.obtener_df_modelo()

    def scaler(self):
        return self.scaler
    def label_encoders(self):
        return self.label_encoders

    def _limpiar_datos(self):
        print(self.df.head())
        print(self.df.info())
        print(self.df.isnull().sum())
        print("Columnas originales:", self.df.columns)
        self.df.drop(['student_id', 'gender', 'parental_education_level', 'final_exam_score'], axis=1, inplace=True)

    def _codificar_variables(self):

        for col in ['internet_access_at_home', 'extracurricular_activities', 'pass_fail']:
            self.label_encoders[col] = LabelEncoder()
            self.df[col] = self.label_encoders[col].fit_transform(self.df[col])

    def _escalar_datos(self):
        self.df[self.num_cols] = self.scaler.fit_transform(self.df[self.num_cols])
        
    def preparar_datos(self):
        self._limpiar_datos()
        self._codificar_variables()
        self._escalar_datos()
        X = self.df.drop('pass_fail', axis=1)
        y = self.df['pass_fail']
        return train_test_split(X, y, test_size=0.2, random_state=42)
        
    def insertar_datos(self, estudiante):
        self.BD.insertar_estudiante(estudiante)

    def obtener_df_analisis(self):
        return self.BD.obtener_df_analisis()