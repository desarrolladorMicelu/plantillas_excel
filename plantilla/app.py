import datetime
import io
import os
import uuid
from openpyxl import load_workbook
import pyodbc
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from flask import Flask, jsonify, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UUID, create_engine, insert
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import logging



logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['SQLALCHEMY_BINDS'] = {
    #'db2':'postgresql://postgres:WeLZnkiKBsfVFvkaRHWqfWtGzvmSnOUn@viaduct.proxy.rlwy.net:35149/railway',
    'db3':'postgresql://postgres:vWUiwzFrdvcyroebskuHXMlBoAiTfgzP@junction.proxy.rlwy.net:47834/railway'
}
 
db = SQLAlchemy()
db.init_app(app)

class Excel1(db.Model):
    __bind_key__ = 'db3'
    __tablename__ = 'Excel1'
    __table_args__ = {'schema': 'excel_productos'}

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    tipo = db.Column(db.String(255))
    sku = db.Column(db.String)
    nombre = db.Column(db.String)
    publicado = db.Column(db.String)  
    esta_destacado = db.Column(db.String)
    visibilidad_en_el_catalogo = db.Column(db.String)
    descripcion_corta= db.Column(db.String)
    descripcion = db.Column(db.Text) 
    dia_en_que_empieza_el_precio_rebajado = db.Column(db.Date, nullable=True)
    dia_en_que_termina_el_precio_rebajado = db.Column(db.Date, nullable=True)
    estado_del_impuesto = db.Column(db.String)
    clase_de_impuesto = db.Column(db.String)
    en_inventario=db.Column(db.String)
    inventario=db.Column(db.String)
    cantidad_de_bajo_inventario = db.Column(db.Integer)
    permitir_reservas_de_productos_agotados = db.Column(db.String) 
    vendido_individualmente = db.Column(db.String)  
    peso_kg = db.Column(db.String)
    longitud_cm = db.Column(db.String)
    anchura_cm = db.Column(db.String)
    altura_cm = db.Column(db.String)
    permitir_valoraciones_de_clientes = db.Column(db.String) 
    nota_de_compra = db.Column(db.Text)
    precio_rebajado = db.Column(db.String)
    precio_normal = db.Column(db.String)
    categorias = db.Column(db.String)
    etiquetas = db.Column(db.String)
    clase_de_envio = db.Column(db.String)
    imagenes = db.Column(db.Text)
    limite_de_descargas = db.Column(db.Integer)
    dias_de_caducidad_de_la_descarga = db.Column(db.Integer)
    superior = db.Column(db.String)
    productos_agrupados = db.Column(db.String)
    ventas_dirigidas = db.Column(db.String)
    ventas_cruzadas = db.Column(db.String)
    url_externa = db.Column(db.String)
    texto_del_boton = db.Column(db.String)
    posicion = db.Column(db.String)
    nombre_del_atributo_1 = db.Column(db.String)
    valores_del_atributo_1 = db.Column(db.String)
    atributo_visible_1 = db.Column(db.String)
    atributo_global_1 = db.Column(db.String)
    nombre_del_atributo_2 = db.Column(db.String)
    valores_del_atributo_2 = db.Column(db.String)
    atributo_visible_2 = db.Column(db.String)
    atributo_global_2 = db.Column(db.String)
    nombre_del_atributo_3 = db.Column(db.String)
    valores_del_atributo_3 = db.Column(db.String)
    atributo_visible_3 = db.Column(db.String)
    atributo_global_3 = db.Column(db.String)
    nombre_del_atributo_4 = db.Column(db.String)
    valores_del_atributo_4 = db.Column(db.String)
    atributo_visible_4 = db.Column(db.String)
    atributo_global_4 = db.Column(db.String)    
    

