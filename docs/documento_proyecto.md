# Simulador de Misiones Espaciales

## Documento de proyecto: desafío “Space Mission Design Game”, NASA Space Apps Challenge 2026

Equipo: [COMPLETAR] · Integrantes: [COMPLETAR] · Evento local: [COMPLETAR] · Repositorio: [COMPLETAR] · Video: [COMPLETAR]

Fecha: 14 de noviembre de 2026 · Versión: borrador 0.1

**Cómo leer este documento.** [COMPLETAR] marca datos que solo el equipo puede aportar. Cada capacidad figura como **Hecho**, **Parcial** o **Pendiente**. Cada dato figura como **verificado** (comprobado en la fuente indicada el 14/11/2026), **por verificar** o **estimación de juego** (número inventado o simplificado para poder jugar). Este documento prefiere decir lo que falta antes que prometer de más.

## 1. Resumen ejecutivo

Es un juego de navegador en español donde una persona, o un equipo de hasta cuatro, diseña una misión espacial a un cuerpo celeste del sistema solar con un presupuesto escalonado y ampliado (1.800 a 3.200 créditos, más bonificaciones por destino). Elige destino, órbita, cohete, nave, instrumentos, equipo de superficie y tripulación; una revisión previa al vuelo valida masa, energía, datos y comunicaciones; después sigue un corredor de vuelo con controles direccionales, corrige el rumbo y enfrenta eventos y recibe un reporte que explica por qué la misión salió bien o mal.

Estado real: hay un prototipo jugable con 7 destinos, 6 recursos y un reporte de causas. Los números de costo, masa y potencia son **estimaciones de juego**, todavía sin contrastar con fuentes. Hay una tubería para traer datos reales del JPL (distancia y retraso de señal) que **no fue probada** contra el servidor. No hicimos pruebas con usuarios. La competencia dentro de este mismo desafío ya es amplia (sección 11), por lo que nuestra diferenciación debe sostenerse en pocos puntos claros (sección 12).

## 2. Cumplimiento del track

| Requisito del desafío | Estado | Evidencia | Brecha |
|---|---|---|---|
| Definir objetivo y requisitos de la misión | Parcial | Cada destino fija un objetivo de ciencia mínimo | Requisitos no editables; un solo tipo de objetivo |
| Diseñar nave y carga científica | Parcial | Bus, energía, antenas, instrumentos, tripulación | Sin baterías, control de actitud ni computadora de a bordo |
| Elegir lanzador y órbita con chequeo de compatibilidad | Hecho (simplificado) | Revisión masa contra capacidad según destino y órbita | Sin curvas reales de carga útil |
| Gestionar presupuesto, masa, energía, comunicaciones, datos y duración | Parcial | Seis recursos con barras en vivo | Modelos lineales; sin eclipses ni degradación |
| Simular y evaluar la misión | Parcial | Cuatro maniobras, inserción, eventos, puntaje | Dinámica orbital abstracta |
| Explicar por qué se gana o se pierde | Hecho | Revisión previa con “por qué” y reporte de causas | Falta tutorial guiado |
| Jugador individual y equipo de hasta 4 | Parcial | Roles por turnos en un mismo dispositivo | No hay multijugador en red |
| Sistema de puntaje | Parcial | Fórmula con ciencia, ahorro, estrellas y precisión | Sin calibrar |
| Escenarios, dificultad y sandbox | Hecho | 7 destinos, 3 niveles, sandbox | Europa, Titán y Neptuno casi no se ganan (ver 14) |
| Eventos aleatorios | Parcial | Alertas específicas por destino con alternativas de respuesta | Todavía no usan clima espacial real |
| Dashboard en tiempo real | Parcial | Barras durante diseño y vuelo | Sin consumo a lo largo del tiempo |
| Visualización de la nave | Pendiente | Ninguna | Es una brecha visible frente a otros equipos |
| Guardar, compartir y comparar diseños | Pendiente | Ninguna | Códigos de diseño compartibles |
| Ranking | Parcial | Local en cada dispositivo | No hay ranking global |
| Modo competitivo | Pendiente | Ninguna | Mismo objetivo, equipos distintos |
| Uso de datos reales de NASA | Parcial | Retraso de señal vía JPL Horizons (script sin probar) | El resto son estimaciones |

