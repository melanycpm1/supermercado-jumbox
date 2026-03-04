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