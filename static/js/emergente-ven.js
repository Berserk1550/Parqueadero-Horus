document.addEventListener("DOMContentLoaded", function () {
  // --- Elementos del DOM ---
  const btnCarro = document.getElementById("btn_carro");
  const btnMoto = document.getElementById("btn_moto");
  const modal = document.getElementById("ventana_proceso");
  const cerrarBtn = document.getElementById("cerrar");
  const formOperacion = document.getElementById("form_operacion");
  const tipoVehiculoInput = document.getElementById("tipo_vehiculo_input");
  const registrarBtn = document.getElementById("registrar_ingreso");
  const liberarBtn = document.getElementById("liberar_salida");
  const placaInput = formOperacion.querySelector("input[name='vehiculo_placa']");

  // --- Funciones auxiliares ---
  function abrirModalOperacion(tipo) {
    modal.style.display = "flex";
    tipoVehiculoInput.value = tipo.toUpperCase(); // siempre enviar CARRO/MOTO
    placaInput.value = ""; // limpiar input al abrir
    placaInput.disabled = false;
    placaInput.ariaReadOnly = false;
    placaInput.focus();
    console.log("DEBUG tipo enviado:", tipoVehiculoInput.value);
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
    alert(resumen);
  }

  // --- Validación de placa ---
  function validarPlaca(tipo, placa) {
    placa = placa.trim().toUpperCase();

    if (placa.length !== 6) {
      alert("La placa debe tener exactamente 6 caracteres.");
      return false;
    }

    if (tipo === "CARRO") {
      if (!/^[A-Z]{3}[0-9]{3}$/.test(placa)) {
        alert("Formato Carro: 3 letras + 3 números (ej: ABC123).");
        return false;
      }
    } else if (tipo === "MOTO") {
      if (!/^[A-Z]{3}[0-9]{2}[A-Z]{1}$/.test(placa)) {
        alert("Formato Moto: 3 letras + 2 números + 1 letra (ej: ABC12D).");
        return false;
      }
    }

    placaInput.value = placa; // normalizar a mayúsculas
    return true;
  }

  // --- Eventos ---
  btnCarro.addEventListener("click", () => abrirModalOperacion("carro"));
  btnMoto.addEventListener("click", () => abrirModalOperacion("moto"));
  cerrarBtn.addEventListener("click", cerrarModalOperacion);

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

  registrarBtn.addEventListener("click", async function () {
    if (bloqueando) return;
    lock();

    const tipo = tipoVehiculoInput.value;
    const placa = placaInput.value;

    if (!validarPlaca(tipo, placa)) {
      unlock();
      return;
    }

    const formData = new FormData(formOperacion);
    try {
      const response = await fetch("/operaciones/ingreso", { method: "POST", body: formData });
      const data = await response.json();
      console.log("DEBUG ingreso:", data);
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

  liberarBtn.addEventListener("click", async function () {
    if (bloqueando) return;
    lock();

    const tipo = tipoVehiculoInput.value;
    const placa = placaInput.value;

    if (!validarPlaca(tipo, placa)) {
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