## 3. Problema, público y objetivos de aprendizaje

**Problema.** Según el desafío, los estudiantes rara vez experimentan una misión completa de principio a fin y las herramientas existentes tratan temas sueltos (órbitas, naves o lanzamientos) sin mostrar cómo interactúan. Sin esa visión de sistema, los trade-offs quedan abstractos.

**Público.** Estudiantes de secundaria y universitarios, clubes de ciencia y docentes de habla hispana, sin conocimientos previos de ingeniería aeroespacial.

**Objetivos de aprendizaje.** Al terminar, la persona puede: (1) explicar por qué un destino más lejano exige más masa, energía y capacidad de comunicación; (2) identificar qué recurso limita su misión; (3) comparar dos diseños que cumplen el mismo objetivo; (4) justificar una reserva presupuestaria. Medición propuesta: cuestionario de 5 preguntas antes y después de jugar [COMPLETAR resultados].

## 4. Diseño de juego

**Flujo.** Diseño (6 menús) → revisión previa al vuelo → vuelo continuo con seguimiento de corredor y correcciones direccionales → resolución de incidentes → inserción o aterrizaje → reporte → rediseño.

**Menús y precios (estimaciones de juego).** Destinos: Luna 50, Venus 150, Marte 180, asteroide Bennu 130, Europa 320, Titán 380, Neptuno 400. Órbita: baja 0, elíptica 10, polar 20, aterrizaje 40. Duración: 6 meses 0, 12 meses 15, 24 meses 35. Cohetes: Tronador II 80, Falcon 9 150, Saturn V 200, SLS 240. Bus: simple 25, avanzado 60. Además hay 23 ítems entre energía, comunicaciones, soporte, instrumentos, vehículos de superficie y tripulación (ver `index.html`).

**Equipos.** Con 2 a 4 jugadores se reparten cuatro roles: Planificador (destino, órbita, tiempo), Ingeniero (cohete, nave), Científico (instrumentos) y Logística (superficie y tripulación). Cada uno decide solo en su área y todos deben confirmar antes de lanzar.

**Dificultad.** Fácil (1.800 créditos, explicaciones en cada chequeo, tolerancias amplias), Normal (2.400) y Experto (3.200, más eventos y tolerancias estrictas). Se agregan bonificaciones por destino para que las misiones lejanas puedan equiparse sin recurrir obligatoriamente al sandbox. Sandbox sin límite de crédito.

**Reglas pedagógicas.** Nunca hay una única solución: el mismo destino se alcanza con combinaciones distintas. La reserva de 50 créditos o más da una estrella, porque un recorte presupuestario sin reserva reduce la ciencia.

**Ejemplos resueltos (cálculo manual con las reglas del juego).**

| Misión | Diseño | Costo | Resultado esperado |
|---|---|---|---|
| Luna, mínima | Aterrizaje, Tronador II, bus simple, 1 panel, antena básica, cámara óptica, 12 meses | 280 | Masa 2,9 t de 6,4 t; energía 2,2 de 3 kW; ciencia 11,2 de 10 |
| Marte, ajustada | Órbita elíptica, Tronador II, bus simple, 2 paneles, antena básica, espectrómetro, 12 meses | 450 | Masa 3,8 t de 3,83 t; energía 2,5 de 2,58 kW; ciencia 16 de 14 |

La misión a Marte funciona con un margen mínimo de masa y energía: ese es justamente el aprendizaje. Estos resultados deben confirmarse jugando.

### Tiempos y distancias de vuelo (escala de juego)

Cada partida sortea una distancia dentro de un rango orientativo y usa una duración propia. La distancia real entre cuerpos cambia con sus órbitas; estos rangos son referencias de jugabilidad, no una efeméride JPL consultada en el instante de lanzamiento. Marte conserva los 120 segundos como referencia. Luna: 28 s; Venus: 95 s; Marte: 120 s; Bennu: 145 s; Europa: 255 s; Titán: 340 s; Neptuno: 480 s. Los tiempos están comprimidos y no representan el tiempo real de transferencia interplanetaria.

