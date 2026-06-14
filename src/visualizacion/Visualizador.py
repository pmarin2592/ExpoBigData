import uuid

from datos.GestorDatos import GestorDatos
from modelo.modelo import Modelo
import streamlit as st
import plotly.express as px
from Entidades.Entidades import Estudiantes


class Visualizador:
    def __init__(self):
        self.model= None
        self.GD = GestorDatos()
        self.X = None
        self.y = None


    def _cargar_modelo(self):
        X_train, X_test, y_train, y_test = self.GD.preparar_datos()
        self.model = Modelo(self.GD.label_encoders, self.GD.scaler)
        self.model.entrenar_modelo(X_train, y_train)
        self.X = self.GD.df.drop('pass_fail', axis=1)
        self.y = self.GD.df['pass_fail']
        self.model.evaluar_modelo( self.X,  self.y, X_test, y_test)

    def cargar_formulario(self):
        past_exam_scores = st.number_input("¿Cómo has sentido tu rendimiento en los últimos exámenes? Si tuvieras que darme un aproximado de tu nota, ¿Cómo andaríamos?", min_value=0, max_value=100, value=50)
        study_hours_per_week = st.number_input("Y fuera de las lecciones, ¿cuánto tiempo aproximado le dedicas a repasar a la semana?", min_value=0, value=60)
        attendance_rate = st.number_input("Contame sobre las herramientas en tu casa, ¿tenés internet estable para hacer los trabajos o se te complica a veces?", min_value=0.0, max_value=100.0, value=80.0)
        internet_access = st.selectbox("¿Acceso a Internet en casa?", ["Si", "No"])
        extracurricular = st.selectbox("¿Participa en actividades extracurriculares?", ["Si", "No"])

        if st.button("Predecir"):
            datos = {
                'past_exam_scores': [past_exam_scores],
                'study_hours_per_week': [study_hours_per_week],
                'attendance_rate': [attendance_rate],
                'internet_access_at_home': [internet_access],
                'extracurricular_activities': [extracurricular]
            }
            # Cargar modelo y log del entrenamiento
            self._cargar_modelo()

            # Realizar predicción
            resultado = self.model.predecir_nuevo_estudiante(datos, self.X.columns)

            estudiante =  Estudiantes(
            past_exam_scores=past_exam_scores,
            study_hours_per_week=study_hours_per_week,
            attendance_rate=attendance_rate,
            internet_access_at_home=internet_access,
            extracurricular_activities=extracurricular,
            prediccion="Aprobado" if resultado == 'Pass' else "Reprobado"
            )

            self.GD.insertar_datos(estudiante)
            st.success("✅ Predicción realizada con éxito")

            with st.expander("Ver resultados de la predicción", expanded=True):
                # Mostrar resultados en dos columnas
                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Predicción", "✅ Aprobado" if resultado == 'Pass' else "❌ Reprobado")

    def cargar_estadisticas(self):

        st.title("📊 Monitoreo de Predicciones de Estudiantes")

        # ——— Auto‐refresh cada 10 segundos vía META tag ———
       # st.markdown(
        #    '<meta http-equiv="refresh" content="10">',
        #    unsafe_allow_html=True
        #)

        df = self.GD.obtener_df_analisis()

        # Gráfico 1: Conteo por predicción

        fig1 = px.histogram(
            df,
            x="prediccion",
            title="Distribución de Predicciones",
            color="prediccion",
            labels={"prediccion": "Predicción"}
        )
        st.plotly_chart(fig1, use_container_width=True, key="grafico_1")

        # Gráfico 2: Boxplot de puntajes por predicción
        fig2 = px.box(
            df,
            x="prediccion",
            y="past_exam_scores",
            title="Notas Previas según la Predicción",
            color="prediccion",
            labels={
                "prediccion": "Predicción",
                "past_exam_scores": "Notas de Exámenes Anteriores"
            }
        )
        st.plotly_chart(fig2, use_container_width=True, key="grafico_2")

        # Gráfico 3: Dispersión asistencia vs horas de estudio
        fig3 = px.scatter(
            df,
            x="study_hours_per_week",
            y="attendance_rate",
            color="prediccion",
            size="past_exam_scores",
            title="Relación entre Asistencia y Horas de Estudio",
            labels={
                "study_hours_per_week": "Horas de Estudio por Semana",
                "attendance_rate": "Porcentaje de Asistencia",
                "prediccion": "Predicción",
                "past_exam_scores": "Notas de Exámenes Anteriores"
            }
        )
        st.plotly_chart(fig3, use_container_width=True, key="grafico_3")



