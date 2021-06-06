
const crearTabla = (productosComunes, canales, diccionario_datos) => {
    diccionario_datos = diccionario_datos
    canales.forEach(function (canal) {
        let nombre_canal = canal.nombre_canal
        let id_canal = canal.id_canal

        productos_canal = []
        productos_canal = productosComunes.filter(producto => producto.fuente==nombre_canal)
        
        let canal_sin_espacios = limpiar_string(nombre_canal)        
        let div_tabla = creacion_estructura_tabla(nombre_canal, canal_sin_espacios, id_canal)        

        contenedor = document.getElementById("tablas_productos")
        contenedor.appendChild(div_tabla)
        
        productos_canal.forEach(function (productoComun) {

            let canal_tabla_sin_espacios = limpiar_string(nombre_canal)            
            let fila = creacion_fila(nombre_canal, productoComun.nombre, canal_tabla_sin_espacios)

            $(`#tabla_canal_${canal_tabla_sin_espacios} tbody`).append(fila).on('click', 'input', (element) => {
                producto_asociado_seleccionado = $(event.target).attr("value");
                             
                diccionario_datos.set(nombre_canal, `${id_canal}* ${producto_asociado_seleccionado}`)
                console.log(diccionario_datos)
                actualizar_diccionario_datos(nombre_canal)
                /** 
                if(diccionario_datos.size > 0){
                    $(':input[type="radio"]').each(function(index){
                        $(this).prop('required',false);
                    });
                }   
                */    
                           
            });
        })
    });    
    
    $(`table`).DataTable({
        "language": {
            "lengthMenu": "Muestra _MENU_ registros",
            "zeroRecords": "No se encontraron productos similares en el canal de forma automática, realice el proceso manual en caso de que el producto si se encuentre con otro nombre",
            "info": "Mostrando _PAGE_ de _PAGES_",
            "infoEmpty": "No hay registros disponibles",
            "infoFiltered": "(filtrado de _MAX_ registros totales)",
            "loadingRecords": "Cargarndo...",
            "processing":     "Procesando...",
            "search":         "Buscar:",

            "paginate": {
                "first":      "Primero",
                "last":       "Último",
                "next":       "Siguiente",
                "previous":   "Anterior"
            },
        },
        
    });
}

function actualizar_diccionario_datos(nombre_canal){
    if (document.getElementById(`datos_${nombre_canal}`)){
        document.getElementById(`datos_${nombre_canal}`).setAttribute("value", diccionario_datos.get(nombre_canal));
    }else{
        let input_data = document.createElement('input');
        input_data.setAttribute("name", "datos");
        input_data.setAttribute("id", `datos_${nombre_canal}`);
        input_data.setAttribute("value", diccionario_datos.get(nombre_canal));                    
        input_data.hidden = true
        formulario.appendChild(input_data)                     
    }    
}

function creacion_estructura_tabla(canal, nombre_canal, id_canal){
    let tabla = document.createElement('table')
    let encabezado = document.createElement('thead')
    let cuerpo = document.createElement('tbody')
    let fila_encabezado = document.createElement('tr')
    let div_tabla = document.createElement('div')
    let titulo = document.createElement('h3')

    tabla.setAttribute("id", `tabla_canal_${nombre_canal}`)   

    tabla.setAttribute("class", "table table-bordered table-hover datatable")
    tabla.appendChild(encabezado)
    tabla.appendChild(cuerpo)
    titulo.innerHTML = canal
    titulo.setAttribute("class", "text-capitalize nombre_canal")

    let div_busqueda_manual = creacion_busqueda_manual(id_canal, nombre_canal, canal)

    div_tabla.setAttribute("class", "card mx-2 contenedor-tabla px-2 py-3 my-2 border offset")
    div_tabla.appendChild(titulo)    
    div_tabla.appendChild(div_busqueda_manual)
    div_tabla.appendChild(tabla)
    encabezado.appendChild(fila_encabezado)

    lista_encabezados = ['Nombre', 'Selección']
    lista_encabezados.forEach(elemento => {
        let columna_encabezado = document.createElement('th')
        columna_encabezado.innerHTML = elemento
        fila_encabezado.appendChild(columna_encabezado)
    })

    return div_tabla
}