| Destino | Rango de distancia orientativo | Duración de juego |
|---|---:|---:|
| Luna | 363.000–406.000 km | 28 s |
| Venus | 38–261 millones km | 95 s |
| Marte | 55–401 millones km | 120 s |
| Bennu | 15–300 millones km | 145 s |
| Europa | 588–968 millones km | 255 s |
| Titán | 1.200–1.700 millones km | 340 s |
| Neptuno | 4.300–4.700 millones km | 480 s |

### Control de vuelo y eventos

La nave avanza de manera continua. Las flechas izquierda/derecha modifican el rumbo y arriba/abajo corrigen la posición lateral respecto del corredor. En dispositivos táctiles se usa la cruceta en pantalla. El jugador puede cambiar de trayectoria durante el vuelo; el corredor objetivo cambia sin detener la nave. En tres momentos de la misión aparecen alertas anticipadas con alternativas: desvío, blindaje o asumir el riesgo. La inserción orbital se habilita al completar el tiempo de viaje; el aterrizaje solo detiene la nave cuando se confirma la maniobra de superficie.

## 5. Modelo de misión

| Variable | Modelo actual (juego) | Modelo realista que lo reemplazaría |
|---|---|---|
| Costo | C = destino + órbita + cohete + bus + duración + suma de ítems ≤ presupuesto | Modelos paramétricos de costo de misión (por masa y complejidad) [COMPLETAR fuente] |
| Masa | m = m_bus + suma de masas ≤ capacidad del cohete / (energía del destino × energía de la órbita) | Curva de carga útil contra C3 por lanzador |
| Energía | Generación = suma de paneles × factor solar; el RTG no depende del Sol; consumo = bus + ítems | Flujo solar S = S0 / r² (r en UA, S0 ≈ 1361 W/m² a 1 UA, por verificar) con eficiencia, eclipses y batería |
| Datos | Capacidad = tasa de las antenas × 10 / factor de distancia; la IA reduce 30 % los datos | Presupuesto de enlace (potencia, ganancia, distancia², frecuencia) |
| Retraso de señal | Tabla o valor de JPL Horizons | t = d / c, con c = 299 792,458 km/s (1 UA ≈ 499 s) |
| Δv y combustible | Combustible abstracto por cohete | Tsiolkovsky: Δv = Isp · g0 · ln(m0 / mf), g0 = 9,80665 m/s² |
| Inserción | Tolerancia en velocidad y ángulo según destino, órbita y piloto | Maniobras de inserción con arco gravitatorio del cuerpo |
| Ciencia | S = suma de valores × factor de órbita × bus × duración × astrobiólogo | Valor científico por instrumento según requisitos de la misión |
| Puntaje | 50 · min(ciencia/objetivo, 1,5) + 20 · reserva/presupuesto + 5 · estrellas + 10 · precisión + 2 · maniobras sobrantes | Pesos a calibrar con pruebas |

Los factores de energía por destino (1 a 5), la capacidad de los cohetes y los precios son **estimaciones de juego**. La fila “modelo realista” es la hoja de ruta para ganar validez científica.

## 6. Validación del modelo

Plan: elegir tres misiones reales de referencia (candidatas: MAVEN a Marte, OSIRIS-REx a Bennu y Europa Clipper), cargar su masa, instrumentos, potencia, lanzador y costo públicos, y comparar con lo que el juego considera factible. Tabla a completar:

| Misión real | Masa real | Potencia real | Lanzador | Costo público | ¿El juego la acepta? | Desvío |
|---|---|---|---|---|---|---|
| [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] | [COMPLETAR] |

Resultado hasta hoy: **no realizado**.

## 7. Datos y APIs

