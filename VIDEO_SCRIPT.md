# 🎬 Guion de Video de Demostración (3 a 4 Minutos)
## Actividad Grupal 01: Visualization Reports or Dashboard
### Proyecto: Paracas Renewable Wind & Solar Energy Explorer

Este guion está optimizado para que grabes tu pantalla (usando **OBS Studio**, **Loom**, o **Clipchamp**) en **menos de 5 minutos** (duración estimada: 3:45 min), cumpliendo al 100% con los requisitos de la actividad.

---

## ⏱️ Estructura y Tiempos del Video

| Minuto | Escena / Pantalla a Mostrar | Qué decir (Voz en off / Audio) |
| :--- | :--- | :--- |
| **0:00 - 0:40** | **Portada y Contexto:**<br>Mostrar el artículo en Dev.to o el `README.md` del repositorio. | *"Hola a todos. En este video voy a presentar la construcción y despliegue automatizado de nuestro dashboard interactivo: **Paracas Renewable Wind & Solar Energy Explorer**.<br>Tomando como base científica los datos satelitales y de reanálisis atmosférico de la **NASA POWER**, este proyecto analiza 5 años de observaciones diarias (2020 a 2024) en el corredor eólico de Paracas y Pisco, en Ica, Perú, para evaluar la complementariedad entre la energía solar y los vientos costeros."* |
| **0:40 - 1:15** | **Estructura del Proyecto:**<br>Mostrar VS Code con las carpetas: `app.py`, `data/`, `.github/workflows/ci.yml`, `.streamlit/`. | *"La arquitectura está diseñada bajo principios de reproducibilidad y GitOps:<br>- Desarrollado en **puro Python** con **Streamlit** y **Plotly**.<br>- Un dataset histórico curado de 1,827 días en `data/paracas_renewable_daily.csv` y sus metadatos.<br>- Un pipeline de integración continua con **GitHub Actions** en `.github/workflows/ci.yml`.<br>- Y despliegue automatizado en la nube SaaS pública a través de **Streamlit Community Cloud**."* |
| **1:15 - 2:35** | **Demostración en Vivo del Dashboard:**<br>Mostrar la aplicación corriendo en el navegador (local o en la nube). | *"Veamos la aplicación en vivo:<br>1. **KPI Scorecards:** En la parte superior vemos la velocidad promedio del viento a 50 metros de altura de buje (más de 6 m/s), la radiación solar diaria (~6.2 kWh/m²/día), la densidad de potencia eólica y el factor de planta híbrido.<br>2. **Series de Tiempo y Estacionalidad:** En la primera pestaña observamos la evolución diaria y la media móvil a 14 días, junto a diagramas de cajas mensuales.<br>3. **Rosa de los Vientos y Distribución Weibull:** Aquí en la segunda pestaña vemos la dirección predominante: más del 70% de la energía eólica proviene del Sur-Suroeste (180° a 210°), con su ajuste probabilístico de Weibull.<br>4. **Complementariedad Eólica-Solar:** En esta matriz demostramos cómo en los meses de invierno, cuando baja la radiación solar, los vientos térmicos de Paracas se intensifican, estabilizando el suministro.<br>5. **Simulador de Planta Híbrida:** Podemos ajustar la capacidad en megavatios (por ejemplo, 50 MW eólicos y 30 MW solares) y el modelo calcula la generación diaria en MWh y las toneladas de CO₂ evitadas a la red peruana."* |
| **2:35 - 3:20** | **Automatización CI/CD con GitHub Actions:**<br>Mostrar la pestaña **Actions** en tu repositorio de GitHub con el check verde ✅. | *"El segundo requisito clave es el despliegue mediante automatización.<br>En la pestaña **Actions** de GitHub vemos nuestro workflow `ci.yml`. En cada `push` o `pull request`:<br>1. Valida el código con el linter **Flake8** para evitar errores de sintaxis.<br>2. Verifica la integridad del dataset de la NASA.<br>3. Ejecuta una prueba de compilación del módulo `app.py`.<br>4. Lanza Streamlit en modo headless para garantizar que no haya excepciones al arrancar el servidor en producción."* |
| **3:20 - 3:45** | **Despliegue Continuo en la Nube SaaS:**<br>Mostrar Streamlit Community Cloud (`share.streamlit.io`) y la URL pública `paracas-renewable-energy-explorer.streamlit.app`. | *"Por último, el dashboard está publicado en una plataforma SaaS pública: **Streamlit Community Cloud**.<br>Gracias a la integración con GitHub, cualquier cambio en la rama `main` pasa las pruebas automáticas y se actualiza en vivo en cuestión de segundos con HTTPS y disponibilidad global."* |
| **3:45 - 4:00** | **Cierre:**<br>Mostrar la tabla de enlaces del `README.md` o el artículo de Dev.to. | *"El repositorio público, el workflow de CI/CD y el enlace en vivo están disponibles en la descripción del video y en nuestro artículo publicado en Dev.to. Muchas gracias por su atención."* |

---

## 💡 Consejos Prácticos para Grabar el Video

1. **Herramienta recomendada:**
   - **Windows:** Presiona `Windows + Alt + R` para grabar la pantalla directamente con la barra de juegos de Windows, o usa **Loom** (gratuito desde el navegador o extensión de Chrome).
   - O descarga **OBS Studio** para mayor control.
2. **Audio claro:** Usa tus auriculares o micrófono manos libres para que el audio se escuche nítido.
3. **Subida:** Sube el video a **YouTube** (puedes ponerlo como *No listado* o *Público*), copia el enlace y pégalo en el artículo y en la entrega grupal.