class Excel2(db.Model): #falabella
    __bind_key__ = 'db3'
    __tablename__ = 'Excel2'
    __table_args__ = {'schema': 'excel_productos'}

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    nombre = db.Column(db.String)
    marca = db.Column(db.String)
    modelo = db.Column(db.String)
    descripcion = db.Column(db.String)
    categoria_primaria = db.Column(db.String)
    pais_de_produccion = db.Column(db.String)
    codigo_de_barras=db.Column(db.String)
    sku_del_vendedor = db.Column(db.String)
    variacion = db.Column(db.String)
    tax_percentage = db.Column(db.String)
    quantity_falabella = db.Column(db.String, nullable=True)
    price_falabella = db.Column(db.String)
    sale_price_falabella = db.Column(db.String)
    sale_start_date_falabella = db.Column(db.String)
    sale_end_date_falabella = db.Column(db.String)
    generacion = db.Column(db.String)
    camara_posterior = db.Column(db.String)
    capacidad_de_almacenamiento = db.Column(db.String)
    marca_procesador = db.Column(db.String)
    sistema_operativo = db.Column(db.String)
    capacidad_de_la_bateria_en_mah = db.Column(db.String,nullable=True)
    incluye_cargador = db.Column(db.String)
    tamano_de_la_pantalla = db.Column(db.String)
    ano_fabricacion = db.Column(db.String, nullable=True)
    conectividad_celular = db.Column(db.String)
    duracion_en_condiciones_previsibles_de_uso = db.Column(db.String)
    plazo_de_disponibilidad_de_repuestos = db.Column(db.String)
    procesador_especifico_txt = db.Column(db.String)
    resistente_al_agua = db.Column(db.String)
    memoria_expandible = db.Column(db.String)
    memoria_ram = db.Column(db.String)
    sistema_operativo_especifico = db.Column(db.String)
    autonomia = db.Column(db.String)
    camara_frontal = db.Column(db.String)
    caracteristicas = db.Column(db.String)
    caracteristicas_de_la_pantalla = db.Column(db.String)
    color = db.Column(db.String)
    conectividad_conexion = db.Column(db.String)
    dimensiones = db.Column(db.String)
    nucleos_del_procesador = db.Column(db.String, nullable=True)
    proveedor_de_servicio_compania = db.Column(db.String)
    ranura_para_sim = db.Column(db.String)
    requiere_imei = db.Column(db.String)
    requiere_serial_number = db.Column(db.String)
    resolucion_de_pantalla = db.Column(db.String)
    sello_sec = db.Column(db.String)
    tamano_de_sim = db.Column(db.String)
    tiempo_de_carga = db.Column(db.String)
    tipo_de_celular = db.Column(db.String)
    velocidad_de_imagen = db.Column(db.String)
    velocidad_de_procesamiento_ghz = db.Column(db.String)
    condicion_del_producto = db.Column(db.String)
    garantia_del_producto = db.Column(db.String)
    garantia_del_vendedor = db.Column(db.String)
    contenido_del_paquete = db.Column(db.Text)
    ancho_del_paquete = db.Column(db.String)
    largo_del_paquete = db.Column(db.String)
    alto_del_paquete = db.Column(db.String)
    peso_del_paquete = db.Column(db.String)
    imagen_principal = db.Column(db.String)
    imagen2 = db.Column(db.String)
    imagen3 = db.Column(db.String)
    imagen4 = db.Column(db.String)
    imagen5 = db.Column(db.String)
    imagen6 = db.Column(db.String)
    imagen7 = db.Column(db.String)
    imagen8 = db.Column(db.String) 
    

class Excel3(db.Model): #bancolombia
    __bind_key__ = 'db3'
    __tablename__ = 'Excel3'
    __table_args__ = {'schema': 'excel_productos'}

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    validacion = db.Column(db.String)
    product_id = db.Column(db.String)
    nombre = db.Column(db.String)
    precio_impuestos_incluidos = db.Column(db.String)
    porcentaje_de_descuento = db.Column(db.String)
    referencia_n = db.Column(db.String)
    ean13 = db.Column(db.String)
    upc = db.Column(db.String)
    altura_cm = db.Column(db.String)
    anchura_cm = db.Column(db.String)
    profundidad_cm = db.Column(db.String)
    peso_kg = db.Column(db.String)
    cantidad = db.Column(db.Integer, nullable=True)
    resumen_max_800_caracteres = db.Column(db.String(800))
    descripcion = db.Column(db.Text)
    urls_de_la_imagen = db.Column(db.Text)
    producto = db.Column(db.String)
    marca = db.Column(db.String)
    tienda = db.Column(db.String)
    caracteristicas_extras = db.Column(db.Text)
    caracteristicas = db.Column(db.Text)
    
