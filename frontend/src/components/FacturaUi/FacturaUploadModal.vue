<template>
  <div class="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-md p-6 relative">

      <!-- Botón cerrar -->
      <button 
        @click="$emit('close')" 
        class="absolute right-3 top-3 text-gray-500 hover:text-gray-800"
      >✕</button>

      <h2 class="text-xl font-bold text-gray-800 mb-4">Ingresar Factura COPEC</h2>

      <!-- Input archivo -->
      <input 
        type="file" 
        accept="application/pdf"
        @change="onFileChange"
        class="border p-2 w-full rounded"
      />

      <!-- 🔥 Mensaje de error -->
      <p 
        v-if="errorMsg" 
        class="text-red-600 text-sm mt-2 font-semibold"
      >
        {{ errorMsg }}
      </p>

      <button
        @click="subirFactura"
        :disabled="loading || !archivo"
        class="w-full mt-4 bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg font-semibold disabled:opacity-50"
      >
        {{ loading ? "Subiendo..." : "Subir factura" }}
      </button>

    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import axios from "axios"

const emit = defineEmits(["close", "uploaded"])

const archivo = ref(null)
const loading = ref(false)
const errorMsg = ref("")   // <- NUEVO

function onFileChange(e) {
  archivo.value = e.target.files[0]
  errorMsg.value = "" // limpiar error al elegir archivo
}

async function subirFactura() {
  if (!archivo.value) {
    errorMsg.value = "Debe seleccionar un archivo PDF."
    return
  }

  const form = new FormData()
  form.append("archivo", archivo.value)

  loading.value = true
  errorMsg.value = ""

  try {
    await axios.post("http://localhost:5000/facturas/subir", form, {
      headers: { "Content-Type": "multipart/form-data" }
    })

    emit("uploaded")
    emit("close")

  } catch (err) {
    console.error(err)

    const backendMsg =
      err.response?.data?.error ||
      "Error subiendo factura. Intente nuevamente."

    errorMsg.value = backendMsg  // Mostrar debajo del input
  }

  loading.value = false
}
</script>
