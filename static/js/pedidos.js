document.querySelector("form").addEventListener("submit", function (e) {
    let detalles = [];
    document.querySelectorAll(".cantidad-input").forEach(input => {
        if (input.value > 0) {
            detalles.push({
                id_producto: input.dataset.id,
                cantidad_solicitada: input.value
            });
        }
    });
    document.getElementById("detalle_json").value = JSON.stringify(detalles);
});