class Excel4(db.Model): #exito
    __bind_key__ = 'db3'
    __tablename__ = 'Excel4'
    __table_args__ = {'schema': 'excel_productos'}

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    grupo_ean_combo = db.Column(db.String)
    ean = db.Column(db.String)
    nombre_del_producto = db.Column(db.String)
    categoria = db.Column(db.String)
    marca = db.Column(db.String)
    descripcion = db.Column(db.String)
    palabras_clave = db.Column(db.String)
    alto_del_empaque = db.Column(db.String)
    largo_del_empaque = db.Column(db.String)
    ancho_del_empaque = db.Column(db.String)
    peso_del_empaque = db.Column(db.String)
    sku_shippingsize = db.Column(db.String)
    alto_del_producto = db.Column(db.String)
    largo_del_producto = db.Column(db.String)
    ancho_del_producto = db.Column(db.String)
    peso_del_producto = db.Column(db.String)
    descripcion_unidad_de_medida = db.Column(db.String)
    factor_de_conversion = db.Column(db.String)
    tipo_producto = db.Column(db.String)
    url_de_imagen_1 = db.Column(db.String)
    url_de_imagen_2 = db.Column(db.String)
    url_de_imagen_3 = db.Column(db.String)
    url_de_imagen_4 = db.Column(db.String)
    url_de_imagen_5 = db.Column(db.String)
    url_video_youtube = db.Column(db.String)
    logistica_exito = db.Column(db.String)
    camara_principal = db.Column(db.String)
    memoria_del_sistema_ram = db.Column(db.String)
    red = db.Column(db.String)
    tamano_de_pantalla = db.Column(db.String)
    capacidad_de_almacenamiento = db.Column(db.String)
    tiempo_de_carga = db.Column(db.String)
    tamano_sim = db.Column(db.String)
    camara_frontal = db.Column(db.String)
    dual_sim = db.Column(db.String)
    tipo_de_camara_principal = db.Column(db.String)
    accesorios = db.Column(db.String)
    tipo_de_pantalla = db.Column(db.String)
    sistema_operativo = db.Column(db.String)
    radio = db.Column(db.String)
    altavoz = db.Column(db.String)
    rango_tamano_de_pantalla = db.Column(db.String)
    rango_bateria = db.Column(db.String)

class Falabella_Maestra(db.Model): #falabellamaestra
    __bind_key__ = 'db3'
    __tablename__ = 'Marca'
    __table_args__ = {'schema': 'excel_productos'}  
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    marca = db.Column(db.String)
    paisdeproduccion = db.Column(db.String)
    taxpercentage = db.Column(db.String)
    generacion = db.Column(db.String)
    camaraposterior = db.Column(db.String)
    capacidadalmacenamiento = db.Column(db.String)
    marcaprocesador = db.Column(db.String)
    sistemaoperativo = db.Column(db.String)
    conectividadcelular = db.Column(db.String)
    resistenteagua = db.Column(db.String)
    memoriaexpandible = db.Column(db.String)
    sistemaoperativoespecifico = db.Column(db.String)
    camarafrontal = db.Column(db.String)
    caracteristicas = db.Column(db.Text)
    caracteristicaspantallas = db.Column(db.String)
    conectividadconexion = db.Column(db.String)
    nucleoprocesador = db.Column(db.Integer)
    proveedorservicio = db.Column(db.String)
    ranurapasim = db.Column(db.String)
    requiereImei = db.Column(db.String)
    resolucionpantalla = db.Column(db.String)
    tamanosim = db.Column(db.String)
    tipocelular = db.Column(db.String)
    velocidadimagen = db.Column(db.String)
    condicionproducto = db.Column(db.String)
    garantia_del_vendedor = db.Column(db.String)
    categoriaprimaria=db.Column(db.String)
    incluyecargador=db.Column(db.String)
    memoriaram=db.Column(db.String)
    requiere_serial_number=db.Column(db.String)
    
class Exito_Maestra(db.Model): #exitoamaestra
    __bind_key__ = 'db3'
    __tablename__ = 'Exito'
    __table_args__ = {'schema': 'excel_productos'}  
    Id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    categoria=db.Column(db.String)
    marca=db.Column(db.String)
    descripcionunidad=db.Column(db.String)
    tipoproducto=db.Column(db.String)
    camaraprincipal=db.Column(db.String)
    memoriasistemaram=db.Column(db.String)
    red=db.Column(db.String)
    tamanodepantalla=db.Column(db.String)
    capacidadalmacenamiento=db.Column(db.String)
    tamanosim=db.Column(db.String)
    camarafrontal=db.Column(db.String)
    dualsim=db.Column(db.String)
    tipocamaraprincipal=db.Column(db.String)
    tipodepantalla=db.Column(db.String)
    radio=db.Column(db.String)
    altavoz=db.Column(db.String)
    rangotamano=db.Column(db.String)
    rangobateria=db.Column(db.String)
    sistemaoperativo=db.Column(db.String)
        

