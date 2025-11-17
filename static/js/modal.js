function abrirModal(idProducto, cantidadActual) {
    document.getElementById("modal_id_producto").value = idProducto;
    document.getElementById("modal_cantidad").value = cantidadActual;
    document.getElementById("cantidad_previa").value = cantidadActual;

    document.getElementById("modalCantidad").style.display = "flex";
}

function cerrarModal() {
    document.getElementById("modalCantidad").style.display = "none";
}

document.addEventListener("DOMContentLoaded", function () {

    const botonesEditar = document.querySelectorAll(".editar-btn");

    botonesEditar.forEach(boton => {
        boton.addEventListener("click", function () {

            // Tomar los datos del data
            document.getElementById("edit_id").value = this.dataset.id;
            document.getElementById("edit_nombre").value = this.dataset.nombre;
            document.getElementById("edit_categoria").value = this.dataset.categoria;
            document.getElementById("edit_precio").value = this.dataset.precio;
            document.getElementById("edit_stock").value = this.dataset.stock;

            // Mostrar modal
            document.getElementById("modalEditar").style.display = "flex";
        });
    });
});

function cerrarEditar() {
    document.getElementById("modalEditar").style.display = "none";
}