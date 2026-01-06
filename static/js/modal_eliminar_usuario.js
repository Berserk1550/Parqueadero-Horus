let formAEliminar = null;

function abrirModal(boton) {
    formAEliminar = boton.closest("form");
    document.getElementById("modalEliminar").style.display = "flex";
}

function cerrarModal() {
    document.getElementById("modalEliminar").style.display = "none";
    formAEliminar = null;
}

document.addEventListener("DOMContentLoaded", () => {

    const btnCancelar = document.getElementById("btnCancelar");
    const btnConfirmar = document.getElementById("btnConfirmar");

    if (btnCancelar) {
        btnCancelar.addEventListener("click", cerrarModal);
    }

    if (btnConfirmar) {
        btnConfirmar.addEventListener("click", () => {
            if (formAEliminar) {
                formAEliminar.submit();
            }
        });
    }

});