@app.route('/')
def index():
    celulares = Excel1.query.filter(Excel1.tipo == 'variable').all()
    celulares_falabella = Excel2.query.all() 
    celulares_bancolombia = Excel3.query.all()
    celulares_exito = Excel4.query.all()
    return render_template('plantilla.html', celulares=celulares, celulares_falabella=celulares_falabella,celulares_bancolombia=celulares_bancolombia,celulares_exito=celulares_exito)

@app.route('/crear_producto', methods=['POST'])
def crear_producto():
    try:
        datos = request.json
        logging.info(f"Received data: {datos}")
        
        plataforma = datos.pop('plataforma', None)
        if not plataforma:
            return jsonify({"error": "Plataforma no especificada"}), 400
        
        platform_models = {
            'micelu': Excel1,
            'bancolombia': Excel3,
            'falabella': Excel2,
            'exito': Excel4
        }
        
        ModelClass = platform_models.get(plataforma)
        if not ModelClass:
            return jsonify({"error": f"Plataforma no válida: {plataforma}"}), 400
        
        # Remove any fields that are not in the model
        valid_fields = set(ModelClass.__table__.columns.keys())
        datos_filtrados = {k: v for k, v in datos.items() if k in valid_fields}
        
        # Convert empty strings to None
        for key, value in datos_filtrados.items():
            if value == '':
                datos_filtrados[key] = None
        
        logging.info(f"Filtered data for {plataforma}: {datos_filtrados}")
        
        nuevo_producto = ModelClass(**datos_filtrados)
        db.session.add(nuevo_producto)
        db.session.commit()
        
        return jsonify({"message": f"Producto creado exitosamente en {plataforma}", "id": nuevo_producto.id}), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Database error: {str(e)}")
        return jsonify({"error": "Error de base de datos: " + str(e)}), 400
    
    except Exception as e:
        db.session.rollback()
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "Error inesperado: " + str(e)}), 500

@app.route('/get_variations/<string:sku>')
def get_variations(sku):
    parent = Excel1.query.filter_by(sku=sku, tipo='variable').first()
    if parent:
        variations = Excel1.query.filter_by(superior=parent.sku, tipo='variation').all()
        return jsonify([
            {
                'id': parent.id,
                'sku': parent.sku,
                'nombre': parent.nombre,
                'descripcion': parent.descripcion,  # Add description for parent
                'is_parent': True
            }
        ] + [
            {
                'id': v.id,
                'sku': v.sku,
                'nombre': v.nombre,
                'descripcion': parent.descripcion,  # Use parent's description for variations
                'is_parent': False
            } for v in variations
        ])
    return jsonify([])


