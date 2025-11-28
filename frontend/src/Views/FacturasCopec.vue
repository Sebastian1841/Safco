<template>
    <div class="p-1">

        <!-- TABLA -->
        <FacturaTable v-model="seleccionadas" :facturas="facturas" @nuevaFactura="mostrarModal = true"
            @eliminarSeleccionadas="eliminarSeleccionadas" />


        <!-- MODAL SUBIR FACTURA -->
        <FacturaUploadModal v-if="mostrarModal" @close="mostrarModal = false" @uploaded="cargarFacturas" />
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"


import FacturaTable from "@/components/FacturaUi/FacturaTable.vue"
import FacturaUploadModal from "@/components/FacturaUi/FacturaUploadModal.vue"

const facturas = ref([])
const seleccionadas = ref([])
const mostrarModal = ref(false)

async function cargarFacturas() {
    const res = await axios.get("http://localhost:5000/facturas/listar")
    facturas.value = res.data
    seleccionadas.value = [] // limpiar selección
}


async function eliminarSeleccionadas() {
    if (!confirm("¿Eliminar facturas seleccionadas?")) return

    for (const id of seleccionadas.value) {
        await axios.delete(`http://localhost:5000/facturas/${id}`)
    }

    await cargarFacturas()
}

onMounted(() => cargarFacturas())
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity .25s;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>