**Principio.** El navegador del jugador nunca llama a las APIs de NASA. Un script programado descarga los datos, los guarda como archivo estático (`data/live-data.js` y `.json`) y el juego los lee. Así se respetan los límites de uso, el juego funciona sin conexión y siempre muestra la fecha de actualización. Si el archivo falta, el juego usa valores de referencia y lo indica en pantalla.

| Fuente | Dato útil | Acceso | Estado | Uso |
|---|---|---|---|---|
| JPL Horizons API | Distancia, luz-tiempo y velocidad de planetas, lunas y asteroides | GET `https://ssd.jpl.nasa.gov/api/horizons.api`, sin clave | Documentación verificada; script sin probar | Retraso de señal; a futuro Δv y ventanas |
| Horizons Lookup API | Identificadores de cuerpos | GET `.../horizons_lookup.api?sstr=` | Documentación verificada | Confirmar el ID de Bennu (2101955, por verificar) |
| SBDB, SBDB Query y Close-Approach | Órbitas y parámetros de asteroides y cometas | `https://ssd-api.jpl.nasa.gov/sbdb.api` | Documentación verificada | Escenarios con asteroides |
| Small-Body Mission Design (JPL) | Datos para diseño rápido de misiones a cuerpos menores | `https://ssd.jpl.nasa.gov/sb` | Listado verificado | Δv a Bennu |
| DONKI (CCMC) | Fulguraciones, eyecciones de masa coronal, tormentas | `https://ccmc.gsfc.nasa.gov/DONKI-API/get/`, sin clave, máximo 30 días | **Migró el 30/09/2026** desde api.nasa.gov según dos proyectos de terceros; ruta exacta por verificar | Eventos de tormenta solar reales |
| Launch Library 2 | Lanzadores y lanzamientos | `https://thespacedevs.com/llapi`; 15 llamadas por hora sin clave | Límite verificado; campos de capacidad y costo por verificar | Catálogo de cohetes con caché |
| DSN Now | Estado de enlaces con naves | `https://eyes.nasa.gov/dsn/data/dsn.xml` | La página avisaba mantenimiento al consultarla | Opcional |
| APOD | Imagen astronómica del día | El endpoint antiguo de api.nasa.gov se apaga el 01/12/2026; el nuevo está en science.nasa.gov (fuente de terceros) | Por verificar | Decorativo |
| Biblioteca de imágenes de NASA | Fotos de destinos | `https://images-api.nasa.gov` | Sin clave (fuente de terceros) | Ilustrar destinos |
| NASA Exoplanet Archive | Exoplanetas | TAP/API | Por verificar | Modo avanzado |
| Fichas planetarias (NSSDCA), elementos keplerianos (JPL), PDS, fichas de misiones | Gravedad, radio, velocidad de escape; masas y potencias reales | Páginas y archivos | Por verificar | Tabla curada (ver abajo) |
| Pestaña Resources del desafío | Datos oficiales del track | Sitio del desafío | **No se pudo abrir** (bloquea acceso automático) | [COMPLETAR: revisar a mano] |

**Corrección.** En una versión previa de este análisis se recomendaba DONKI vía api.nasa.gov con clave de demostración. Eso quedó desactualizado por la migración a CCMC.

**Datos curados.** No existe API para costos de misión ni para especificaciones de instrumentos. Se mantienen en `data/curated/sources.csv`, con valor del juego, valor real, fuente, fecha y un estado (`estimacion_juego` o `verificado`). Cada vez que se contraste un dato, se cambia su estado. Esa trazabilidad responde al criterio de validez.

## 8. Arquitectura técnica

Aplicación de una sola página sin dependencias (`index.html`), que lee `data/live-data.js`. Funciona abriendo el archivo en el navegador. Estructura del repositorio: `index.html`, `data/` (datos en vivo y curados), `tools/fetch_data.py` (descarga), `tools/build_pdf.py` (genera este documento), `docs/`, `.github/workflows/update-data.yml` (ejecuta la descarga cada día). Para publicar: GitHub Pages desde la rama principal. Estado: el flujo de actualización automática **no fue probado**.

## 9. Experiencia de usuario y accesibilidad

