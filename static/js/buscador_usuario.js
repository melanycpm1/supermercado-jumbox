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
