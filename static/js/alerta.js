document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("form_espacio");

    const inputCarros = document.getElementById("capacidad_carros");
    const inputMotos = document.getElementById("capacidad_motos");

    const modal = document.getElementById("modal-alerta");
    const btnAceptar = document.getElementById("btn-aceptar");

    // Valores originales
    const valorOriginalCarros = inputCarros.value;
    const valorOriginalMotos = inputMotos.value;

    form.addEventListener("submit", (e) => {

        const valorActualCarros = inputCarros.value;
        const valorActualMotos = inputMotos.value;

        if (
            valorOriginalCarros === valorActualCarros &&
            valorOriginalMotos === valorActualMotos
        ) {
            e.preventDefault(); // ⛔ NO envía el form
            modal.style.display = "flex"; // Muestra modal
        }
    });

    btnAceptar.addEventListener("click", () => {
        modal.style.display = "none";
    });

});