@app.route('/descargar_micelu', methods=['POST'])
def descargar_micelu():
    try:
        selected_skus = request.json.get('skus', [])
        
        print(f"SKUs recibidos: {selected_skus}")  # Log para debugging
        
        if not selected_skus:
            return jsonify({"error": "No se seleccionaron SKUs"}), 400

        # Obtener los productos seleccionados
        products = Excel1.query.filter(Excel1.sku.in_(selected_skus)).all()

        print(f"Productos encontrados: {len(products)}")  # Log para debugging

        if not products:
            return jsonify({"error": "No se encontraron productos con los SKUs seleccionados"}), 404

        # Crear un DataFrame con la información de los productos
        data = []
        for product in products:
            parent = Excel1.query.filter_by(sku=product.superior, tipo='variable').first() if product.tipo == 'variation' else product
            row = {
                'id': "",
                'Tipo': product.tipo,
                'SKU': product.sku,
                'Nombre': product.nombre,
                'Publicado': product.publicado,
                '¿Está destacado?': product.esta_destacado,
                'Visibilidad en el catálogo': product.visibilidad_en_el_catalogo,
                'Descripción corta': parent.descripcion_corta,
                'Descripción': parent.descripcion, 
                'Día en que empieza el precio rebajado': product.dia_en_que_empieza_el_precio_rebajado,
                'Día en que termina el precio rebajado': product.dia_en_que_termina_el_precio_rebajado,
                'Estado del impuesto': product.estado_del_impuesto,
                'Clase de impuesto': product.clase_de_impuesto,
                '¿En inventario?':product.en_inventario,
                'Inventario':product.inventario,
                'Cantidad de bajo inventario': product.cantidad_de_bajo_inventario,
                '¿Permitir reservas de productos agotados?': product.permitir_reservas_de_productos_agotados,
                '¿Vendido individualmente?': product.vendido_individualmente,
                'Peso (kg)': product.peso_kg,
                'Longitud (cm)': product.longitud_cm,
                'Anchura (cm)': product.anchura_cm,
                'Altura (cm)': product.altura_cm,
                '¿Permitir valoraciones de clientes?': product.permitir_valoraciones_de_clientes,
                'Nota de compra': product.nota_de_compra,
                'Precio rebajado': product.precio_rebajado,
                'Precio normal': product.precio_normal,
                'Categorías': product.categorias,
                'Etiquetas': product.etiquetas,
                'Clase de envío': product.clase_de_envio,
                'Imágenes': product.imagenes,
                'Límite de descargas': product.limite_de_descargas,
                'Días de caducidad de la descarga': product.dias_de_caducidad_de_la_descarga,
                'Superior': product.superior,
                'Productos agrupados': product.productos_agrupados,
                'Ventas dirigidas': product.ventas_dirigidas,
                'Ventas cruzadas': product.ventas_cruzadas,
                'URL externa': product.url_externa,
                'Texto del botón': product.texto_del_boton,
                'Posición': product.posicion,
                'Nombre del atributo 1': product.nombre_del_atributo_1,
                'Valores del atributo 1': product.valores_del_atributo_1,
                'Atributo visible 1': product.atributo_visible_1,
                'Atributo global 1': product.atributo_global_1,
                'Nombre del atributo 2': product.nombre_del_atributo_2,
                'Valores del atributo 2': product.valores_del_atributo_2,
                'Atributo visible 2': product.atributo_visible_2,
                'Atributo global 2': product.atributo_global_2,
                'Nombre del atributo 3': product.nombre_del_atributo_3,
                'Valores del atributo 3': product.valores_del_atributo_3,
                'Atributo visible 3': product.atributo_visible_3,
                'Atributo global 3': product.atributo_global_3,
                'Nombre del atributo 4': product.nombre_del_atributo_4,
                'Valores del atributo 4': product.valores_del_atributo_4,
                'Atributo visible 4': product.atributo_visible_4,
                'Atributo global 4': product.atributo_global_4,
            }
            data.append(row)

        df = pd.DataFrame(data)

        # Crear un objeto BytesIO para guardar el archivo Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Celulares Master')

        output.seek(0)

        # Enviar el archivo como respuesta
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='productos_micelu.xlsx'
        )

    except Exception as e:
        print(f"Error en descargar_micelu: {str(e)}")  # Log para debugging
        return jsonify({"error": str(e)}), 500
    


