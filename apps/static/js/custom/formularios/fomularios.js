function quitar_espacios_input_al_escribir(elemento){
    elemento.keyup(function() {
        $( this ).val($( this ).val().replace(/\s/g, '').replace('.', '').replace(',', '').replace('@', ''));
    });
}