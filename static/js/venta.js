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
            <td>${cantidad}</td>
            <td>${precio}</td>
            <td>${subtotal}</td>
        </tr>
    `;
    const formVenta = document.getElementById('formVenta');

    formVenta.addEventListener('submit', function(e) {
        // Antes de enviar, marcar como pagado automáticamente
        const estadoInput = document.getElementById('estadoInput');
        estadoInput.value = 'Pagado';
    });

    document.getElementById("totalSpan").innerText = total;
    document.getElementById("detalle_json").value = JSON.stringify(listaDetalle);
}