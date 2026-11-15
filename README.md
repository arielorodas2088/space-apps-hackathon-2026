# Simulador de Misiones Espaciales

Juego de navegador para diseñar y simular una misión espacial a cualquier cuerpo del sistema solar. Hecho para el desafío **Space Mission Design Game** de NASA Space Apps Challenge 2026.

> Estado: prototipo. Los costos, masas y potencias son **estimaciones de juego**; ver `docs/documento_proyecto.pdf` (secciones 7 y 14) y `assets/curated/sources.csv`.

## Probarlo en local
Abrí `index.html` con el navegador. No hace falta instalar nada.

## Datos reales de NASA/JPL
El juego usa cuatro fuentes (verificadas el 15/11/2026):

| Fuente | Qué cambia en el juego |
|---|---|
| JPL Horizons | Distancia real de hoy a cada destino y retraso de señal |
| NASA DONKI (CCMC) | Clima espacial de los últimos 30 días: decide si aparece la tormenta solar y qué tan fuerte pega |
| JPL Small-Body Mission Design | Ventana de lanzamiento real a Bennu y su dificultad energética (v∞) |
| NASA NeoWs + Mission Design | Un destino extra: el asteroide cercano más grande de la semana |

Cómo llegan los datos al navegador (el navegador nunca llama a NASA directo: JPL no permite CORS y la DEMO_KEY tiene un límite de 10 llamadas por hora):
1. **En Vercel:** la función `api/live-data.py` consulta las APIs y Vercel cachea la respuesta 6 h. Opcional: cargar una clave gratuita de api.nasa.gov como variable de entorno `NASA_API_KEY` (si falta, usa `DEMO_KEY`).
2. **Respaldo:** `assets/live-data.js`, una copia guardada. Para actualizarla:
   ```
   python tools/fetch_data.py
   ```
3. Si no hay ninguna de las dos, el juego usa valores de referencia. Arriba de la pantalla siempre dice de dónde salen los datos.

La lógica de consulta está en `api/_live.py` (solo biblioteca estándar de Python).

## Documento del proyecto
Fuente editable: `docs/documento_proyecto.md`. Para regenerar el PDF:
```
pip install reportlab
python tools/build_pdf.py
```

## Subirlo a GitHub
```
git init
git add .
git commit -m "Primera versión"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```
Para publicarlo: Settings > Pages > rama `main`, carpeta raíz. GitHub Pages no ejecuta la función de `api/`, así que ahí el juego usa la copia guardada (`assets/live-data.js`).

## Licencia
MIT (ver `LICENSE`); completá el nombre del equipo.

## Rediseño visual y mejoras de jugabilidad (DRACO: MISIÓN 500)
- Interfaz espacial oscura con paneles HUD, tarjetas interactivas y diseño adaptable a móvil.
- La portada original de DRACO se conserva como identidad visual del simulador (`assets/portada-draco.jpg`).
- Presupuesto ampliado por dificultad: 1.800 créditos (Fácil), 2.400 (Normal) y 3.200 (Experto), más bonificación según destino. Son valores de balance del juego.
- Selector de trayectoria: automática, segura, rápida o científica; cada ruta tiene costo y perfil de riesgo.
- Controles adaptables: flechas del teclado en computadora y cruceta táctil en celular/tableta; diseño responsive.
- Duración diferenciada por destino: Luna 28 s, Venus 95 s, Marte 120 s, Bennu 145 s, Europa 255 s, Titán 340 s y Neptuno 480 s. Marte es la referencia de dos minutos; los demás tiempos son escalas comprimidas de jugabilidad.
- Distancia de cada misión variable entre partidas, dentro de rangos orbitales de referencia; estos rangos son aproximaciones de juego y no efemérides exactas en tiempo real.
- Vuelo continuo con seguimiento de corredor, indicador de desviación, controles de teclado y cruceta táctil para celulares y tabletas, además de alertas anticipadas de obstáculos.
- Respuestas ante riesgos: desvío de trayectoria, activación de blindaje o continuar asumiendo el riesgo. La nave no se detiene durante el crucero; la detención solo corresponde a un aterrizaje completado.
- Las maniobras ya no se agotan tras cuatro acciones: se puede corregir el vuelo durante la simulación.

Nota: la escena de vuelo usa una representación 2.5D ligera hecha con CSS para funcionar sin instalar motores ni descargar librerías. No es todavía una simulación orbital 3D física como Kerbal Space Program; es una mejora de interfaz y dinámica del prototipo web.


## Publicar y compartir el juego

El proyecto es estático (HTML, CSS y JavaScript), por lo que puede alojarse gratis sin servidor. Para obtener un enlace público: 

1. Descomprimí el ZIP.
2. Abrí https://app.netlify.com/drop desde una computadora e iniciá sesión o creá una cuenta gratuita.
3. Arrastrá la carpeta `repo` descomprimida (debe contener `index.html` y la carpeta `assets`; Netlify Drop no ejecuta `api/`, así que usa la copia guardada de los datos).
4. Netlify publicará el sitio y mostrará una dirección `https://...netlify.app` para compartir.

Alternativa: GitHub Pages, siguiendo la sección anterior. No se incluye un enlace público ya publicado porque requiere que el propietario del juego autorice la publicación en una cuenta de hosting.
