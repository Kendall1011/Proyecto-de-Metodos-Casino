import pygame
import pyodbc
import matplotlib.pyplot as plt
import csv
from config import VENTANA, ANCHO, fuente, pequena, BLANCO,ALTO,NEGRO
import os

rojos = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
negros = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]

class PantallaEstadisticas:
    def __init__(self, volver_callback):
        self.volver_callback = volver_callback
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

            plt.figure(figsize=(9, 4), dpi=200)
            plt.bar(numeros, cantidades, color=colores_barras)
            plt.xticks(numeros, fontsize=9)
            plt.yticks(fontsize=9)
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

            plt.figure(figsize=(4.5, 4.5), dpi=200)
            wedges, texts, autotexts = plt.pie(
                valores, labels=labels, colors=colores_pie, autopct='%1.1f%%',
                startangle=90, textprops={'color': 'white', 'fontsize': 12}
            )
            for text in autotexts:
                text.set_color("white")
                text.set_fontsize(13)

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

        # Total de giros arriba del todo centrado con borde negro
        total_txt = fuente.render(f"Total de giros: {self.total}", True, NEGRO)
        ventana.blit(total_txt, (ANCHO // 2 - total_txt.get_width() // 2, 10))
        pygame.draw.rect(ventana, NEGRO, (ANCHO // 2 - total_txt.get_width() // 2 - 10, 8, total_txt.get_width() + 20, total_txt.get_height() + 4), 1)

        # Gráfico de barras
        if os.path.exists("grafico_barras.png"):
            img_barra = pygame.image.load("grafico_barras.png")
            img_barra = pygame.transform.scale(img_barra, (820, 180))
            ventana.blit(img_barra, (ANCHO // 2 - 410, 50))

        # Gráfico de pastel
        if os.path.exists("grafico_pastel.png"):
            img_pie = pygame.image.load("grafico_pastel.png")
            img_pie = pygame.transform.scale(img_pie, (240, 240))
            ventana.blit(img_pie, (80, 260))

        # Tabla de frecuencias
        y_base = 260
        x_col1 = 350
        x_col2 = x_col1 + 70
        x_col3 = x_col2 + 70
        x_col4 = x_col3 + 80

        ventana.blit(fuente.render("Num", True, NEGRO ), (x_col1, y_base))
        ventana.blit(fuente.render("Freq", True, NEGRO), (x_col2, y_base))
        ventana.blit(fuente.render("%", True, NEGRO), (x_col3 + 5, y_base))
        ventana.blit(fuente.render("Color", True, NEGRO), (x_col4, y_base))
        y_base += 30

        filas = [(i, self.frecuencias[i]) for i in range(37) if self.frecuencias[i] > 0]
        filas_visibles = 12
        self.max_scroll = max(0, len(filas) - filas_visibles)
        for idx in range(self.scroll_offset, min(self.scroll_offset + filas_visibles, len(filas))):
            i, freq = filas[idx]
            porcentaje = (freq / self.total) * 100
            color = "verde" if i == 0 else "rojo" if i in rojos else "negro"
            ventana.blit(pequena.render(str(i), True, NEGRO), (x_col1, y_base))
            ventana.blit(pequena.render(str(freq), True, NEGRO), (x_col2, y_base))
            ventana.blit(pequena.render(f"{porcentaje:.1f}%", True, NEGRO), (x_col3, y_base))
            ventana.blit(pequena.render(color, True, NEGRO), (x_col4, y_base))
            y_base += 22

        # Indicador de scroll
        if self.max_scroll > 0:
            scroll_text = pequena.render(f"▲▼ ({self.scroll_offset+1}-{min(self.scroll_offset+filas_visibles, len(filas))}/{len(filas)})", True, NEGRO)
            ventana.blit(scroll_text, (x_col4 + 60, 260))

        # Título recomendaciones
        titulo_reco = fuente.render("Recomendaciones:", True, NEGRO)
        ventana.blit(titulo_reco, (80, 555))

        # Mostrar recomendaciones con colores específicos
        recomendaciones = self.generar_recomendaciones()
        colores = [(0, 150, 0), NEGRO, (200, 0, 0), NEGRO, NEGRO]
        y_reco = 590
        for i, reco in enumerate(recomendaciones):
            color = colores[i % len(colores)]
            texto_reco = pequena.render("* " + reco, True, color)
            ventana.blit(texto_reco, (80, y_reco))
            y_reco += 25

        # Botones
        boton_ancho = 90
        boton_alto = 30
        espacio_botones = 12
        margen_derecho = 30
        margen_inferior = 20

        self.boton_exportar = pygame.Rect(ANCHO - boton_ancho - margen_derecho, ALTO - boton_alto - margen_inferior, boton_ancho, boton_alto)
        self.boton_volver = pygame.Rect(ANCHO - 2 * boton_ancho - espacio_botones - margen_derecho, ALTO - boton_alto - margen_inferior, boton_ancho, boton_alto)

        pygame.draw.rect(ventana, (180, 180, 0), self.boton_volver, border_radius=8)
        texto_btn = fuente.render("Volver", True, (0, 0, 0))
        ventana.blit(texto_btn, (self.boton_volver.centerx - texto_btn.get_width() // 2, self.boton_volver.centery - texto_btn.get_height() // 2))

        pygame.draw.rect(ventana, (100, 200, 100), self.boton_exportar, border_radius=8)
        texto_exp = fuente.render("CSV", True, (0, 0, 0))
        ventana.blit(texto_exp, (self.boton_exportar.centerx - texto_exp.get_width() // 2, self.boton_exportar.centery - texto_exp.get_height() // 2))

    def generar_recomendaciones(self):
        recomendaciones = []

        color_mas_frecuente = max(self.colores_contador, key=self.colores_contador.get)
        veces_color = self.colores_contador[color_mas_frecuente]
        porcentaje_color = (veces_color / self.total) * 100
        recomendaciones.append(f"Se recomienda apostar al color {color_mas_frecuente} porque ha salido un {porcentaje_color:.2f}% de las veces.")

        numero_mas_frecuente = max(range(len(self.frecuencias)), key=lambda i: self.frecuencias[i])
        veces_num = self.frecuencias[numero_mas_frecuente]
        recomendaciones.append(f"El número que más ha salido es el {numero_mas_frecuente} ({veces_num} veces).")

        if self.colores_contador["verde"] == 0:
            recomendaciones.append("No se recomienda apostar al verde (0), ya que nunca ha salido.")

        menor_frecuencia = min([f for f in self.frecuencias if f > 0])
        numeros_menos_frecuentes = [i for i, f in enumerate(self.frecuencias) if f == menor_frecuencia]
        recomendaciones.append(f"No se recomienda apostar al número {numeros_menos_frecuentes[0]} que ha salido solo {menor_frecuencia} veces.")

        recomendaciones.append("Se recomienda apostar a la zona 1st 12, ya que concentra varios números con alta frecuencia.")

        return recomendaciones