Hecho: diseño adaptable a celular, tema claro y oscuro, foco visible de teclado, controles operables con botones nativos. Pendiente: auditoría de accesibilidad, prueba con lector de pantalla, contraste verificado con herramienta, tutorial inicial, versión en inglés, tamaño de objetivos táctiles revisado.

## 10. Pruebas con usuarios

Protocolo: 5 a 10 personas sin experiencia aeroespacial; tarea “lograr una misión a la Luna y luego a Marte”; métricas: tiempo hasta el primer éxito, porcentaje de misiones logradas, comprensión (cuestionario antes y después) y escala de usabilidad SUS.

| Métrica | Resultado |
|---|---|
| Participantes | [COMPLETAR] |
| Tiempo hasta el primer éxito | [COMPLETAR] |
| Misiones logradas | [COMPLETAR] |
| Mejora en el cuestionario | [COMPLETAR] |
| SUS | [COMPLETAR] |
| Cambios hechos tras la prueba | [COMPLETAR] |

Hasta la fecha de este borrador **no se hicieron pruebas con usuarios**.

## 11. Mercado y competencia

| Producto | Qué ofrece | Lección para nosotros |
|---|---|---|
| Kerbal Space Program | Sandbox con física muy detallada | Una reseña señala que cuando un cohete falla el juego explica mal por qué. Nuestro hueco: explicar causas |
| Kerbal Space Program 2 | Secuela | Reseñas mayormente negativas en Steam (27 % positivas sobre más de 31.000 al consultar) |
| Mars Horizon | Gestión de agencia, hecho con apoyo de ESA y de la agencia espacial británica | Menos realismo orbital; el respaldo institucional da credibilidad |
| Per Aspera | Estrategia narrativa de terraformar Marte | No es diseño de misión |
| Last Signal from Ceruvia (equipo del desafío) | Diseño arrastrando piezas, pilotaje de lanzamiento a reentrada, eventos, ranking, códigos de diseño, roles | Cubre varias funciones que nos faltan |
| MissionForge (dos repositorios) y Mission Forge (otros dos) | 3D, revisión previa al vuelo, reporte exportable, SLS, Falcon Heavy, Vulcan, Ariane 64, Electron, fuentes NASA citadas | Visualización y fuentes citadas son el estándar a superar |
| LUNARIS | 15 conjuntos de datos con fuente (unos 396 valores), centrado en la Luna | Los datos con trazabilidad ya existen en otros proyectos |
| MISSION: LAST LIGHT | Escenario Bennu con datos de Horizons y PDS | Compite en uno de nuestros destinos |
| Space Traveller | Para 10 a 14 años, “del Sol a Plutón” | Cubre la idea de múltiples cuerpos |
| Proyecto con archivo de trazabilidad | Marca cada dato como estimación o valor NASA; el juego solo lee un archivo estático | Es el mismo enfoque que adoptamos aquí |
| What IF | Reporte que traza la cadena de causas del resultado | Explicar causas ya no diferencia |

## 12. Diferenciación

Lo que ya no nos diferencia: eventos aleatorios, roles, ranking, reporte de causas, “varios cuerpos celestes” y datos de la NASA. Lo que sí puede diferenciarnos, **si lo hacemos de verdad**: (1) la economía como objetivo pedagógico explícito (presupuesto escalonado, reserva y el “gastar bien, no gastar menos”); (2) trazabilidad total de cada dato, con estado verificado o estimación visible en pantalla; (3) español primero, con un cohete argentino (Tronador II, datos por verificar con CONAE) y contexto latinoamericano; (4) la navegación continua, el seguimiento del corredor y la resolución de incidentes como decisiones centrales. Si no se cumple al menos (2), el proyecto queda por debajo de varios competidores.

## 13. Impacto y sostenibilidad

Uso en aulas y clubes de ciencia, sin instalación y sin costo. Sostenibilidad: licencia abierta, datos actualizados por automatización, contribuciones de terceros para sumar destinos y misiones. Métricas de impacto a medir: cantidad de jugadores, escuelas piloto y mejora en el cuestionario [COMPLETAR].

