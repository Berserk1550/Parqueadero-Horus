document.addEventListener("DOMContentLoaded", function () {
  // --- Elementos del DOM ---
  const btnCarro = document.getElementById("btn_carro");
  const btnMoto = document.getElementById("btn_moto");
  const modal = document.getElementById("ventana_proceso");
  const cerrarBtn = document.getElementById("cerrar"); // ajustado al HTML
  const formOperacion = document.getElementById("form_operacion");
  const tipoVehiculoInput = document.getElementById("tipo_vehiculo_input");
  const registrarBtn = document.getElementById("registrar_ingreso");
  const liberarBtn = document.getElementById("liberar_salida");
  const placaInput = formOperacion.querySelector("input[name='vehiculo_placa']"); // ajustado al HTML

  // --- Helpers UI ---
  function abrirModalOperacion(tipo) {
    modal.style.display = "flex";
    tipoVehiculoInput.value = tipo;
  }

  function cerrarModalOperacion() {
    modal.style.display = "none";
  }

  function resetForm() {
    formOperacion.reset();
  }

  function mostrarResumen(data) {
    const resumen = `
      Placa: ${data.vehiculo_placa}
      Tipo: ${data.tipo_vehiculo}
      Ingreso: ${data.fecha_ingreso}
      Salida: ${data.fecha_salida}
      Minutos: ${data.minutos}
      Tarifa aplicada: ${data.tarifa ? data.tarifa.tipo_tarifa : "N/A"}
      Total a cobrar: $${Number(data.total).toFixed(2)}
    `;
    alert(resumen); // usa alert porque tu HTML no tiene modal de resumen
  }

  // --- Eventos ---
  btnCarro.addEventListener("click", () => abrirModalOperacion("carro"));
  btnMoto.addEventListener("click", () => abrirModalOperacion("moto"));
  cerrarBtn.addEventListener("click", cerrarModalOperacion);

  // --- Prevención de doble envío ---
  let bloqueando = false;
  function lock() {
    bloqueando = true;
    registrarBtn.disabled = true;
    liberarBtn.disabled = true;
  }
  function unlock() {
    bloqueando = false;
    registrarBtn.disabled = false;
    liberarBtn.disabled = false;
  }

  // --- Registrar ingreso ---
  registrarBtn.addEventListener("click", async function () {
    if (bloqueando) return;
    lock();

    if (placaInput && placaInput.value) {
      placaInput.value = placaInput.value.trim().toUpperCase();
    } else {
      alert("Debes ingresar una placa");
      unlock();
      return;
    }

    const formData = new FormData(formOperacion);

    try {
      const response = await fetch("/operaciones/ingreso", { method: "POST", body: formData });
      const data = await response.json();

      if (response.ok && data.ok) {
        alert("Ingreso registrado: " + data.vehiculo_placa);
        cerrarModalOperacion();
        resetForm();
      } else {
        alert("Error al registrar ingreso: " + (data.error || "Error desconocido"));
      }
    } catch (error) {
      console.error("Error de conexión al registrar ingreso:", error);
      alert("Error de conexión al registrar ingreso");
    } finally {
      unlock();
    }
  });

  // --- Liberar salida ---
  liberarBtn.addEventListener("click", async function () {
    if (bloqueando) return;
    lock();

    if (placaInput && placaInput.value) {
      placaInput.value = placaInput.value.trim().toUpperCase();
    } else {
      alert("Debes ingresar una placa");
      unlock();
      return;
    }

    const formData = new FormData(formOperacion);

    try {
      const response = await fetch("/operaciones/salida", { method: "POST", body: formData });
      const data = await response.json();

      if (response.ok && data.ok) {
        mostrarResumen(data);
        cerrarModalOperacion();
        resetForm();
      } else {
        alert("Error al registrar salida: " + (data.error || "Error desconocido"));
      }
    } catch (error) {
      console.error("Error de conexión al registrar salida:", error);
      alert("Error de conexión al registrar salida");
    } finally {
      unlock();
    }
  });
});
