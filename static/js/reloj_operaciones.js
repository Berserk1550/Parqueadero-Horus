function actualizarFechaHora() {
    const ahora= new Date();
    //fecha
    const opcionesFecha ={weekday: 'long', year: 'numeric', month:'long', day:'numeric'};
    const fechaFormateada= ahora.toLocaleDateString('es-ES', opcionesFecha) ;
    //hora
    let horas = ahora.getHours();
    const minutos = String(ahora.getMinutes()).padStart(2,'0');
    const ampm = horas>=12 ? 'PM' : 'AM';
    horas = horas %12;
    horas = horas ? horas:12;
    const horaFormateada = `${horas}:${minutos}:${ampm}`;
    //Dom
    document.getElementById("fecha_actual").textContent = `Hoy es ${fechaFormateada}`;
    document.getElementById("hora_actual").textContent = `y son las ${horaFormateada}`;
}
setInterval(actualizarFechaHora, 1000);
actualizarFechaHora();
