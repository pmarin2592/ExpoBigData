import os
import time

import pandas as pd
import psycopg2
from configparser import ConfigParser
from helpers.utilidades import Utilidades


class BaseDatos:
    def __init__(self):
        self.util = Utilidades()

    def _config(self, filename=os.path.abspath(os.path.join(os.path.dirname(__file__), '../config.ini')),
                section='postgresql'):
        parser = ConfigParser()
        parser.read(os.path.abspath(filename))

        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(f'Sección {section} no encontrada en el archivo {filename}')

        return db

    def _conectar(self,max_reintentos=20, espera_segundos=3):
        conn = None
        for intento in range(1, max_reintentos + 1):
            try:
                params = self._config()
                conn = psycopg2.connect(**params)
                print("✅ Conexión exitosa a PostgreSQL")
                return conn
            except (Exception, psycopg2.DatabaseError) as error:
                print(f"⚠️ Intento {intento}/{max_reintentos} fallido: {error}")
                if intento == max_reintentos:
                    print(
                        "❌ Error al conectar: connection to server at \"40.76.114.77\", port 5432 failed: Connection timed out (0x0000274C/10060)\n¿Está el servidor ejecutándose y aceptando conexiones TCP/IP?")
                    return None
                time.sleep(espera_segundos)  # Espera entre reintentos

    def obtener_df_modelo(self):
        conn = None
        cursor = None
        try:
            # Función que debes definir tú con tus datos de conexión
            conn = self._conectar()
            cursor = conn.cursor()

            # Consulta SQL
            query = """
                       SELECT student_id, gender, study_hours_per_week, attendance_rate, past_exam_scores, parental_education_level, 
                       internet_access_at_home, extracurricular_activities, final_exam_score, pass_fail
                        FROM cuc.student_performance;
                    """

            cursor.execute(query)
            resultados = cursor.fetchall()

            # Obtener nombres de columnas
            columnas = [desc[0] for desc in cursor.description]

            # Convertir a DataFrame
            df = pd.DataFrame(resultados, columns=columnas)
            return df

        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            print(f"Error al consultar la base de datos: {e.pgerror}")
            return None

        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error inesperado: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    def insertar_estudiante(self, estudiante):
        conn = None
        cursor = None
        try:
            conn = self._conectar()
            cursor = conn.cursor()

            query = """
                        INSERT INTO cuc.predicciones_estudiantes
                        (past_exam_scores, study_hours_per_week, attendance_rate, internet_access_at_home, 
                        extracurricular_activities, prediccion)
                        VALUES (%s, %s, %s, %s, %s, %s);
                    """

            cursor.execute(query, (
                estudiante.get_past_exam_scores(),
                estudiante.get_study_hours_per_week(),
                estudiante.get_attendance_rate(),
                estudiante.get_internet_access_at_home(),
                estudiante.get_extracurricular_activities(),
                estudiante.get_prediccion()
            ))

            conn.commit()
            print("Registro de estudiante insertado exitosamente.")

        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            print(f"Error al insertar el registro: {e.pgerror}")

        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error inesperado: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def obtener_df_analisis(self):
        conn = None
        cursor = None
        try:
            # Función que debes definir tú con tus datos de conexión
            conn = self._conectar()
            cursor = conn.cursor()

            # Consulta SQL
            query = """
                       SELECT id, past_exam_scores, study_hours_per_week, attendance_rate,
                        internet_access_at_home, extracurricular_activities, prediccion, fecha_creacion
                        FROM cuc.predicciones_estudiantes;
                    """

            cursor.execute(query)
            resultados = cursor.fetchall()

            # Obtener nombres de columnas
            columnas = [desc[0] for desc in cursor.description]

            # Convertir a DataFrame
            df = pd.DataFrame(resultados, columns=columnas)
            return df

        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            print(f"Error al consultar la base de datos: {e.pgerror}")
            return None

        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error inesperado: {e}")
            return None

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()