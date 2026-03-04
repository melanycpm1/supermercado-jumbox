document.addEventListener("DOMContentLoaded", function() {

    const checkboxes = document.querySelectorAll(".filtro-categoria");
    const filas = document.querySelectorAll("tbody tr");
    const buscador = document.getElementById("buscarCategoria");
    const itemsCategorias = document.querySelectorAll(".categoria-item");

    function filtrarTabla() {
        let categoriasSeleccionadas = [];

        checkboxes.forEach(cb => {
            if (cb.checked) {
                categoriasSeleccionadas.push(cb.value);
            }
        });

        filas.forEach(fila => {
            let categoriaFila = fila.getAttribute("data-categoria");

            if (categoriasSeleccionadas.length === 0) {
                fila.style.display = "";
            } else {
                fila.style.display = categoriasSeleccionadas.includes(categoriaFila) ? "" : "none";
            }
        });
    }

    checkboxes.forEach(cb => {
        cb.addEventListener("change", filtrarTabla);
    });

    // Buscador dentro del filtro
    buscador.addEventListener("keyup", function() {
        let texto = buscador.value.toLowerCase();

        itemsCategorias.forEach(item => {
            let label = item.textContent.toLowerCase();
            item.style.display = label.includes(texto) ? "" : "none";
        });
    });

});

function ordenarPrecio(tipo) {

    let tbody = document.querySelector("tbody");
    let filas = Array.from(tbody.querySelectorAll("tr"));

    filas.sort(function(a, b) {

        let precioA = parseFloat(a.getAttribute("data-precio"));
        let precioB = parseFloat(b.getAttribute("data-precio"));

        if (tipo === "asc") {
            return precioA - precioB;  // menor a mayor
        } else {
            return precioB - precioA;  // mayor a menor
        }
    });

    // Vaciar tabla
    tbody.innerHTML = "";

    // Volver a agregar filas ordenadas
    filas.forEach(fila => tbody.appendChild(fila));
}