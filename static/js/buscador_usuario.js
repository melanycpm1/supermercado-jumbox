function buscadorUsuario(){
const inputBuscarCard = document.getElementById('buscarUsuario');
inputBuscarCard.addEventListener('keyup', function() {
    const filter = inputBuscarCard.value.toLowerCase();
    const cards = document.querySelectorAll('.row .card');

    cards.forEach(card => {
        const nombre = card.querySelector('.card-title').innerText.toLowerCase();
        const email = card.querySelector('.card-text').innerText.toLowerCase();
        const rolBadge = card.querySelector('.badge').innerText.toLowerCase();

        if (nombre.includes(filter) || email.includes(filter) || rolBadge.includes(filter)) {
            card.parentElement.style.display = '';
        } else {
            card.parentElement.style.display = 'none';
        }
    });
});
};
document.addEventListener('DOMContentLoaded', buscadorUsuario);

let ordenAscendente = true;

function ordenarUsuarios(tipo) {

    const contenedor = document.querySelector(".row.g-3");
    const usuarios = Array.from(document.querySelectorAll(".usuario-card"));

    usuarios.sort((a, b) => {

        let valorA = a.dataset[tipo];
        let valorB = b.dataset[tipo];

        if (valorA < valorB) return ordenAscendente ? -1 : 1;
        if (valorA > valorB) return ordenAscendente ? 1 : -1;
        return 0;
    });

    ordenAscendente = !ordenAscendente;

    contenedor.innerHTML = "";
    usuarios.forEach(u => contenedor.appendChild(u));
}