@app.route('/descargar_falabella', methods=['POST'])
def descargar_falabella():
    try:
        
        data = request.json
        selected_skus = data.get('skus', [])
        
        products = Excel2.query.all()

        if not products:
            return jsonify({"error": "No se encontraron productos de Falabella"}), 404

        data = []
        for product in products:
            if product.sku_del_vendedor in selected_skus:
                row = {
                    'Nombre ': product.nombre,
                    'Marca': product.marca,
                    'Modelo': product.modelo,
                    'Descripción': product.descripcion,
                    'Categoría primaria': product.categoria_primaria,
                    'País de producción': product.pais_de_produccion,
                    'Código de barras': product.codigo_de_barras,
                    'SKU del vendedor': product.sku_del_vendedor,
                    'Variación': product.variacion,
                    'TaxPercentage': product.tax_percentage,
                    'QuantityFalabella': product.quantity_falabella,
                    'PriceFalabella': product.price_falabella,
                    'SalePriceFalabella': product.sale_price_falabella,
                    'SaleStartDateFalabella': product.sale_start_date_falabella,
                    'SaleEndDateFalabella': product.sale_end_date_falabella,
                    'Generacion': product.generacion,
                    'CamaraPosterior': product.camara_posterior,
                    'CapacidadDeAlmacenamiento': product.capacidad_de_almacenamiento,
                    'MarcaProcesador': product.marca_procesador,
                    'SistemaOperativo': product.sistema_operativo,
                    'CapacidadDeLaBateriaEnMah': product.capacidad_de_la_bateria_en_mah,
                    'IncluyeCargador': product.incluye_cargador,
                    'TamanoDeLaPantalla': product.tamano_de_la_pantalla,
                    'AnoFabricacion': product.ano_fabricacion,
                    'ConectividadCelular': product.conectividad_celular,
                    'DuracionEnCondicionesPrevisiblesDeUso': product.duracion_en_condiciones_previsibles_de_uso,
                    'PlazoDeDisponibilidadDeRepuestos': product.plazo_de_disponibilidad_de_repuestos,
                    'ProcesadorEspecificoTxt': product.procesador_especifico_txt,
                    'ResistenteAlAgua': product.resistente_al_agua,
                    'MemoriaExpandible': product.memoria_expandible,
                    'MemoriaRam': product.memoria_ram,
                    'SistemaOperativoEspecifico': product.sistema_operativo_especifico,
                    'Autonomia': product.autonomia,
                    'CamaraFrontal': product.camara_frontal,
                    'Caracteristicas': product.caracteristicas,
                    'CaracteristicasDeLaPantalla': product.caracteristicas_de_la_pantalla,
                    'Color #1532': product.color,
                    'ConectividadConexion': product.conectividad_conexion,
                    'Dimensiones': product.dimensiones,
                    'NucleosDelProcesador': product.nucleos_del_procesador,
                    'ProveedorDeServicioCompania': product.proveedor_de_servicio_compania,
                    'RanuraParaSim': product.ranura_para_sim,
                    'RequiereImei': product.requiere_imei,
                    'RequiereSerialNumber': product.requiere_serial_number,
                    'ResolucionDePantalla': product.resolucion_de_pantalla,
                    'SelloSec': product.sello_sec,
                    'TamanoDeSim #1530': product.tamano_de_sim,
                    'TiempoDeCarga': product.tiempo_de_carga,
                    'TipoDeCelular': product.tipo_de_celular,
                    'VelocidadDeImagen': product.velocidad_de_imagen,
                    'VelocidadDeProcesamientoGhz': product.velocidad_de_procesamiento_ghz,
                    'Condición del Producto': product.condicion_del_producto,
                    'Garantía del producto': product.garantia_del_producto,
                    'Garantía del vendedor': product.garantia_del_vendedor,
                    'Contenido del paquete': product.contenido_del_paquete,
                    'Ancho del paquete': product.ancho_del_paquete,
                    'Largo del paquete': product.largo_del_paquete,
                    'Alto del paquete': product.alto_del_paquete,
                    'Peso del paquete': product.peso_del_paquete,
                    'Imagen principal': product.imagen_principal,
                    'Imagen2': product.imagen2,
                    'Imagen3': product.imagen3,
                    'Imagen4': product.imagen4,
                    'Imagen5': product.imagen5,
                    'Imagen6': product.imagen6,
                    'Imagen7': product.imagen7,
                    'Imagen8': product.imagen8
                }
                data.append(row)

        df = pd.DataFrame(data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Subir Plantilla')

        output.seek(0)

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='productos_falabella.xlsx'
        )

    except Exception as e:
        print(f"Error en descargar_falabella: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/descargar_bancolombia', methods=['POST'])
def descargar_bancolombia():
    try:
        data = request.json
        selected_ids = data.get('ids', [])
        
        products = Excel3.query.filter(Excel3.product_id.in_(selected_ids)).all()

        if not products:
            return jsonify({"error": "No se encontraron productos de Bancolombia"}), 404

        data = []
        for product in products:
            row = {
                'Validación': product.validacion,
                'Product_ID': product.product_id,
                'Nombre': product.nombre,
                'Precio impuestos incluidos': product.precio_impuestos_incluidos,
                'Porcentaje de descuento': product.porcentaje_de_descuento,
                'Referencia n°': product.referencia_n,
                'EAN13': product.ean13,
                'UPC': product.upc,
                'Altura cm': product.altura_cm,
                'Anchura cm': product.anchura_cm,
                'Profundidad cm': product.profundidad_cm,
                'Peso KG': product.peso_kg,
                'Cantidad': product.cantidad,
                'Resumen (Max 800 caracteres)': product.resumen_max_800_caracteres,
                'Descripcion': product.descripcion,
                'URLs de la imagen (x,y,z...)': product.urls_de_la_imagen,
                'Producto': product.producto,
                'Marca': product.marca,
                'Tienda': product.tienda,
                'Caracteristicas extras': product.caracteristicas_extras,
                'Caracteristicas': product.caracteristicas
            }
            data.append(row)

        df = pd.DataFrame(data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Carga Productos Nuevos')

        output.seek(0)

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='productos_bancolombia.xlsx'
        )

    except Exception as e:
        print(f"Error en descargar_bancolombia: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/descargar_exito', methods=['POST'])
def descargar_exito():
    try:
        data = request.json
        selected_eans = data.get('eans', [])
        
        products = Excel4.query.all()

        if not products:
            return jsonify({"error": "No se encontraron productos de Éxito"}), 404

        data = []
        for product in products:
            if product.ean in selected_eans:
                row = {
                    'Grupo EAN Combo': product.grupo_ean_combo,
                    'EAN': product.ean,
                    'Nombre del producto': product.nombre_del_producto,
                    'Categoria': product.categoria,
                    'Marca': product.marca,
                    'Descripcion': f"<p>{product.descripcion}</p>",
                    'Palabras clave': product.palabras_clave,
                    'Alto del empaque': product.alto_del_empaque,
                    'Largo del empaque': product.largo_del_empaque,
                    'Ancho del empaque': product.ancho_del_empaque,
                    'Peso del empaque': product.peso_del_empaque,
                    'skuShippingsize': product.sku_shippingsize,
                    'Alto del producto': product.alto_del_producto,
                    'Largo del producto': product.largo_del_producto,
                    'Ancho del producto': product.ancho_del_producto,
                    'Peso del producto': product.peso_del_producto,
                    'Descripcion Unidad de Medida': product.descripcion_unidad_de_medida,
                    'Factor de conversion': product.factor_de_conversion,
                    'TipoProducto': product.tipo_producto,
                    'URL de Imagen 1': product.url_de_imagen_1,
                    'URL de Imagen 2': product.url_de_imagen_2,
                    'URL de Imagen 3': product.url_de_imagen_3,
                    'URL de Imagen 4': product.url_de_imagen_4,
                    'URL de Imagen 5': product.url_de_imagen_5,
                    'URL Video YouTube': product.url_video_youtube,
                    'Logistica Exito': product.logistica_exito,
                    'Cámara Principal': product.camara_principal,
                    'Memoria del Sistema Ram': product.memoria_del_sistema_ram,
                    'Red': product.red,
                    'Tamaño de Pantalla': product.tamano_de_pantalla,
                    'Capacidad de almacenamiento': product.capacidad_de_almacenamiento,
                    'Tiempo de carga': product.tiempo_de_carga,
                    'Tamaño SIM': product.tamano_sim,
                    'Cámara frontal': product.camara_frontal,
                    'Dual Sim': product.dual_sim,
                    'Tipo de Cámara Principal': product.tipo_de_camara_principal,
                    'Accesorios': product.accesorios,
                    'Tipo de pantalla': product.tipo_de_pantalla,
                    'Sistema Operativo': product.sistema_operativo,
                    'Radio': product.radio,
                    'Altavoz': product.altavoz,
                    'Rango Tamaño de Pantalla': product.rango_tamano_de_pantalla,
                    'Rango Bateria': product.rango_bateria
                }
                data.append(row)

        df = pd.DataFrame(data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Productos Éxito')

        output.seek(0)

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='productos_exito.xlsx'
        )

    except Exception as e:
        print(f"Error en descargar_exito: {str(e)}")
        return jsonify({"error": str(e)}), 500
    


 
@app.route('/get_falabella_fields')
def get_falabella_fields():
    try:
        # 1. Realizar una única consulta que obtenga todos los campos necesarios
        fields_query = db.session.query(
            Falabella_Maestra.marca,
            Falabella_Maestra.paisdeproduccion,
            Falabella_Maestra.taxpercentage,
            Falabella_Maestra.generacion,
            Falabella_Maestra.camaraposterior,
            Falabella_Maestra.capacidadalmacenamiento,
            Falabella_Maestra.marcaprocesador,
            Falabella_Maestra.sistemaoperativo,
            Falabella_Maestra.conectividadcelular,
            Falabella_Maestra.resistenteagua,
            Falabella_Maestra.memoriaexpandible,
            Falabella_Maestra.sistemaoperativoespecifico,
            Falabella_Maestra.camarafrontal,
            Falabella_Maestra.caracteristicas,
            Falabella_Maestra.caracteristicaspantallas,
            Falabella_Maestra.conectividadconexion,
            Falabella_Maestra.nucleoprocesador,
            Falabella_Maestra.proveedorservicio,
            Falabella_Maestra.ranurapasim,
            Falabella_Maestra.requiereImei,
            Falabella_Maestra.resolucionpantalla,
            Falabella_Maestra.tamanosim,
            Falabella_Maestra.tipocelular,
            Falabella_Maestra.velocidadimagen,
            Falabella_Maestra.condicionproducto,
            Falabella_Maestra.garantia_del_vendedor,
            Falabella_Maestra.categoriaprimaria,
            Falabella_Maestra.incluyecargador,
            Falabella_Maestra.memoriaram,
            Falabella_Maestra.requiere_serial_number
        ).distinct()
 
        # 2. Crear un diccionario para almacenar los resultados
        response = {
            'marca': set(),
            'paisdeproduccion': set(),
            'taxpercentage': set(),
            'generacion': set(),
            'camaraposterior': set(),
            'capacidadalmacenamiento': set(),
            'marcaprocesador': set(),
            'sistemaoperativo': set(),
            'conectividadcelular': set(),
            'resistenteagua': set(),
            'memoriaexpandible': set(),
            'sistemaoperativoespecifico': set(),
            'camarafrontal': set(),
            'caracteristicas': set(),
            'caracteristicaspantallas': set(),
            'conectividadconexion': set(),
            'nucleoprocesador': set(),
            'proveedorservicio': set(),
            'ranurapasim': set(),
            'requiereImei': set(),
            'resolucionpantalla': set(),
            'tamanosim': set(),
            'tipocelular': set(),
            'velocidadimagen': set(),
            'condicionproducto': set(),
            'garantia_del_vendedor': set(),
            'categoriaprimaria': set(),
            'incluyecargador': set(),
            'memoriaram': set(),
            'requiere_serial_number': set()
        }
 
        # 3. Procesar los resultados en memoria
        for row in fields_query.all():
            for idx, value in enumerate(row):
                if value is not None:
                    field_name = list(response.keys())[idx]
                    response[field_name].add(value)
 
        # 4. Convertir sets a listas ordenadas
        return jsonify({field: sorted(list(values)) for field, values in response.items()})
 
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
    

@app.route('/get_exito_fields')
def get_exito_fields():
    try:
        # 1. Realizar una única consulta que obtenga todos los campos necesarios
        fields_query = db.session.query(
        Exito_Maestra.categoria,
        Exito_Maestra.marca,
        Exito_Maestra.descripcionunidad,
        Exito_Maestra.tipoproducto,
        Exito_Maestra.camaraprincipal,
        Exito_Maestra.memoriasistemaram,
        Exito_Maestra.red,
        Exito_Maestra.tamanodepantalla,
        Exito_Maestra.capacidadalmacenamiento,
        Exito_Maestra.tamanosim,
        Exito_Maestra.camarafrontal,
        Exito_Maestra.dualsim,
        Exito_Maestra.tipocamaraprincipal,
        Exito_Maestra.tipodepantalla,
        Exito_Maestra.radio,
        Exito_Maestra.altavoz,
        Exito_Maestra.rangotamano,
        Exito_Maestra.rangobateria,
        Exito_Maestra.sistemaoperativo
        ).distinct()
        
        
        response = {
        "categoria": set(),
        "marca": set(),
        "descripcionunidad": set(),
        "tipoproducto": set(),
        "camaraprincipal": set(),
        "memoriasistemaram": set(),
        "red": set(),
        "tamanodepantalla": set(),
        "capacidadalmacenamiento": set(),
        "tamanosim": set(),
        "camarafrontal": set(),
        "dualsim": set(),
        "tipocamaraprincipal": set(),
        "tipodepantalla": set(),
        "radio": set(),
        "altavoz": set(),
        "rangotamano": set(),
        "rangobateria": set(),     
        "sistemaoperativo":set(),
        }
        for row in fields_query.all():
            for idx, value in enumerate(row):
                if value is not None:
                    field_name = list(response.keys())[idx]
                    response[field_name].add(value)
 
        # 4. Convertir sets a listas ordenadas
        return jsonify({field: sorted(list(values)) for field, values in response.items()})
 
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
 
    
if __name__ == '__app__':
    app.run(port=os.getenv("PORT", default=5000))
 

    
