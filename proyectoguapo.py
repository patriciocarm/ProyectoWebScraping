# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 12:49:59 2025

@author: rportatil115
"""

# 📦 Importación de librerías necesarias
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 🧠 Función principal que obtiene reseñas de un lugar en Google Maps
def obtener_reseñas():
    # ✅ Se solicita al usuario el nombre de la empresa o lugar
    empresa = input("¿Qué empresa o sitio quieres su reseña (recuerda poner el lugar)? ")

    # ⚙️ Configuración del navegador (modo privado, pantalla completa, etc.)
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--inprivate")
    options.add_argument("start-maximized")

    # 🧭 Ruta del driver de Edge
    service = Service(r"C:\Users\rportatil115\Desktop\PROYECTO IA+PYTHON+POWER BI\msedgedriver.exe")
    driver = webdriver.Edge(service=service, options=options)

    # 🌍 Abre Google Maps en una vista inicial
    driver.get("https://www.google.es/maps/@39.849787,-4.2468073,939812m/data=!3m1!1e3?hl=es&entry=ttu")

    # 🍪 Intenta cerrar el banner de cookies si aparece
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[jsname="tWT92d"]'))).click()
    except:
        pass  # Si no aparece, continúa

    # 🔍 Busca la empresa introducida por el usuario
    cuadro_texto = driver.find_element(By.ID, "searchboxinput")
    cuadro_texto.click()
    time.sleep(1)
    cuadro_texto.send_keys(empresa)
    time.sleep(1)
    cuadro_texto.send_keys(Keys.ENTER)
    time.sleep(3)

    # 🧷 Intenta hacer clic en el botón de reseñas
    try:
        reseñas_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[.//div[contains(text(), "Reseñas")]]'))
        )
        reseñas_btn.click()
        time.sleep(2)
    except:
        # 🛠 Si no lo encuentra, intenta otra ruta alternativa
        try:
            primer_div = driver.find_element(By.CLASS_NAME, "hfpxzc")
            primer_div.click()
            time.sleep(2)
            reseñas_btn = driver.find_element(By.XPATH, '//button[.//div[contains(text(), "Reseñas")]]')
            reseñas_btn.click()
            time.sleep(3)
        except:
            print("No se pudieron encontrar reseñas.")
            driver.quit()
            return []

    # ⏳ Espera hasta que aparezca el botón "Ordenar"
    wait = WebDriverWait(driver, 10)
    ordenar_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[contains(text(), 'Ordenar') or contains(text(), 'Sort')]")
    ))
    ordenar_btn.click()
    time.sleep(1.5)

    # 🆕 Clic en la opción "Más recientes"
    mas_recientes = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Más recientes') or contains(text(), 'Newest')]")))
    driver.execute_script("arguments[0].click();", mas_recientes)
    time.sleep(2)

    # ⬇️ Scroll manual dentro del contenedor de reseñas
    scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div[class="m6QErb DxyBCb kA9KIf dS8AEf XiKgde "]')
    last_height = driver.execute_script('return arguments[0].scrollHeight', scrollable_div)

    while True:
        driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight);', scrollable_div)
        time.sleep(2)
        new_height = driver.execute_script('return arguments[0].scrollHeight', scrollable_div)
        if new_height == last_height:
            break
        last_height = new_height

    # ➕ Expande los comentarios truncados ("Ver más")
    for btn in scrollable_div.find_elements(By.CSS_SELECTOR, 'button[class*="w8nwRe"]'):
        try:
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.3)
        except:
            continue

    # 📌 Obtiene todas las reseñas del contenedor (solo reseñas reales, sin respuestas del dueño)
    divs_reseñas = scrollable_div.find_elements(By.CSS_SELECTOR, 'div.jftiEf.fontBodyMedium')

    lista_reseñas = []
    for reseña in divs_reseñas:
        # ❌ Omitir reseñas del propietario
        try:
            respuesta_dueño = reseña.find_element(By.CSS_SELECTOR, 'div.CDe7pd')
            if respuesta_dueño:
                continue
        except:
            pass

        # 💬 Obtener texto de la reseña
        try:
            comentario = reseña.find_element(By.CLASS_NAME, "wiI7pd").text.strip()
        except:
            comentario = "Sin comentario"

        # ⭐ Obtener número de estrellas
        try:
            estrellas_elem = reseña.find_element(By.CSS_SELECTOR, 'span.kvMYJc')
            estrellas = estrellas_elem.get_attribute("aria-label").strip()
        except:
            estrellas = "Sin estrellas"

        # 📅 Obtener fecha de la reseña
        try:
            fecha_elem = reseña.find_element(By.CSS_SELECTOR, 'span.rsqaWe')
            fecha = fecha_elem.text.strip()
        except:
            fecha = "Sin fecha"

        # 📦 Guardar la reseña como diccionario
        lista_reseñas.append({
            "texto": f"[{estrellas}] ({fecha}) → {comentario}",
            "estrellas": estrellas,
            "fecha": fecha,
            "comentario": comentario
        })

    # 🔚 Cierra el navegador y devuelve las reseñas recopiladas
    driver.quit()
    return lista_reseñas

# 🔁 Bloque para probar la función si se ejecuta directamente el script
if __name__ == "__main__":
    comentarios = obtener_reseñas()
    for idx, texto in enumerate(comentarios, 1):
        print(f"{idx}. {texto}")
