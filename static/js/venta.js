let total = 0;
let listaDetalle = [];

function agregarProducto() {
    const select = document.getElementById("productoSelect");
    const id = select.value;
    const nombre = select.options[select.selectedIndex].text;

    const precio = parseFloat(select.options[select.selectedIndex].dataset.precio);
    const stock = parseInt(select.options[select.selectedIndex].dataset.stock);
    const cantidad = parseInt(document.getElementById("cantidadInput").value);

    if (isNaN(precio)) {
        alert("Error: el producto no tiene precio.");
        return;
    }

    if (isNaN(stock)) {
        alert("Error: stock inválido.");
        return;
    }

    if (isNaN(cantidad) || cantidad <= 0) {
        alert("Ingresá una cantidad válida.");
        return;
    }

    if (cantidad > stock) {
        alert("No podés vender más de lo que hay en stock.");
        return;
    }

    const subtotal = precio * cantidad;
    total += subtotal;

    listaDetalle.push({
        id_producto: id,
        cantidad: cantidad,
        precio_unit: precio,
        subtotal: subtotal
    });

    const tabla = document.getElementById("tablaDetalle");
    tabla.innerHTML += `
    <tr>
        <td>${nombre}</td>
        <td>
            <input type="number" 
                    value="${cantidad}" 
                    min="1" 
                    max="${stock}"
                    onchange="actualizarCantidad(this, ${precio}, ${id})"
                    class="form-control form-control-sm">
        </td>
        <td>${precio}</td>
        <td class="subtotal">${subtotal}</td>
        <td>
            <button type="button" 
                    class="btn btn-danger btn-sm"
                    onclick="eliminarProducto(this, ${id})">
                Eliminar
            </button>
        </td>
    </tr>
`;
    const formVenta = document.getElementById('formVenta');

    /*formVenta.addEventListener('submit', function(e) {
        // Antes de enviar, marcar como pagado automáticamente
        const estadoInput = document.getElementById('estadoInput');
        estadoInput.value = 'Pagado';
    });*/

    document.getElementById("totalSpan").innerText = total;
    document.getElementById("detalle_json").value = JSON.stringify(listaDetalle);
}
    document.getElementById('formVenta').addEventListener('submit', function(e) {
    document.getElementById('estadoInput').value = 'Pagado';
});

function actualizarCantidad(input, precio, idProducto) {

    const nuevaCantidad = parseInt(input.value);

    if (isNaN(nuevaCantidad) || nuevaCantidad <= 0) {
        alert("Cantidad inválida");
        return;
    }

    const fila = input.closest("tr");
    const nuevoSubtotal = precio * nuevaCantidad;

    fila.querySelector(".subtotal").innerText = nuevoSubtotal;

    // Actualizar en listaDetalle
    listaDetalle.forEach(item => {
        if (item.id_producto == idProducto) {
            item.cantidad = nuevaCantidad;
            item.subtotal = nuevoSubtotal;
        }
    });

    recalcularTotal();
}

function eliminarProducto(boton, idProducto) {

    const fila = boton.closest("tr");
    fila.remove();

    // Eliminar del array
    listaDetalle = listaDetalle.filter(item => item.id_producto != idProducto);

    recalcularTotal();
}

function recalcularTotal() {

    total = 0;

    listaDetalle.forEach(item => {
        total += item.subtotal;
    });

    document.getElementById("totalSpan").innerText = total;
    document.getElementById("detalle_json").value = JSON.stringify(listaDetalle);
}

function limpiarFormulario() {
    // Vaciar tabla de detalle
    tablaDetalle.innerHTML = "";

    // Resetear total
    total = 0;
    totalSpan.textContent = total.toFixed(2);

    // Ocultar método de pago
    metodoPagoContainer.style.display = "none";

    // Resetear cantidad a 1
    document.getElementById('cantidadInput').value = 1;

    // Limpiar detalle_json si lo estás usando
    document.getElementById('detalle_json').value = "";
}

// Buscador interno de productos
document.getElementById("buscadorProducto").addEventListener("input", function () {

    let filtro = this.value.toLowerCase();
    let select = document.getElementById("productoSelect");
    let opciones = select.options;

    for (let i = 0; i < opciones.length; i++) {

        let texto = opciones[i].text.toLowerCase();

        if (texto.includes(filtro)) {
            opciones[i].style.display = "";
        } else {
            opciones[i].style.display = "none";
        }
    }
});