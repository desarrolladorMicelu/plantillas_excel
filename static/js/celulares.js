document.addEventListener('DOMContentLoaded', function() {
    const selectPlataforma = document.getElementById('plataforma');
    const miceluContent = document.getElementById('micelu-content');
    const selectCelulares = document.getElementById('celulares');
    const variacionesCheckboxes = document.getElementById('variaciones-checkboxes');
    const listaSeleccionados = document.getElementById('lista-seleccionados');
    const btnCrearProducto = document.getElementById('crear-producto');
    const selectPlataformaCrear = document.getElementById('plataforma-crear');
    const modalCrearProducto = document.getElementById('modal-crear-producto');
    const spanClose = modalCrearProducto.querySelector('.close');
    const formCrearProducto = document.getElementById('form-crear-producto');
    const descargarMiceluBtn = document.getElementById('descargar-micelu');
    let selectedItems = new Map();
    let parentDescription = '';
 
    selectPlataforma.addEventListener('change', function() {
        if (this.value === 'micelu') {
            miceluContent.style.display = 'block';
        } else {
            miceluContent.style.display = 'none';
            // Restablecer los otros campos si es necesario
            selectCelulares.value = '';
            variacionesCheckboxes.innerHTML = '';
            listaSeleccionados.innerHTML = '';
            selectedItems.clear();
        }
    });
 
    selectCelulares.addEventListener('change', function() {
        const selectedSku = this.value;
        if (selectedSku) {
            fetch(`/get_variations/${selectedSku}`)
                .then(response => response.json())
                .then(variations => {
                    variacionesCheckboxes.innerHTML = '';
                    variations.forEach(variation => {
                        if (variation.is_parent) {
                            parentDescription = variation.descripcion;
                        }
 
                        const checkbox = document.createElement('input');
                        checkbox.type = 'checkbox';
                        checkbox.id = variation.sku;
                        checkbox.value = JSON.stringify(variation);
                        checkbox.checked = selectedItems.has(variation.sku);
 
                        const label = document.createElement('label');
                        label.htmlFor = variation.sku;
                        label.textContent = `${variation.nombre} (SKU: ${variation.sku})`;
                        if (variation.is_parent) {
                            label.style.fontWeight = 'bold';
                        }
 
                        const div = document.createElement('div');
                        div.appendChild(checkbox);
                        div.appendChild(label);
 
                        variacionesCheckboxes.appendChild(div);
 
                        checkbox.addEventListener('change', function() {
                            if (this.checked) {
                                const variationData = JSON.parse(this.value);
                                variationData.descripcion = parentDescription;
                                selectedItems.set(variation.sku, variationData);
                            } else {
                                selectedItems.delete(variation.sku);
                            }
                            updateSelectedList();
                        });
                    });
                    updateSelectedList();
                })
                .catch(error => console.error('Error:', error));
        } else {
            variacionesCheckboxes.innerHTML = '';
        }
    });
 
    function updateSelectedList() {
        listaSeleccionados.innerHTML = '';
        selectedItems.forEach(item => {
            const li = document.createElement('li');
            li.className = 'selected-item';
 
            const itemText = document.createElement('span');
            itemText.textContent = `${item.nombre} (SKU: ${item.sku})`;
            li.appendChild(itemText);
 
            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = 'Eliminar';
            deleteBtn.className = 'delete-btn';
            deleteBtn.addEventListener('click', function() {
                selectedItems.delete(item.sku);
                updateSelectedList();
                updateCheckboxState(item.sku, false);
            });
            li.appendChild(deleteBtn);
 
            listaSeleccionados.appendChild(li);
        });
    }
 
    function updateCheckboxState(sku, checked) {
        const checkbox = document.getElementById(sku);
        if (checkbox) {
            checkbox.checked = checked;
        }
    }
 
    // Nuevo código para el modal de crear producto
 
 
    function generarFormulario(plataforma) {
        formCrearProducto.innerHTML = ''; // Limpiar el formulario existente
       
        let campos;
        switch(plataforma) {
            case 'micelu':
                campos = ['tipo', 'sku', 'nombre', 'publicado', 'esta_destacado', 'visibilidad_en_el_catalogo','descripcion_corta', 'descripcion', 'dia_en_que_empieza_el_precio_rebajado', 'dia_en_que_termina_el_precio_rebajado', 'estado_del_impuesto', 'clase_de_impuesto', 'en_inventario', 'inventario', 'cantidad_de_bajo_inventario', 'permitir_reservas_de_productos_agotados', 'vendido_individualmente', 'peso_kg', 'longitud_cm', 'anchura_cm', 'altura_cm', 'permitir_valoraciones_de_clientes', 'nota_de_compra', 'precio_rebajado', 'precio_normal', 'categorias', 'etiquetas', 'clase_de_envio', 'imagenes', 'limite_de_descargas', 'dias_de_caducidad_de_la_descarga', 'superior', 'productos_agrupados:', 'ventas_dirigidas:', 'ventas_cruzadas:', 'url_externa:', 'texto_del_boton:', 'posicion:'];
                break;
            case 'bancolombia':
                campos = ['validacion', 'product_id', 'nombre', 'precio_impuestos_incluidos', 'porcentaje_de_descuento', 'referencia_n', 'ean13', 'upc', 'altura_cm', 'anchura_cm', 'profundidad_cm', 'peso_kg', 'cantidad', 'resumen_max_800_caracteres', 'descripcion', 'urls_de_la_imagen', 'producto', 'marca', 'tienda', 'caracteristicas_extras', 'caracteristicas'];
                break;
            case 'falabella':
                campos = ['nombre', 'marca', 'modelo', 'descripcion', 'categoria_primaria', 'pais_de_produccion', 'codigo_de_barras', 'sku_del_vendedor', 'variacion', 'tax_percentage', 'quantity_falabella', 'price_falabella', 'sale_price_falabella', 'sale_start_date_falabella', 'sale_end_date_falabella', 'generacion', 'camara_posterior', 'capacidad_de_almacenamiento', 'marca_procesador', 'sistema_operativo', 'capacidad_de_la_bateria_en_mah', 'incluye_cargador', 'tamano_de_la_pantalla', 'ano_fabricacion', 'conectividad_celular', 'duracion_en_condiciones_previsibles_de_uso', 'plazo_de_disponibilidad_de_repuestos', 'procesador_especifico_txt', 'resistente_al_agua', 'memoria_expandible', 'memoria_ram', 'sistema_operativo_especifico', 'autonomia', 'camara_frontal', 'caracteristicas', 'caracteristicas_de_la_pantalla', 'color', 'conectividad_conexion', 'dimensiones', 'nucleos_del_procesador', 'proveedor_de_servicio_compania', 'ranura_para_sim', 'requiere_imei', 'requiere_serial_number', 'resolucion_de_pantalla', 'sello_sec', 'tamano_de_sim', 'tiempo_de_carga', 'tipo_de_celular', 'velocidad_de_imagen', 'velocidad_de_procesamiento_ghz', 'condicion_del_producto', 'garantia_del_producto', 'garantia_del_vendedor', 'contenido_del_paquete', 'ancho_del_paquete', 'largo_del_paquete', 'alto_del_paquete', 'peso_del_paquete', 'imagen_principal', 'imagen2', 'imagen3', 'imagen4', 'imagen5', 'imagen6', 'imagen7', 'imagen8'];
                break;
            case 'exito':
                campos = ['grupo_ean_combo', 'ean', 'nombre_del_producto', 'categoria', 'marca', 'descripcion', 'palabras_clave', 'alto_del_empaque', 'largo_del_empaque', 'ancho_del_empaque', 'peso_del_empaque', 'sku_shippingsize', 'alto_del_producto', 'largo_del_producto', 'ancho_del_producto', 'peso_del_producto', 'descripcion_unidad_de_medida', 'factor_de_conversion', 'tipo_producto', 'url_de_imagen_1', 'url_de_imagen_2', 'url_de_imagen_3', 'url_de_imagen_4', 'url_de_imagen_5', 'url_video_youtube', 'logistica_exito','camara_principal', 'memoria_del_sistema_ram', 'red', 'tamano_de_pantalla', 'capacidad_de_almacenamiento', 'tiempo_de_carga', 'tamano_sim', 'camara_frontal', 'dual_sim', 'tipo_de_camara_principal', 'accesorios', 'tipo_de_pantalla', 'sistema_operativo', 'radio', 'altavoz', 'rango_tamano_de_pantalla', 'rango_bateria'];
                break;
            default:
                campos = [];
        }
           
        
        function mapFieldName(campo, plataforma) {
            if (plataforma === 'exito') {
                const fieldMap = {
                    'categoria': 'categoria',
                    'marca': 'marca',
                    'descripcion_unidad_de_medida': 'descripcionunidad',
                    'tipo_producto': 'tipoproducto',
                    'camara_principal': 'camaraprincipal',
                    'memoria_del_sistema_ram': 'memoriasistemaram',
                    'red': 'red',
                    'tamano_de_pantalla': 'tamanodepantalla',
                    'capacidad_de_almacenamiento': 'capacidadalmacenamiento',
                    'tamano_sim': 'tamanosim',
                    'camara_frontal': 'camarafrontal',
                    'dual_sim': 'dualsim',
                    'tipo_de_camara_principal': 'tipocamaraprincipal',
                    'tipo_de_pantalla': 'tipodepantalla',
                    'radio': 'radio',
                    'altavoz': 'altavoz',
                    'rango_tamano_de_pantalla': 'rangotamano',
                    'rango_bateria': 'rangobateria',
                    'sistema_operativo': 'sistemaoperativo'
                };
                return fieldMap[campo] || campo;
            } else {
                const fieldMap = {
                    'capacidad_de_almacenamiento': 'capacidadalmacenamiento',
                    'resistente_al_agua': 'resistenteagua',
                    'caracteristicas_de_la_pantalla': 'caracteristicaspantallas',
                    'nucleos_del_procesador': 'nucleoprocesador',
                    'proveedor_de_servicio_compania': 'proveedorservicio',
                    'ranura_para_sim': 'ranurapasim',
                    'requiere_imei': 'requiereImei',
                    'requiere_serial_number': 'requiere_serial_number',
                    'resolucion_de_pantalla': 'resolucionpantalla',
                    'tamano_de_sim': 'tamanosim',
                    'tipo_de_celular': 'tipocelular',
                    'velocidad_de_imagen': 'velocidadimagen',
                    'condicion_del_producto': 'condicionproducto',
                    'garantia_del_vendedor': 'garantia_del_vendedor',
                };
                return fieldMap[campo] || campo.replace(/_/g, '').toLowerCase();
            }
        }
    
        let fetchUrl = plataforma === 'exito' ? '/get_exito_fields' : '/get_falabella_fields';
    
        fetch(fetchUrl)
        .then(response => response.json())
        .then(data => {
            campos.forEach(campo => {
                const label = document.createElement('label');
                label.htmlFor = campo;
                label.textContent = campo.replace(/_/g, ' ').charAt(0).toUpperCase() + campo.replace(/_/g, ' ').slice(1) +':';
    
                let input;
                const dbFieldName = mapFieldName(campo, plataforma);
    
                if (data.hasOwnProperty(dbFieldName)) {
                    input = document.createElement('select');
                    input.id = campo;
                    input.name = campo;
    
                    const emptyOption = document.createElement('option');
                    emptyOption.value = '';
                    emptyOption.textContent = 'Seleccione una opción';
                    input.appendChild(emptyOption);
    
                    data[dbFieldName].forEach(option => {
                        const optionElement = document.createElement('option');
                        optionElement.value = option;
                        optionElement.textContent = option;
                        input.appendChild(optionElement);
                    });
    
                    formCrearProducto.appendChild(label);
                    formCrearProducto.appendChild(input);
                } else {
                    input = document.createElement('input');
                    input.type = 'text';
                    input.id = campo;
                    input.name = campo;
    
                    formCrearProducto.appendChild(label);
                    formCrearProducto.appendChild(input);
                }
            });
    
            const submitBtn = document.createElement('button');
            submitBtn.type = 'submit';
            submitBtn.textContent = 'Crear Producto';
            formCrearProducto.appendChild(submitBtn);
        })
        .catch(error => {
            console.error(`Error al obtener los campos de ${plataforma}:`, error);
        });
    }
 
    btnCrearProducto.onclick = function() {
        const plataformaSeleccionada = selectPlataformaCrear.value;
        if (plataformaSeleccionada) {
            modalCrearProducto.style.display = "block";
            generarFormulario(plataformaSeleccionada);
        } else {
            alert('Por favor, selecciona una plataforma antes de crear un producto.');
        }
    }
 
    spanClose.onclick = function() {
        modalCrearProducto.style.display = "none";
    }
 
    window.onclick = function(event) {
        if (event.target == modalCrearProducto) {
            modalCrearProducto.style.display = "none";
        }
    }
 
    formCrearProducto.onsubmit = function(e) {
        e.preventDefault();
        const formData = new FormData(formCrearProducto);
        const datos = Object.fromEntries(formData.entries());
 
        // Add the selected platform to the data
        datos.plataforma = selectPlataformaCrear.value;
 
        console.log('Datos a enviar:', datos);
 
        fetch('/crear_producto', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(datos),
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(errorData.error || 'Error desconocido');
                });
            }
            return response.json();
        })
        .then(data => {
            console.log('Respuesta del servidor:', data);
            alert(data.message || 'Producto creado exitosamente');
            modalCrearProducto.style.display = "none";
        })
        .catch((error) => {
            console.error('Error detallado:', error);
            alert('Error al crear el producto: ' + error.message);
        });
    }
 
 
   // Agregar el evento de clic para el botón de descarga micelu
   descargarMiceluBtn.addEventListener('click', function() {
    if (selectedItems.size === 0) {
        alert('Por favor, seleccione al menos un producto para descargar.');
        return;
    }
 
    const selectedSkus = Array.from(selectedItems.keys());
    console.log('SKUs seleccionados para descarga:', selectedSkus);
 
    fetch('/descargar_micelu', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ skus: selectedSkus }),
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        }
        return response.json().then(errData => {
            throw new Error(errData.error || 'Error desconocido en la descarga');
        });
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'productos_micelu.xlsx';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Hubo un error al descargar los productos: ' + error.message);
    });
});
 
});