## 14. Riesgos y límites conocidos

1. Los valores de costo, masa y potencia son estimaciones de juego; el criterio de validez está expuesto hasta contrastarlos.
2. La dinámica orbital y los rangos de distancia son simplificados: todavía no hay integración numérica de órbitas, ventanas reales de lanzamiento ni ecuación del cohete. Los tiempos de viaje son una escala de juego.
3. El presupuesto se amplió a 1.800–3.200 créditos base, más bonificaciones por destino. Se debe continuar probando el equilibrio entre presupuesto, equipamiento y dificultad.
4. El script de datos en vivo y el flujo automático no se probaron contra los servidores reales.
5. El multijugador es por turnos en un mismo dispositivo.
6. Sin pruebas con usuarios ni auditoría de accesibilidad.
7. Las APIs cambian: DONKI y APOD migraron en 2026 y DSN Now estaba en mantenimiento. El juego debe seguir funcionando si una fuente cae.
8. Información de competidores tomada de sus repositorios públicos; puede estar incompleta o desactualizada.

## 15. Equipo, licencia, IA y créditos

Equipo y roles: [COMPLETAR]. Licencia propuesta: MIT (archivo `LICENSE`), a confirmar por el equipo. Datos: NASA, JPL, CCMC; acreditar a cada fuente donde se use, y al CCMC por DONKI según su política de publicaciones. **Uso de inteligencia artificial:** parte del código y de este documento se elaboró con asistencia de Claude (Anthropic). [COMPLETAR: revisar si las reglas 2026 exigen declararlo y cómo].

## 16. Checklist de entrega

- [ ] Revisar la guía de entrega 2026 y la pestaña Resources del desafío
- [ ] Probar `tools/fetch_data.py` y verificar el ID de Bennu
- [ ] Verificar la ruta de DONKI en CCMC
- [ ] Completar `data/curated/sources.csv` con valores reales y fuentes
- [ ] Balancear Europa, Titán y Neptuno
- [ ] Hacer al menos una prueba con usuarios y completar la sección 10
- [ ] Subir el repositorio a GitHub y publicar en GitHub Pages
- [ ] Completar equipo, enlaces y declaración de uso de IA
- [ ] Grabar el video y registrar la entrega a tiempo
- [ ] Traducir el documento al inglés para los jueces globales

## Anexo A. Fuentes consultadas el 14/11/2026

- Texto del desafío: github.com/NASA-SPACEAPP-2026/Space-Mission-Design-Game
- Criterios de evaluación (impacto, creatividad, validez, relevancia y presentación): guías de ediciones anteriores en spaceappschallenge.org; confirmar la edición 2026
- JPL Horizons: ssd-api.jpl.nasa.gov/doc/horizons.html y horizons_lookup.html
- SBDB: ssd-api.jpl.nasa.gov/doc/sbdb.html y sbdb_query.html; ssd.jpl.nasa.gov/sb
- Límites de api.nasa.gov: api.nasa.gov/assets/html/authentication.html
- Migración de DONKI: packagist.org/packages/omnilab/donki y github.com/ProgramComputer/NASA-MCP-server (release v1.2.0)
- Launch Library 2: thespacedevs.com/llapi
- DSN Now: eyes.nasa.gov/apps/dsn-now
- Mercado: pcgamesn.com (Mars Horizon y Kerbal), space.com (Mars Horizon), nodal.gg (datos de Steam)
- Equipos del desafío: repositorios de Last Signal from Ceruvia, MissionForge, Mission Forge, LUNARIS, Mission Last Light, Space Traveller, What IF y otros en GitHub

## Anexo B. Hoja de ruta

Corto plazo (antes de entregar): completar datos curados, probar la descarga de Horizons, hacer una prueba con usuarios y balancear destinos lejanos. Mediano plazo: modelo de Δv con ecuación del cohete, presupuesto de enlace real, códigos de diseño compartibles, multijugador en red y versión en inglés. Largo plazo: visualización 3D de la nave, ventanas de lanzamiento reales, modo competitivo y ranking global.
