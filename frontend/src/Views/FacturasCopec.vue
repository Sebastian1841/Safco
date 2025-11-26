<template>
    <div class="p-6">

        <!-- BOTÓNES DE ACCIÓN -->
        <div class="flex items-center gap-3 mb-4">

            <!-- Botón agregar factura -->
            <button @click="mostrarModal = true"
                class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-semibold">
                + Ingresar Factura
            </button>

            <!-- Botón eliminar (solo si hay seleccionadas) -->
            <transition name="fade">
                <button v-if="seleccionadas.length > 0" @click="eliminarSeleccionadas"
                    class="flex items-center gap-2 bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-semibold">
                    <SvgIcon name="trash" class="w-4 h-4" />
                    <span>Eliminar ({{ seleccionadas.length }})</span>
                </button>

            </transition>

        </div>

        <!-- TABLA -->
        <FacturaTable v-model="seleccionadas" :facturas="facturas" />

        <!-- MODAL SUBIR FACTURA -->
        <FacturaUploadModal v-if="mostrarModal" @close="mostrarModal = false" @uploaded="cargarFacturas" />
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import axios from "axios"
import SvgIcon from '@/components/icons/SvgIcon.vue';

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
