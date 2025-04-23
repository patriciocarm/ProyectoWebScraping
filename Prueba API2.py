# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 08:08:05 2025

@author: rportatil115
"""

import os
import sqlite3
from dotenv import load_dotenv
from openai import OpenAI
import sys

sys.path.append(r"C:\Users\rportatil115\Desktop\PROYECTO IA+PYTHON+POWER BI")
from proyectoguapo import obtener_reseñas

# Cargar variables del entorno
os.chdir(r"C:\Users\rportatil115\Desktop\PROYECTO IA+PYTHON+POWER BI")
load_dotenv(dotenv_path=".env")
api_key = os.getenv("OPENAI_API_KEY")

# Obtener las reseñas (esperadas como lista de diccionarios)
reseñas = obtener_reseñas()

# Crear una conexión a la base de datos SQLite
db_path = r"C:\Users\rportatil115\Desktop\WebScraping\BBDD\reseñas_analizadas.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
    DELETE FROM ReseñasAnalizadas;
''')
cursor.execute('''
    DELETE FROM sqlite_sequence WHERE name='ReseñasAnalizadas';
''')

# Crear tabla con tipo DECIMAL explícito
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ReseñasAnalizadas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        texto TEXT,
        puntuacion DECIMAL(3,2)  -- Formato específico: 3 dígitos totales, 2 decimales
    )
''')


if api_key:
    client = OpenAI(api_key=api_key)

    # Convertir cada reseña en un texto formateado para el prompt
    reseñas_formateadas = [
        f'{r["texto"]}. Estrellas: {r["estrellas"]}. Fecha: {r["fecha"]}'
        for r in reseñas
    ]
    reseñas_prompt = "\n".join(reseñas_formateadas)

    # Enviar a OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": f"""Eres un analista de sentimientos experto en evaluar reseñas de usuarios considerando tres elementos: el texto de la reseña, la fecha en que fue escrita y la puntuación en estrellas (de 1 a 5).

Tu tarea es asignar a cada reseña una puntuación emocional entre -1 (muy negativa) y 1 (muy positiva), teniendo en cuenta matices, contexto, antigüedad del comentario y su coherencia con las estrellas asignadas por el usuario.

Solo debes devolver la puntuación emocional numérica de cada reseña, una por línea, sin texto adicional ni explicaciones. 

-1 El sitio es un desastre total. El café estaba frío, el baño sucio y el camarero nos trató fatal. No volveré nunca.
-0.95 Servicio pésimo y tardaron más de 30 minutos en traerme un café. Inaceptable.
-0.85 El lugar es muy ruidoso, apenas se puede hablar. El café regular y los precios altos.
-0.75 Pedí un café con leche y me trajeron uno solo, mal atendido y sin ganas de trabajar.
-0.60 No me gustó. El trato fue seco y el café estaba quemado.
-0.40 Café mediocre, nada especial. El sitio es bonito pero no compensa.
-0.25 No estuvo tan mal, pero tampoco lo recomendaría. Nada destacable.
-0.10 Café correcto, pero el lugar estaba vacío y sin ambiente.
0.00 Lugar promedio. El café está bien, ni bueno ni malo. Servicio neutral.
0.10 Me gustó el ambiente, pero el café era muy básico.
0.25 Servicio decente y el local es agradable, aunque la calidad del café no destaca.
0.40 Buena atención y café aceptable. Le falta mejorar el espacio.
0.55 Todo correcto. Buen trato y café normalito.
0.65 Buen lugar para trabajar tranquilo. El café está bastante bien.
0.75 El personal fue amable y el café tenía buen sabor.
0.80 Me gustó la experiencia en general. Buen café y música agradable.
0.88 Buena vibra, excelente trato y productos de calidad. Repetiré.
0.95 Sitio espectacular. Buen café, ambiente acogedor y atención impecable.
1.00 Increíble experiencia. Mejor café de la ciudad, atención de 10 y música perfecta.

Lista de reseñas a analizar (una por línea con formato "Texto. Estrellas: X. Fecha: hace x años/meses/días"):
{reseñas_prompt}
"""
        }]
    )

    # Separar cada línea devuelta como puntuación
    resultados = response.choices[0].message.content.strip().splitlines()

    # Verificar que las longitudes coincidan
    min_length = min(len(reseñas), len(resultados))

    for i in range(min_length):
        try:
            puntuacion = resultados[i].strip()
            puntuacion_float = round(float(puntuacion), 2)
            puntuacion_float = max(-1.0, min(1.0, puntuacion_float))
            puntuacion_str = f"{puntuacion_float:.2f}"

            cursor.execute(
                "INSERT INTO ReseñasAnalizadas (texto, puntuacion) VALUES (?, ?)",
                (reseñas[i]["texto"], puntuacion_str)
            )

            print(f"✅ Reseña procesada correctamente:")
            print(f"Texto: {reseñas[i]['texto']}")
            print(f"Puntuación: {puntuacion_str}")

        except ValueError as e:
            print(f"❌ Error en formato: {resultados[i]} - {str(e)}")
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")

    conn.commit()
    conn.close()

else:
    print("❌ No se cargó la API key. Revisa el archivo .env.")
