import flet as ft
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import mysql.connector
from mysql.connector import Error
import os
from reportlab.platypus import Image
from datetime import datetime
from decimal import Decimal  # Para cálculos financieros precisos
import webbrowser
from reportlab.platypus import Frame
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame




# Función para obtener la conexión a la base de datos
def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost", user="root", password="", database="facturacion"
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            return conexion
    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

# Clase Producto para gestionar los datos de los productos
class Producto:
    def __init__(self, concepto, precio_unitario, cantidad):
        self.concepto = concepto
        self.precio_unitario = Decimal(precio_unitario)  # Usar Decimal
        self.cantidad = cantidad
        self.monto = self.precio_unitario * Decimal(cantidad)

# Función principal de la aplicación
def main(page: ft.Page):
    page.title = "Software de Facturación"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 800
    page.window_height = 800
    page.scroll = "auto"

    productos = []
    productos_lista = ft.Column()

    def actualizar_total():
        total = sum(producto.monto for producto in productos)
        total_text.value = f"Total: ${total:.2f}"
        page.update()

    def obtener_precio_concepto(concepto):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "SELECT precio FROM productos WHERE concepto = %s", (concepto,)
            )
            resultado = cursor.fetchone()
            if resultado:
                return Decimal(resultado[0])
            else:
                return None
        except Exception as e:
            print(f"Error al obtener el precio: {e}")
            return None
        finally:
            cursor.close()
            conexion.close()

    def obtener_conceptos():
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("SELECT concepto FROM productos")
            resultados = cursor.fetchall()
            return [r[0] for r in resultados]
        except Exception as e:
            print(f"Error al obtener los conceptos: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

    def asignar_precio(concepto):
        if concepto:
            precio = obtener_precio_concepto(concepto)
            if precio is not None:
                precio_unitario_input.value = f"{precio:.2f}"
            else:
                precio_unitario_input.value = "0.00"
            page.update()
        else:
            precio_unitario_input.value = ""

    def actualizar_opciones_concepto(e):
        query = concepto_input.value.lower().strip()
        if query:
            opciones = [c for c in conceptos_disponibles if query in c.lower()]
            opciones_lista.controls.clear()
            for opcion in opciones:
                opciones_lista.controls.append(
                    ft.TextButton(
                        text=opcion,
                        on_click=lambda e, op=opcion: seleccionar_concepto(op),
                    )
                )
            opciones_lista.visible = bool(opciones)
        else:
            opciones_lista.visible = False
        page.update()

    def ocultar_opciones_concepto(e):
        if not concepto_input.value.strip():  # Si el campo está vacío
            opciones_lista.visible = False
        page.update()

    def seleccionar_concepto(concepto):
        concepto_input.value = concepto
        opciones_lista.visible = False
        asignar_precio(concepto)
        page.update()

    def agregar_producto(e):
        try:
            concepto = concepto_input.value
            precio = Decimal(precio_unitario_input.value)
            cantidad = int(cantidad_input.value)

            if concepto and precio > 0 and cantidad > 0:
                nuevo_producto = Producto(concepto, precio, cantidad)
                productos.append(nuevo_producto)

                def eliminar_producto(e):
                    productos.remove(nuevo_producto)
                    productos_lista.controls.remove(producto_row)
                    actualizar_total()
                    page.update()

                producto_row = ft.Row(
                    [
                        ft.Text(concepto, width=200),
                        ft.Text(f"${precio:,.2f}", width=100),  # Formateado con puntos de miles
                        ft.Text(str(cantidad), width=100, text_align=ft.TextAlign.CENTER),
                        ft.Text(f"${nuevo_producto.monto:,.2f}", width=100),  # Formateado con puntos de miles
                        ft.IconButton(ft.icons.DELETE, on_click=eliminar_producto),
                    ]
                )
                productos_lista.controls.append(producto_row)

                concepto_input.value = ""
                precio_unitario_input.value = ""
                cantidad_input.value = ""

                actualizar_total()
                page.update()
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, ingrese valores válidos"))
            page.snack_bar.open = True
            page.update()


    def actualizar_total():
        total = sum(producto.monto for producto in productos)
        total_text.value = f"Total: ${total:,.2f}"  # Formateado con puntos de miles
        page.update()

        
    def guardar_pdf(e):
       
            # Definir la ruta base del proyecto
        ruta_base = os.path.dirname(os.path.abspath(__file__))  # Obtiene la ruta del archivo Python actual

        # Crear la ruta relativa a la carpeta de facturas dentro del proyecto
        ruta_guardado = os.path.join(ruta_base, "facturas")

        # Verificar si la carpeta existe, si no, crearla
        if not os.path.exists(ruta_guardado):
            os.makedirs(ruta_guardado)

        # Generar el nombre del archivo con la fecha y hora
        fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        archivo = os.path.join(ruta_guardado, f"factura_{fecha_hora}.pdf")

        estilos = getSampleStyleSheet()

        # Crear el documento con un PageTemplate personalizado
        doc = BaseDocTemplate(archivo, pagesize=letter)

        # Definir los márgenes y el área de contenido principal
        margen_superior = 25
        margen_inferior = 80
        ancho, alto = letter

        # Marco para el contenido principal
        frame_contenido = Frame(
            x1=50, y1=margen_inferior + 20, width=ancho - 100, height=alto - margen_superior - margen_inferior,
            id="contenido"
        )

        # Página con un marco para el contenido principal
        def template(canvas, doc):
            canvas.saveState()

            # Calcular la posición central de la página
            y_centro = (alto + margen_inferior + margen_superior) / 2 

            # Crear la tabla de firma y total
            total = sum(p.monto for p in productos)
            firma_y_total = [
                [
                    Paragraph("Firma: ___________________________", estilos["Normal"]),
                    Paragraph(f"Total a Pagar: ${total:,.2f}", estilos["Heading4"]),
                ]
            ]

            tabla_firma_total = Table(firma_y_total, colWidths=[400, 150])
            tabla_firma_total.setStyle(
                TableStyle(
                    [
                        ("ALIGN", (0, 0), (0, 0), "LEFT"),
                        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                    ]
                )
            )
            
            # Calcular la altura para que quede centrado
            tabla_firma_total.wrapOn(canvas, 400, 50)
            tabla_firma_total.drawOn(canvas, 50, y_centro - 30)  # Posición centrada en la página

            canvas.restoreState()

        doc.addPageTemplates([PageTemplate(id="principal", frames=frame_contenido, onPage=template)])

        # Crear contenido dinámico
        elementos = []

                # Rutas de los logos
        logo_izquierdo = "imagenes/logo.png"
        logos_derecha = [
            "imagenes/colombina.png",
            "imagenes/amer.png",
            "imagenes/mas.png",
            "imagenes/postobon.png",
            "imagenes/bavaria.png",
        ]


        # Cargar logo izquierdo
        if os.path.exists(logo_izquierdo):
            logo_left = Image(logo_izquierdo)
            logo_left.drawHeight = 60
            logo_left.drawWidth = 60
        else:
            logo_left = ""

        # Cargar los logos de la derecha
        logo_data_derecha = []
        for logo_path in logos_derecha:
            if os.path.exists(logo_path):
                logo = Image(logo_path)
                logo.drawHeight = 40
                logo.drawWidth = 70
                logo_data_derecha.append(logo)
            else:
                logo_data_derecha.append("")

        # Crear fila con los logos de la derecha
        tabla_derecha = Table([logo_data_derecha], colWidths=[100, 100, 100])
        tabla_derecha.setStyle(
            TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )

        # Tabla principal del encabezado
        encabezado = Table(
            [[logo_left, "", tabla_derecha]],
            colWidths=[70, 200, 300],
        )
        encabezado.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (0, 0), (0, 0), "LEFT"),
                    ("ALIGN", (2, 0), (2, 0), "RIGHT"),
                ]
            )
        )
        elementos.append(encabezado)
        elementos.append(Spacer(1, 7))  # Espacio después de los logos

        # Título
        titulo = Paragraph("DULCERIA <b>R & V</b>", estilos["Title"])
        elementos.append(titulo)
        elementos.append(Spacer(1, 2))  # Espacio después del título

        fecha_actual = datetime.now().strftime("%Y-%m-%d")  # Formato YYYY-MM-DD

        # Agregar recuadro de información
        data_recuadro = [
            [
                Paragraph("Señor(a): José Riascos<br/>Dirección: Carrera 66 1b<br/>Nit: 2133134<br/>Numero de la Empresa: 3165613027", estilos["Normal"]),
                Paragraph("Cliente:<br/>Tel:<br/>Barrio:", estilos["Normal"]),
                Paragraph(f"Fecha: {fecha_actual}<br/>Vendedor: Jhoan Hernandes<br/>Numero: 3206408315-3107075636 ", estilos["Normal"]),
            ]
        ]
        tabla_recuadro = Table(data_recuadro, colWidths=[210, 200, 170])
        tabla_recuadro.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Bordes alrededor de todas las celdas
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),  # Alinear verticalmente al centro
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),  # Alinear texto a la izquierda
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                ]
            )
        )
        elementos.append(tabla_recuadro)
        elementos.append(Spacer(1, 7))  # Espacio después del recuadro

            # Crear la tabla con los productos
        data = [["No.", "Producto", "Precio Unitario", "Cantidad", "Total"]] + [
            [index + 1, p.concepto, f"${p.precio_unitario:,.2f}", p.cantidad, f"${p.monto:,.2f}"]
            for index, p in enumerate(productos)
        ]

        col_widths = [50, 230, 100, 100, 100]  # Ancho de las columnas

        tabla_productos = Table(data, colWidths=col_widths)
        tabla_productos.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),  # Eliminar el padding superior
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),  # Eliminar el padding inferior
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),  # Reducir el padding izquierdo
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),  # Reducir el padding derecho
                ]
            )
        )
        elementos.append(tabla_productos)
        elementos.append(Spacer(1, 7))  # Espacio después de la tabla de productos


        # Generar el documento PDF
        doc.build(elementos)
        page.snack_bar = ft.SnackBar(ft.Text(f"Factura generada: {archivo}"))
        page.snack_bar.open = True
        webbrowser.open(f"file://{archivo}")
        page.update()


    def add_producto(e):
        nombre_producto = producto.value.strip()
        precio_unitario_valor = precio.value.strip()

        # Validación de los campos
        if not nombre_producto or not precio_unitario_valor:
            page.snack_bar = ft.SnackBar(
                ft.Text("Por favor, ingresa todos los datos."), open=True
            )
            page.update()
            return

        try:
            precio_unitario_valor = Decimal(precio_unitario_valor)
            if precio_unitario_valor <= 0:
                raise ValueError("El precio debe ser mayor a cero.")

            # Conectar a la base de datos e insertar el producto
            conexion = obtener_conexion()
            if conexion:
                cursor = conexion.cursor()
                try:
                    cursor.execute(
                        "INSERT INTO productos (concepto, precio) VALUES (%s, %s)",
                        (nombre_producto, precio_unitario_valor),
                    )
                    conexion.commit()

                    # Notificación de éxito
                    page.snack_bar = ft.SnackBar(
                        ft.Text("Producto agregado correctamente."), open=True
                    )
                    producto.value = ""
                    precio.value = ""

                    # Actualizar la lista de conceptos disponibles
                    conceptos_disponibles.clear()  # Limpiar la lista actual
                    conceptos_disponibles.extend(obtener_conceptos())  # Actualizarla con los nuevos conceptos

                    # Actualizar las opciones de búsqueda
                    actualizar_opciones_concepto(None)

                except Error as err:
                    page.snack_bar = ft.SnackBar(
                        ft.Text(f"Error al agregar el producto: {err}"), open=True
                    )
                finally:
                    cursor.close()
                    conexion.close()
        except (ValueError, Error) as ex:
            page.snack_bar = ft.SnackBar(
                ft.Text(f"Error: {ex}"), open=True
            )
        page.update()

    def actualizar_opciones_busqueda(e):
        query = buscar_input.value.lower().strip()  # Leer el texto ingresado
        if query:  # Si hay texto, buscar coincidencias
            opciones = [c for c in conceptos_disponibles if query in c.lower()]
            opciones_busqueda.controls.clear()  # Limpiar opciones anteriores
            for opcion in opciones:
                opciones_busqueda.controls.append(
                    ft.TextButton(
                        text=opcion,
                        on_click=lambda e, op=opcion: seleccionar_producto(op),
                    )
                )
            opciones_busqueda.visible = bool(opciones)  # Mostrar si hay opciones
        else:  # Si el campo está vacío, ocultar las opciones
            opciones_busqueda.controls.clear()
            opciones_busqueda.visible = False
        page.update()

    def seleccionar_producto(producto):
        buscar_input.value = producto
        opciones_busqueda.visible = False
        page.update()  

       # Contenedor para mostrar resultados
    tabla_resultados = ft.Column()

    # Función para actualizar el precio de un producto
    def actualizar_precio_producto(e):
        concepto = buscar_input.value.strip()  # Obtener el nombre del producto desde 'buscar_input'
        precio_nuevo = precios.value.strip()  # Obtener el nuevo precio desde 'precios'

        # Verificar que el nombre del producto y el precio no estén vacíos
        if not concepto or not precio_nuevo:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor, ingresa un nombre de producto y un precio."), open=True)
            page.update()
            return

        try:
            # Convertir el precio a un número decimal para asegurar la correcta actualización
            precio_nuevo_decimal = Decimal(precio_nuevo)

            # Conectar a la base de datos
            conexion = obtener_conexion()
            if not conexion:
                page.snack_bar = ft.SnackBar(ft.Text("No se pudo conectar a la base de datos."), open=True)
                page.update()
                return

            cursor = conexion.cursor()
            # Ejecutar la consulta para actualizar el precio del producto
            cursor.execute(
                "UPDATE productos SET precio = %s WHERE concepto LIKE %s",
                (precio_nuevo_decimal, f"%{concepto}%")
            )
            conexion.commit()

            # Verificar cuántas filas fueron afectadas
            if cursor.rowcount > 0:
                page.snack_bar = ft.SnackBar(ft.Text(f"Precio actualizado para el producto '{concepto}'."), open=True)
            else:
                page.snack_bar = ft.SnackBar(ft.Text("No se encontró el producto o no se pudo actualizar el precio."), open=True)

            page.update()

        except Error as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error al actualizar el precio: {ex}"), open=True)
            page.update()

        finally:
            cursor.close()
            conexion.close()


    conceptos_disponibles = obtener_conceptos()

    titulo = ft.Container(
        content=ft.Text("Sistema de Facturación", size=30, weight=ft.FontWeight.BOLD),
        alignment=ft.alignment.center,
        padding=ft.padding.only(bottom=20),
    )

    # Encabezados para los productos
   # Encabezados para los productos con margen superior
    encabezados_productos = ft.Container(
        content=ft.Row(
            [
                ft.Text("Concepto", width=150, weight=ft.FontWeight.BOLD),
                ft.Text("Precio Unitario", width=150, weight=ft.FontWeight.BOLD),
                ft.Text("Cantidad", width=100, weight=ft.FontWeight.BOLD),
                ft.Text("Total", width=100, weight=ft.FontWeight.BOLD),
            ]
        ),
        margin=ft.margin.only(top=20 ,left=15)
        
    )

    productos_lista.controls.append(encabezados_productos)

    concepto_input = ft.TextField(
        label="Escribe un Producto",
        on_change=actualizar_opciones_concepto,
        on_blur=ocultar_opciones_concepto,
        expand=True,
    )
    opciones_lista = ft.Column(visible=False)
    precio_unitario_input = ft.TextField(label="Precio unitario", width=150, read_only=True)
    cantidad_input = ft.TextField(label="Cantidad", width=100)
    agregar_btn = ft.ElevatedButton(
        "AGREGAR PRODUCTO", on_click=agregar_producto, style=ft.ButtonStyle(text_style=ft.TextStyle(size=16))
    )
    total_text = ft.Text("Total: $0.00", size=20, weight=ft.FontWeight.BOLD)

    generar_factura_btn = ft.Container(
        content=ft.Column(
            [total_text, ft.ElevatedButton("GENERAR FACTURA", on_click=guardar_pdf, style=ft.ButtonStyle(text_style=ft.TextStyle(size=16)))],
        ),
        alignment=ft.alignment.center,
        padding=ft.margin.only(top=100),
    )
    def toggle_contenedor(e):
        contenedor.visible = not contenedor.visible  # Cambia la visibilidad del contenedor
        titulo2.visible = not titulo2.visible  # Cambia la visibilidad de titulo2 al mismo tiempo
        titulo_buscar.visible = not titulo_buscar.visible  # Cambia la visibilidad de titulo_buscar al mismo tiempo
        busqueda_container.visible = not busqueda_container.visible  # Cambia la visibilidad de busqueda_container al mismo tiempo
        tabla_resultados.visible = not tabla_resultados.visible  # Cambia la visibilidad de tabla_resultados al mismo tiempo
        e.page.update()  # Actualiza la página para reflejar el cambio

    # Definir titulo2
    titulo2 = ft.Container(
        content=ft.Text("Registro de Nuevos Productos", size=30, weight=ft.FontWeight.BOLD),
        alignment=ft.alignment.center,
        margin=ft.margin.only(top=30),
        visible=False  # Inicialmente oculto
    )

    # Definir el contenedor
    producto = ft.TextField(label="Ingresa el nombre del producto", expand=True)
    precio = ft.TextField(label="Ingresa el precio unitario", width=270)
    add = ft.ElevatedButton("Adiccionar Producto", width=150, on_click=add_producto)

    contenedor = ft.Container(
        content=ft.Row(
            controls=[producto, precio, add],
            spacing=10,
            alignment="start"
        ),
        margin=ft.margin.only(top=40),
        padding=ft.padding.all(10),
        visible=False  # Inicialmente oculto
    )

    # Crear interfaz de usuario
    titulo_buscar = ft.Container(
        content=ft.Text("Actualizar Precios de Productos", size=30, weight=ft.FontWeight.BOLD),
        alignment=ft.alignment.center,
        margin=ft.margin.only(top=30),
        visible=False
    )

    opciones_busqueda = ft.Column(visible=False)

    tabla_resultados.visible = False

    buscar_input = ft.TextField(label="Buscar producto", expand=True,on_change=actualizar_opciones_busqueda,  # Actualiza las opciones dinámicamenteon_blur=lambda e: opciones_busqueda.visible = False  # Oculta al salir del campo)
    )
    precios = ft.TextField(label="Nuevo Precio Unitario", width=200  # Actualiza las opciones dinámicamenteon_blur=lambda e: opciones_busqueda.visible = False  # Oculta al salir del campo)
    )
    buscar_btn = ft.ElevatedButton("Actualizar Precio", on_click=actualizar_precio_producto)

    busqueda_container = ft.Container(
        content=ft.Row(
            controls=[
                buscar_input,
                precios,
                buscar_btn,
            ],
            spacing=10,  # Espaciado entre los controles
            alignment="start"  # Alinea los elementos al inicio
        ),
        margin=ft.margin.only(top=40),  # Márgenes para el Container
        padding=ft.padding.all(10),  # Padding alrededor del Container
        visible=False  # Inicialmente oculto
    )

    # Botón para mostrar/ocultar el contenedor
    mostrar_button = ft.ElevatedButton("Mostrar o Ocultar Las otras opciones", on_click=toggle_contenedor)

    page.add(
        ft.Column(
            [
                titulo,
                ft.Row(
                    [concepto_input, precio_unitario_input, cantidad_input, agregar_btn]
                ),
                opciones_lista,
                productos_lista,
                generar_factura_btn,
                titulo2,
                contenedor,
                mostrar_button,
                titulo_buscar,
                busqueda_container,
                opciones_busqueda,
                tabla_resultados
            ],
            expand=True,
        )
    )



ft.app(target=main)
