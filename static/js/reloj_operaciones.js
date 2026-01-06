function actualizarReloj() {
  const ahora = new Date();
  let horas = ahora.getHours().toString().padStart(2, '0');
  let minutos = ahora.getMinutes().toString().padStart(2, '0');
  let segundos = ahora.getSeconds().toString().padStart(2, '0');
  
  const spanHora = document.getElementById("hora_actual");
  if (spanHora) {
    spanHora.textContent = `${horas}:${minutos}:${segundos}`;
  }
}

// Espera a que el DOM esté listo----
document.addEventListener("DOMContentLoaded", () => {
  actualizarReloj();
  setInterval(actualizarReloj, 1000);
});
