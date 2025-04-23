# ProyectoWebScraping
🧠 Análisis de Reseñas con Web Scraping, IA y Visualización en Power BI
🔎 Descripción del proyecto
En este proyecto he desarrollado una solución completa de análisis de reseñas públicas de Google Maps, combinando web scraping, procesamiento de lenguaje natural (NLP) con inteligencia artificial 
y visualización de datos en Power BI.
El objetivo principal es transformar las reseñas de los usuarios en insights accionables, que puedan ser utilizados por empresas, investigadores o gestores de marca para entender mejor la experiencia del cliente
y su percepción sobre un producto, servicio o establecimiento.

🛠️ Tecnologías utilizadas
    • Python + Selenium para automatizar la extracción de reseñas desde Google Maps.
    • ChatGPT (IA) para interpretar y calificar el sentimiento de cada reseña textual (positivo, neutro o negativo).
    • Pandas para estructurar y preparar los datos para análisis.
    • Power BI para visualizar los resultados de forma clara e interactiva.

🔁 Proceso automatizado
    1. Scraping de reseñas
A través de Selenium, el script navega automáticamente hasta Google Maps, busca el lugar indicado por el usuario y extrae todas las reseñas disponibles, incluyendo:
        ◦ El texto completo del comentario
        ◦ La valoración en estrellas otorgadas por el usuario
        ◦ La fecha de publicación de la reseña
    2. Análisis de sentimiento con IA
Cada comentario es enviado a un modelo de lenguaje (ChatGPT), que interpreta su contenido y devuelve una puntuación de sentimiento (por ejemplo, en una escala de -1 a +1 o categorizado como negativo, 
neutro o positivo). Esto permite identificar la emoción real del cliente más allá de la puntuación en estrellas.
    3. Almacenamiento y limpieza de datos
Se genera una base de datos estructurada que puede guardarse en CSV, Excel o en una base relacional, lista para análisis o visualización.
    4. Visualización en Power BI
Finalmente, los datos se cargan en Power BI,mediante una conexión OCDB donde se pueden explorar a través de:
        ◦ Gráficos de distribución de sentimientos
        ◦ Comparativas entre estrellas y análisis semántico
        ◦ Evolución temporal de opiniones
        ◦ Palabras clave más repetidas, entre otros

📊 Valor añadido
Este proyecto es un ejemplo práctico de cómo automatizar la minería de opiniones públicas, enriquecerlas mediante IA y convertirlas en conocimiento visual.
Se puede adaptar fácilmente para múltiples ubicaciones o sectores, y escalar para análisis de reputación online o benchmarking competitivo.



🤖 Análisis de sentimiento con ChatGPT
Para cada reseña textual extraída de Google Maps, se realiza un análisis semántico utilizando ChatGPT, que interpreta el contenido del mensaje más allá de las estrellas otorgadas.
Este modelo de lenguaje clasifica cada reseña en una escala de sentimiento:
    • Positivo
    • Neutro
    • Negativo
El proceso se puede ajustar para generar también una puntuación numérica personalizada (por ejemplo, de -1 a +1), o extraer directamente emociones específicas (como frustración, satisfacción, etc.).
El análisis permite responder preguntas como:
    • ¿Coincide la puntuación de estrellas con el sentimiento real expresado?
    • ¿Qué porcentaje de reseñas positivas están acompañadas de críticas implícitas?
    • ¿Cómo varía el sentimiento con el tiempo?
Este tipo de enriquecimiento semántico mejora significativamente la capacidad de interpretación de los datos en comparación con un análisis basado únicamente en puntuaciones numéricas.
