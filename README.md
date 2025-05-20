
# 🎰 Proyecto de Métodos Cuantitativos – Simulador de Ruleta

Este repositorio contiene un simulador de ruleta desarrollado como parte del curso de Métodos Cuantitativos, con el objetivo de aplicar modelos de análisis y simulación en un entorno lúdico. La aplicación permite simular apuestas en una ruleta estilo casino, analizar resultados y obtener estadísticas, utilizando programación con Pygame y técnicas como simulación Monte Carlo.

---

## 🧠 Objetivos del Proyecto

- Simular el comportamiento de una ruleta tipo americana de casino.
- Permitir apuestas visuales por color, número o grupos.
- Implementar lógica de pagos, turnos y control de fichas.
- Registrar los resultados para análisis probabilístico y visualización de estadísticas.
- Explorar conceptos matemáticos como probabilidad, regresión y simulación.

---

## 🕹️ Funcionalidades Principales

- 🎮 Modo de 1 jugador y 2 jugadores con fichas diferenciadas.
- 🧠 Lógica de apuestas realista: el dinero solo se rebaja si se realiza el giro.
- 🔁 Animación de giro de la ruleta con resultado visual.
- 📊 Registro en base de datos de los resultados para análisis estadístico.
- 🔊 Efectos de sonido: clics, giro de ruleta, música de fondo y notificación de resultado.
- 📐 Tablero de apuestas visual con diseño realista tipo casino.
- 💾 Estadísticas de resultados acumulados tras múltiples giros.

---

## 📁 Estructura del Proyecto

```
Proyecto-Casino/
├── sonidos/                  # Imágenes y sonidos
├── base_datos/             # Scripts y archivo SQLite de registro
├── screens/                # pantallas del juego (inicio, juego1, juego2)
├── estado_juego.py         # Clase que controla el estado general
├── main.py                 # Archivo principal de ejecución
├── config.py               # Colores, dimensiones, constantes
├── datos_juego.py          # Números, fichas y colores de ruleta
├── estadisticas.py         # Cálculo y visualización de estadísticas
├── README.md               # Este archivo
```

---

## ▶️ Cómo ejecutar

1. Instala Python 3.10 o superior.
2. Instala las dependencias:

3. Ejecuta el juego:

```bash
python main.py
```

---

## 🧮 Métodos Cuantitativos aplicados

- **Simulación Monte Carlo** para análisis de patrones de aparición de números.
- **Estadística descriptiva** (frecuencias y porcentajes de aparición).
- **Probabilidades empíricas** por número, color y tipo de apuesta.
- **Visualización de datos** con gráficas y contadores.

---

## 📚 Requisitos del Curso

- Proyecto interactivo con entrada/salida de datos.
- Uso de modelo cuantitativo claramente definido.
- Resultados visuales y reportes.
- Prototipos de pantallas con diseño e interfaz.

---

## 👥 Autores

- **Kendall León González**  
  Estudiante de Informática Empresarial – Universidad de Costa Rica  
  [LinkedIn](https://www.linkedin.com/in/kendall-leon-gonzález1011)

---

## 📜 Licencia

Este proyecto está bajo la licencia MIT. Puedes utilizarlo libremente con fines educativos y personales.

---

## 🛠️ To Do (Futuro)

- Conexión con una base de datos externa o web.
- Gráficas avanzadas con Matplotlib o Power BI.
- Agregar tipos de apuesta complejas (esquinas, líneas).
- Modo multijugador online.
