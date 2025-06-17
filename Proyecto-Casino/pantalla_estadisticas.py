import pygame
import pyodbc
import matplotlib.pyplot as plt
import csv
from config import VENTANA, ANCHO, fuente, pequena, BLANCO,ALTO,NEGRO
import os

rojos = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
negros = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]

class PantallaEstadisticas:
    def __init__(self, volver_callback, sugerencias_callback):
        self.volver_callback = volver_callback
        self.sugerencias_callback = sugerencias_callback
        self.frecuencias = [0] * 37
        self.total = 0
        self.colores_contador = {"rojo": 0, "negro": 0, "verde": 0}
        self.scroll_offset = 0
        self.max_scroll = 0
        self.generar_datos()
        self.generar_graficos()

    def generar_datos(self):
        try:
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=DESKTOP-TEIIL4V\\SQLSERVERDEV2022;'
                'DATABASE=RuletaDBMetodos;'
                'UID=SaysaProject;'
                'PWD=leogon10'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT Numero FROM Giros")
            resultados = [row[0] for row in cursor.fetchall()]
            conn.close()

            for numero in resultados:
                if 0 <= numero <= 36:
                    self.frecuencias[numero] += 1
                    if numero == 0:
                        self.colores_contador["verde"] += 1
                    elif numero in rojos:
                        self.colores_contador["rojo"] += 1
                    else:
                        self.colores_contador["negro"] += 1
            self.total = sum(self.frecuencias)
        except Exception as e:
            print(f"❌ Error al obtener datos: {e}")

    def generar_graficos(self):
        try:
            # Barras
            numeros, cantidades, colores_barras = [], [], []
            for i in range(37):
                if self.frecuencias[i] > 0:
                    numeros.append(i)
                    cantidades.append(self.frecuencias[i])
                    colores_barras.append("green" if i == 0 else "red" if i in rojos else "black")

            plt.figure(figsize=(14, 6), dpi=200)  # Más ancho que alto
            bar_width = 0.6  # Más delgado para dejar espacio entre barras
            bars = plt.bar(numeros, cantidades, color=colores_barras, width=bar_width, align='center', edgecolor='gray', linewidth=0.8)
            plt.xticks(numeros, fontsize=11)
            plt.yticks(fontsize=11)
            plt.xlabel("Número", fontsize=13)
            plt.ylabel("Frecuencia", fontsize=13)
            plt.grid(axis='y', linestyle='--', alpha=0.4)
            plt.subplots_adjust(left=0.06, right=0.98, top=0.95, bottom=0.13)  # Usa más espacio del cuadro
            plt.tight_layout()
            plt.savefig("grafico_barras.png")
            plt.close()

            # Pastel
            labels, valores, colores_pie = [], [], []
            for color in ['rojo', 'negro', 'verde']:
                count = self.colores_contador[color]
                if count > 0:
                    labels.append(color.capitalize())
                    valores.append(count)
                    colores_pie.append("red" if color == "rojo" else "black" if color == "negro" else "green")

            plt.figure(figsize=(9, 9), dpi=200)  # <-- También puedes agrandar el gráfico aquí
            wedges, texts, autotexts = plt.pie(
                valores, labels=labels, colors=colores_pie, autopct='%1.1f%%',
                startangle=90, textprops={'color': 'white', 'fontsize': 18}  # <-- Aumenta el tamaño de fuente
            )
            for text in autotexts:
                text.set_color("white")
                text.set_fontsize(32)  # <-- Aumenta el tamaño de los porcentajes

            plt.tight_layout()
            plt.savefig("grafico_pastel.png")
            plt.close()

        except Exception as e:
            print(f"❌ Error al generar gráficos: {e}")

    def exportar_csv(self):
        try:
            with open("resultados_ruleta.csv", mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Numero", "Frecuencia", "Porcentaje", "Color"])

                for i in range(37):
                    if self.frecuencias[i] > 0:
                        porcentaje = (self.frecuencias[i] / self.total) * 100
                        color = "verde" if i == 0 else "rojo" if i in rojos else "negro"
                        writer.writerow([i, self.frecuencias[i], f"{porcentaje:.1f}%", color])

            print("✅ Archivo 'resultados_ruleta.csv' exportado correctamente.")
        except Exception as e:
            print(f"❌ Error al exportar CSV: {e}")

    def manejar_evento(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos
            if self.boton_volver.collidepoint(x, y):
                self.volver_callback()
            elif self.boton_exportar.collidepoint(x, y):
                self.exportar_csv()
            elif self.boton_recomendaciones.collidepoint(x, y):
                self.sugerencias_callback()  # <-- Aquí llamas al callback
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_DOWN:
                if self.scroll_offset < self.max_scroll:
                    self.scroll_offset += 1
            elif evento.key == pygame.K_UP:
                if self.scroll_offset > 0:
                    self.scroll_offset -= 1

    def actualizar(self):
        pass

    def dibujar(self, ventana):
        ventana.fill(BLANCO)

        # Título pequeño en caja discreta arriba a la izquierda
        titulo_font = pygame.font.SysFont("Arial", 22, bold=True)
        total_txt = titulo_font.render(f"Total de giros: {self.total}", True, NEGRO)
        box_w, box_h = total_txt.get_width() + 32, total_txt.get_height() + 16
        pygame.draw.rect(ventana, (245,245,245), (40, 18, box_w, box_h), border_radius=10)
        pygame.draw.rect(ventana, (200,200,200), (40, 18, box_w, box_h), 1, border_radius=10)
        ventana.blit(total_txt, (40 + 16, 18 + 8))

        # --- BOTONES ARRIBA, alineados A LA DERECHA ---
        boton_ancho = 90
        boton_alto = 32
        espacio_btns = 12
        total_botones_w = (boton_ancho + espacio_btns) * 3 - espacio_btns
        x_botones = ANCHO - 40 - total_botones_w
        y_botones = 18 + (box_h - boton_alto) // 2

        self.boton_recomendaciones = pygame.Rect(x_botones, y_botones, boton_ancho, boton_alto)
        self.boton_volver = pygame.Rect(x_botones + boton_ancho + espacio_btns, y_botones, boton_ancho, boton_alto)
        self.boton_exportar = pygame.Rect(x_botones + 2 * (boton_ancho + espacio_btns), y_botones, boton_ancho, boton_alto)

        pygame.draw.rect(ventana, (100, 200, 100), self.boton_recomendaciones, border_radius=8)
        texto_reco_btn = pequena.render("Sugerencias", True, (0, 0, 0))
        ventana.blit(texto_reco_btn, (self.boton_recomendaciones.centerx - texto_reco_btn.get_width() // 2, self.boton_recomendaciones.centery - texto_reco_btn.get_height() // 2))

        pygame.draw.rect(ventana, (180, 180, 0), self.boton_volver, border_radius=8)
        texto_btn = pequena.render("Volver", True, (0, 0, 0))
        ventana.blit(texto_btn, (self.boton_volver.centerx - texto_btn.get_width() // 2, self.boton_volver.centery - texto_btn.get_height() // 2))

        pygame.draw.rect(ventana, (0, 120, 255), self.boton_exportar, border_radius=8)
        texto_exp = pequena.render("CSV", True, (255, 255, 255))
        ventana.blit(texto_exp, (self.boton_exportar.centerx - texto_exp.get_width() // 2, self.boton_exportar.centery - texto_exp.get_height() // 2))

        # Gráfico de barras
        grafico_h = 320
        grafico_w = ANCHO - 80
        grafico_x = 40
        grafico_y = 18 + box_h + 10
        if os.path.exists("grafico_barras.png"):
            img_barra = pygame.image.load("grafico_barras.png")
            img_barra = pygame.transform.smoothscale(img_barra, (grafico_w, grafico_h))
            ventana.blit(img_barra, (grafico_x, grafico_y))

        # Cuadro para datos y gráfico de pastel
        cuadro_x = 50
        cuadro_y = grafico_y + grafico_h + 10
        cuadro_w = ANCHO - 90
        cuadro_h = ALTO - cuadro_y - 50
        pygame.draw.rect(ventana, (255,255,255), (cuadro_x, cuadro_y, cuadro_w, cuadro_h), border_radius=18)
        pygame.draw.rect(ventana, (210,210,210), (cuadro_x, cuadro_y, cuadro_w, cuadro_h), 2, border_radius=18)

        # División de columnas (60% tabla, 40% pastel)
        col_div = cuadro_x + int(cuadro_w * 0.5)
        margen_lateral = 20
        margen_vertical = 20

        # Calcula el área disponible para el gráfico de pastel
        ancho_columna = cuadro_w * 0.4 - 2 * margen_lateral
        alto_columna = cuadro_h - 2 * margen_vertical

        # El gráfico de pastel ocupa todo el espacio disponible en la columna derecha
        pastel_size = int(min(ancho_columna, alto_columna) * 1)

        # Centrado en la columna derecha
        pastel_x = int(col_div + (cuadro_x + cuadro_w - col_div - pastel_size) // 2)
        pastel_y = int(cuadro_y + (cuadro_h - pastel_size) // 2)

        if os.path.exists("grafico_pastel.png"):
            img_pie = pygame.image.load("grafico_pastel.png")
            img_pie = pygame.transform.smoothscale(img_pie, (pastel_size, pastel_size))
            ventana.blit(img_pie, (pastel_x, pastel_y))

        # --- TABLA IZQUIERDA ---
        tabla_x = cuadro_x + 30
        tabla_y = cuadro_y + 18
        col_w = 70
        header_font = pygame.font.SysFont("Arial", 18, bold=True)
        cell_font = pygame.font.SysFont("Arial", 15)
        headers = ["Num", "Frec.", "%", "Color"]
        for i, h in enumerate(headers):
            ventana.blit(header_font.render(h, True, NEGRO), (tabla_x + i * col_w, tabla_y))

        filas = [(i, self.frecuencias[i]) for i in range(37) if self.frecuencias[i] > 0]
        filas_visibles = int((cuadro_h - 60) // 22)
        self.max_scroll = max(0, len(filas) - filas_visibles)
        y_base = tabla_y + 24
        for idx in range(self.scroll_offset, min(self.scroll_offset + filas_visibles, len(filas))):
            i, freq = filas[idx]
            porcentaje = (freq / self.total) * 100
            color = "verde" if i == 0 else "rojo" if i in rojos else "negro"
            ventana.blit(cell_font.render(str(i), True, NEGRO), (tabla_x, y_base))
            ventana.blit(cell_font.render(str(freq), True, NEGRO), (tabla_x + col_w, y_base))
            ventana.blit(cell_font.render(f"{porcentaje:.1f}%", True, NEGRO), (tabla_x + 2 * col_w, y_base))
            ventana.blit(cell_font.render(color, True, NEGRO), (tabla_x + 3 * col_w, y_base))
            y_base += 22

        # Indicador de scroll
        if self.max_scroll > 0:
            scroll_text = pequena.render(
                f"▲▼ ({self.scroll_offset+1}-{min(self.scroll_offset+filas_visibles, len(filas))}/{len(filas)})",
                True, (120,120,120)
            )
            ventana.blit(scroll_text, (tabla_x + 4 * col_w + 8, tabla_y))

    def generar_recomendaciones(self):
        # Consejos generales (sin datos)
        consejos_generales = [
            "Recuerda que la ruleta es un juego de azar, juega de manera responsable.",
            "No apuestes grandes sumas en una sola jugada, distribuye tu capital para minimizar riesgos.",
            "Si detectas una tendencia, puedes aprovecharla, pero no confíes en que continuará indefinidamente.",
            "Consulta las estadísticas regularmente para ajustar tu estrategia.",
            "Establece un límite de pérdidas y respétalo para evitar decisiones impulsivas.",
            "El objetivo principal es disfrutar el juego ¡Juega con responsabilidad!."
        ]

        recomendaciones = []

        # Ejemplo de recomendaciones basadas en datos:
        if self.total > 0:
            color_mas_frecuente = max(["rojo", "negro", "verde"], key=lambda c: getattr(self, "colores_contador", {}).get(c, 0))
            veces_color = getattr(self, "colores_contador", {}).get(color_mas_frecuente, 0)
            porcentaje_color = (veces_color / self.total) * 100 if self.total > 0 else 0
            recomendaciones.append(
                f"Se recomienda apostar al color {color_mas_frecuente} porque ha salido {veces_color} veces, representando el {porcentaje_color:.2f}% de los giros."
            )

            numero_mas_frecuente = max(range(len(self.frecuencias)), key=lambda i: self.frecuencias[i])
            veces_num = self.frecuencias[numero_mas_frecuente]
            porcentaje_num = (veces_num / self.total) * 100 if self.total > 0 else 0
            recomendaciones.append(
                f"El número que más ha salido es el {numero_mas_frecuente} ({veces_num} veces, {porcentaje_num:.2f}% de los giros)."
            )

            menor_frecuencia = min([f for f in self.frecuencias if f > 0])
            numeros_menos_frecuentes = [i for i, f in enumerate(self.frecuencias) if f == menor_frecuencia]
            lista_menores = ', '.join(str(n) for n in numeros_menos_frecuentes)
            recomendaciones.append(
                f"No se recomienda apostar a los números {lista_menores}, ya que cada uno ha salido solo {menor_frecuencia} veces."
            )

            if getattr(self, "colores_contador", {}).get("verde", 0) == 0:
                recomendaciones.append("No se recomienda apostar al verde (0), ya que nunca ha salido en el historial actual.")

            zonas = {
                "1st 12": sum(self.frecuencias[1:13]),
                "2nd 12": sum(self.frecuencias[13:25]),
                "3rd 12": sum(self.frecuencias[25:37])
            }
            zona_mas_frecuente = max(zonas, key=zonas.get)
            veces_zona = zonas[zona_mas_frecuente]
            porcentaje_zona = (veces_zona / self.total) * 100 if self.total > 0 else 0
            recomendaciones.append(
                f"La zona más frecuente es {zona_mas_frecuente} con {veces_zona} apariciones ({porcentaje_zona:.2f}% de los giros)."
            )

            pares = sum(self.frecuencias[i] for i in range(2, 37, 2))
            impares = sum(self.frecuencias[i] for i in range(1, 37, 2))
            if pares > impares:
                recomendaciones.append(
                    f"Han salido más números pares ({pares}) que impares ({impares}), podrías considerar apostar a PAR."
                )
            elif impares > pares:
                recomendaciones.append(
                    f"Han salido más números impares ({impares}) que pares ({pares}), podrías considerar apostar a IMPAR."
                )

            # Mitades
            bajos = sum(self.frecuencias[1:19])
            altos = sum(self.frecuencias[19:37])
            if bajos > altos:
                recomendaciones.append(
                    f"Han salido más números bajos (1-18): {bajos} veces, que altos (19-36): {altos} veces."
                )
            elif altos > bajos:
                recomendaciones.append(
                    f"Han salido más números altos (19-36): {altos} veces, que bajos (1-18): {bajos} veces."
                )

            # Rachas de color
            if veces_color >= 3:
                recomendaciones.append(
                    f"¡Atención! El color {color_mas_frecuente} lleva una racha de {veces_color} apariciones."
                )

        return consejos_generales, recomendaciones
