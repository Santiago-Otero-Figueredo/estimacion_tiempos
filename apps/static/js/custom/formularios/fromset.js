verificar_limite(0)
function clonarFilaIndividuo(selector) {
    let nuevaFila = $(selector).clone(true);
    
    let total = $(`#${id_formulario}-TOTAL_FORMS`).val();
            
    nuevaFila.find(':input').each(function() {
        
        let nuevoId;
        let nuevoNombre;
        let nuevoPlaceHolder;
        let idDelInput = $(this).attr('id');
        let nombreDelInput = $(this).attr('name');
        if (idDelInput) {
            nuevoId = idDelInput.replace(`${id_formulario}-0`, `${id_formulario}-${total}`);
            nuevoNombre = nombreDelInput.replace(`${nombre}-0-`, `${nombre}-${total}-`);
        }
        $(this).attr({'name':nuevoNombre, 'id': nuevoId}).val('').removeAttr('checked');

        if (typeof nombreDelInput != "undefined"){
            if (nombreDelInput.endsWith('-id')){
                $(this).removeAttr('value');
            }
        }
    });
    
    
    $(nuevaFila).attr({'id': `${clase_formulario}_${total}`});
    total++
    $(`#${id_formulario}-TOTAL_FORMS`).val(total);
    $(`.${clase_formulario}:last`).after(nuevaFila);
    $(nuevaFila).find('.indice').html(total)   
    $(nuevaFila).show();
    return (total-1)
}

$('.clonar_fila').on('click', function(e) {
    console.log("###################")
    e.preventDefault();    
    
    if(typeof cantidad_maxima != 'undefined'){        
        let total = $(`#${id_formulario}-TOTAL_FORMS`).val();
        
        if(cantidad_maxima > total){
            clonarFilaIndividuo(`#${clase_formulario}_0`);
            actualizar_elementos(parseInt(total)+1)            
        }
        verificar_limite(total)
    }else{        
        clonarFilaIndividuo(`#${clase_formulario}_0`);
    }        
    
});

function actualizar_elementos(cantidad){
    let elemento_cantidad_actual = document.getElementById("cantidad_actual")
    elemento_cantidad_actual.innerHTML = cantidad            
}


$('.borrar_estructura').on('click', function(e) {
        
    if(typeof cantidad_maxima != 'undefined'){        
        let total = $(`#${id_formulario}-TOTAL_FORMS`).val();                    
        actualizar_elementos(parseInt(total-1))
        verificar_limite(total-1)
    }   
    e.preventDefault();
    eliminarFilaPartidaContable($(this));
    debe = 0;
    haber = 0;
    $(':input[type="number"]').each(function( index ) {                
        dato = $(this);
        cambiar_valores();
    });  
    
});


function eliminarFilaPartidaContable(boton) {
    
    let total = parseInt($(`#${id_formulario}-TOTAL_FORMS`).val());
    
    if (total > 1){ // no se puede eliminar la base
        boton.parent().parent().remove();
        let filas_de_partidas_contables = $(`.${clase_formulario}`);
        $(`#${id_formulario}-TOTAL_FORMS`).val(filas_de_partidas_contables.length);

        for (let i=0; i<filas_de_partidas_contables.length; i++) {
            $(filas_de_partidas_contables.get(i)).find(':input').each(function() {
                if($(this).is("button")){
                    return;
                }
                let idDelInput = $(this).attr('id');
                let nombreDelInput = $(this).attr('name');

                idDelInput = idDelInput.split("-");
                idDelInput[1] = i;
                idDelInput = idDelInput.join("-");

                nombreDelInput = nombreDelInput.split("-");
                nombreDelInput[1] = i;
                nombreDelInput = nombreDelInput.join("-");

                $(this).attr({'name': nombreDelInput, 'id': idDelInput})
            });
            
            $(filas_de_partidas_contables.get(i)).attr({'id': `${clase_formulario}_${i}`});
        }
    }
}


function verificar_limite(total){    
    if(typeof cantidad_maxima != 'undefined'){
        if(cantidad_maxima <= total){          
            mostrar_mensaje_limite()
        }else{            
            ocultar_mensaje_limite()             
        }
    }else{
        ocultar_mensaje_limite()
    }
}

function mostrar_mensaje_limite(){    
    let elemento = document.getElementById('mensaje_limite')
    if (elemento){
        elemento.style.display='block'
    }
}
function ocultar_mensaje_limite(){
    let elemento = document.getElementById('mensaje_limite')
    if (elemento){
        elemento.style.display='none'
    }
    
}