function creacion_busqueda_manual(id_canal, nombre_canal_normalizado, nombre_canal){
    let div_busqueda_manual = document.createElement('div')
    let input_registro_manual_nombre = document.createElement('input')  
    let boton_mostrar = document.createElement('div')    
    
    boton_mostrar.setAttribute("id", `mostrar_canal_${id_canal}`)
    boton_mostrar.setAttribute("class", "btn btn_volver")
    boton_mostrar.innerHTML="Registro manual"  

    $(document).ready( function () {
        let div_tabla = document.getElementById(`tabla_canal_${nombre_canal_normalizado}_wrapper`)
        let input_manual_canal = document.getElementById(`input_manual_${id_canal}`)
        boton_mostrar.onclick = function() {        
            
            if (input_manual_canal.style.display == "none"){
                input_manual_canal.style.display = "block";
                input_manual_canal.setAttribute("required","");                
                boton_mostrar.innerHTML="Volver a seleccion de tabla"
                div_tabla.style.display = "none"             
            }else{            
                input_manual_canal.value = ""           
                input_manual_canal.removeAttribute('required');
                input_manual_canal.style.display = "none";   
                boton_mostrar.innerHTML="Registro manual"
                div_tabla.style.display = "block" 
                        
            }        
        };

        productos_canales.forEach((elemento) => {
            console.log(nombre_canal)
            let hay_seleccionado = false
            radio_buttons = div_tabla.querySelectorAll('input[type="radio"]')
            
            for(let i=0; i<radio_buttons.length; i++){
                if (radio_buttons[i].checked == true){
                    hay_seleccionado = true
                    break;
                }
               
            }
           
           
            if (hay_seleccionado == false){
                if (elemento.canal__nombre == nombre_canal){
                    div_tabla.style.display = "none"
                    input_manual_canal.style.display = "block";
                    input_manual_canal.value = elemento.nombre            
                }
            }
        })
    })

    

    input_registro_manual_nombre.setAttribute("type", "text")
    input_registro_manual_nombre.setAttribute("id", `input_manual_${id_canal}`)
    input_registro_manual_nombre.setAttribute("name", `${id_canal}`)
    input_registro_manual_nombre.setAttribute("class", "form-control col-8 ml-2")
    input_registro_manual_nombre.style.display = "none"
   
    input_registro_manual_nombre.addEventListener('input', function(){                 
        diccionario_datos.set(nombre_canal, `${id_canal}* ${this.value}`)
        actualizar_diccionario_datos(nombre_canal)
        
        //console.log(diccionario_datos)
    });
    
    div_busqueda_manual.appendChild(boton_mostrar)
    div_busqueda_manual.appendChild(input_registro_manual_nombre)    
    div_busqueda_manual.setAttribute("id", `busqueda_manual_${id_canal}`)
    div_busqueda_manual.setAttribute("class", "row px-3 my-3")
    

    return div_busqueda_manual
}


function creacion_radio_button(canal, producto_nombre){

    let radiobutton = document.createElement('input');
    radiobutton.setAttribute("type", "radio");
    radiobutton.setAttribute("name", canal);
    //radiobutton.setAttribute("required", true);
    
    radiobutton.setAttribute("value", producto_nombre);
    
    productos_canales.forEach((elemento) => {
        if (elemento.canal__nombre == canal){
            if(producto_nombre == elemento.nombre){
                radiobutton.setAttribute("checked", true);
            }
        }
    })

    return radiobutton

}

function creacion_fila(canal, producto_nombre, nombre_canal){
    let tabla_canal = document.getElementById(`tabla_canal_${nombre_canal}`)            
    let cuerpo_tabla = tabla_canal.getElementsByTagName("tbody")[0]  

    let fila = document.createElement('tr');
    let campo = document.createElement('td');

    campo.appendChild(document.createTextNode(producto_nombre));                    
    fila.appendChild(campo);                    
    cuerpo_tabla.appendChild(fila)
    campo = document.createElement('td');
    
    let radiobutton = creacion_radio_button(canal, producto_nombre)

    campo.appendChild(radiobutton);
    fila.appendChild(campo);

    return fila
}


function buscarProducto(productos, nombreProducto){       
    $("#tablas_productos").show();
    $("#listado-productos-comunes tbody").empty();
    $("#id_id_producto_comun").val(0);    
    crearTabla(productos, canales, diccionario_datos);   
}

/** 
const buscarProducto = (nombreProductoCompetencia) => {
    $.ajax({
        type: "GET",
        dataType: "json",
        url: url_api_productos_similares,
        data: {
            nombre: nombreProductoCompetencia,
            id_empresa: id_empresa,
            canales: canales,
            csrfmiddlewaretoken: '{{ csrf_token }}'
        },
        success: function (response) {
            borrar_tablas()
            let productos = [];
            productos = response['extracciones']
            
            $("#tablas_productos").show();
            $("#listado-productos-comunes tbody").empty();
            $("#id_id_producto_comun").val(0);

            if (productos.length > 0) {
                let canales = []
                                   
                productos.forEach(producto => { 
                    if(canales.includes(producto.fuente) == false){
                        canales.push(producto.fuente)
                        diccionario_datos.set(producto.fuente, "")
                    }                                                
                });
                                        
                crearTabla(productos, canales, diccionario_datos);                        
            } else {
                toastr["warning"]("No hay productos disponibles de acuerdo al nombre ingresado '" + nombreProductoCompetencia + "'.");
            }
        },
        error: function (e) {
            console.log(e)
            toastr["error"]("Ha surgido un error al identificar los productos disponibles");
        }
    });
}
*/
function borrar_tablas(){
    $(".contenedor-tabla").remove()
}

const removeAccents = (str) => {
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

const remover_caracter = (original, caracter_eliminar) => {
    return original.replace(caracter_eliminar,'')
}

const limpiar_string = (original) => {
    original = original.replace(/\s/g, '_')
    original = remover_caracter(original, /\)/g)
    original = remover_caracter(original, /\(/g)
    original = removeAccents(original.replace(/\./g, ''))

    return original
}

