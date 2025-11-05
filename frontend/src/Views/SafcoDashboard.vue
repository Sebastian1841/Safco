<template>
  <div class="p-3 sm:p-4 bg-gray-50 min-h-screen font-sans">

    <!-- CAPA CIERRE DROPDOWNS -->
    <div v-if="showDropdownDevices || showDropdownDates" @click="closeAllDropdowns" class="fixed inset-0 z-10">
    </div>

    <!-- FILTROS -->
    <div class="flex flex-col lg:flex-row justify-end items-center mb-4 gap-3">
      <div class="flex flex-wrap justify-end items-center gap-3 w-full lg:w-auto">

        <!-- ✅ DROPDOWN DISPOSITIVOS -->
        <div class="relative z-20" v-click-outside="closeDropdownDevices">
          <button @click="toggleDropdown('devices')"
            class="flex items-center gap-1 px-3 py-1.5 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 transition shadow-sm text-xs sm:text-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3 sm:w-4 sm:h-4" fill="none" viewBox="0 0 24 24"
              stroke-width="2" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
            </svg>
            <span>Dispositivos ({{ selectedDevices.length }})</span>
          </button>

          <div v-if="showDropdownDevices"
            class="absolute z-30 mt-1 right-0 bg-white border border-gray-300 rounded-lg shadow-xl w-48 max-h-52 overflow-y-auto">

            <div @click="toggleSelectAllDevices"
              class="flex items-center px-3 py-1.5 bg-gray-100 hover:bg-gray-200 cursor-pointer border-b">
              <input type="checkbox" :checked="allDevicesSelected" class="mr-2 h-3 w-3" />
              <span class="text-xs sm:text-sm font-bold text-gray-800">
                {{ allDevicesSelected ? 'Deseleccionar Todos' : 'Seleccionar Todos' }}
              </span>
            </div>

            <div v-for="device in dispositivos" :key="device.id" @click="toggleDeviceSelection(device.id)"
              class="flex items-center px-3 py-1.5 hover:bg-blue-50 cursor-pointer">
              <input type="checkbox" :checked="selectedDevices.includes(device.id)" class="mr-2 h-3 w-3" />
              <span class="text-xs sm:text-sm">{{ device.nombre }}</span>
            </div>

          </div>
        </div>

        <!-- ✅ DROPDOWN FECHAS -->
        <div class="relative z-10" v-click-outside="closeDropdownDates">
          <button @click="toggleDropdown('dates')"
            class="flex items-center gap-1 px-3 py-1.5 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 transition shadow-sm text-xs sm:text-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3 sm:w-4 sm:h-4" fill="none" viewBox="0 0 24 24"
              stroke="current" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round"
                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span>Rango de Fechas</span>
          </button>

          <div v-if="showDropdownDates"
            class="absolute z-20 mt-1 right-0 bg-white border border-gray-300 rounded-lg shadow-xl p-3 w-64">

            <div class="mb-3 border-b pb-3 border-gray-100">
              <label class="text-xs font-semibold">Selección Rápida:</label>
              <select v-model="selectedRange" @change="applyDateRange(selectedRange)"
                class="w-full border px-2 py-1.5 text-xs rounded-md bg-white">
                <option :value="null" disabled>-- Rango Predefinido --</option>
                <option v-for="option in dateOptions" :key="option.key" :value="option.key">
                  {{ option.label }}
                </option>
              </select>
            </div>

            <div class="flex flex-col gap-2 text-gray-700">
              <label class="text-xs font-semibold">Fecha Inicio:</label>
              <input type="date" v-model="fechaInicio" @input="clearSelectedRange"
                class="border rounded-md px-2 py-1 text-xs" />

              <label class="text-xs font-semibold">Fecha Fin:</label>
              <input type="date" v-model="fechaFin" @input="clearSelectedRange"
                class="border rounded-md px-2 py-1 text-xs" />

              <button @click="clearDateFilters" class="mt-2 text-xs text-red-600 hover:text-red-800 font-medium">
                Limpiar Filtro de Fechas
              </button>
            </div>
          </div>
        </div>

      </div>
    </div>

    <div class="bg-white rounded-lg shadow p-3 space-y-6">

      <CakeChart :datos="filteredDatos" />

      <BarsChart :fecha-inicio="fechaInicio" :fecha-fin="fechaFin" :selected-devices="selectedDevices"
        :selected-range="selectedRange" :dispositivos="dispositivos" />
    </div>

  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'

import CakeChart from '@/components/DashboardUi/CakeChart.vue'
import BarsChart from '@/components/DashboardUi/BarsChart.vue'

import { useDataFilters } from '@/utils/useDataFilters.js'

export default {
  name: 'SafcoDashboard',
  components: { CakeChart, BarsChart },

  // ✅ AGREGAMOS "emit"
  setup(props, { emit }) {

    const BACKEND_URL = "http://localhost:5000"

    const dispositivos = ref([])
    const datosDummy = ref([])
    const manuales = ref([])
    const manualesFiltrados = ref([])

    let filters = useDataFilters(datosDummy, dispositivos, fetchDatos)

    async function fetchManuales() {
      try {
        const r = await axios.get(`${BACKEND_URL}/litros_control`)
        manuales.value = Array.isArray(r.data) ? r.data : []
        filtrarManuales()
      } catch (e) {
        console.error("Error cargando manuales:", e)
      }
    }

    function filtrarManuales() {
      const now = new Date()
      const last24 = new Date(now.getTime() - 24 * 60 * 60 * 1000)

      let result = [...manuales.value]

      if (filters.selectedDevices.value.length) {
        result = result.filter(m =>
          filters.selectedDevices.value.includes(Number(m.dispositivo))
        )
      }

      if (filters.selectedRange.value === 'last_week') {
        result = result.filter(m => new Date(m.fecha) >= now - 7 * 86400000)
      }
      else if (filters.selectedRange.value === 'last_month') {
        result = result.filter(m => new Date(m.fecha) >= now - 30 * 86400000)
      }
      else if (filters.fechaInicio.value && filters.fechaFin.value) {
        const ini = new Date(filters.fechaInicio.value)
        const fin = new Date(filters.fechaFin.value + "T23:59:59")
        result = result.filter(m => new Date(m.fecha) >= ini && new Date(m.fecha) <= fin)
      }
      else {
        result = result.filter(m => new Date(m.fecha) >= last24)
      }

      manualesFiltrados.value = result
    }

    async function fetchDispositivos() {
      try {
        const res = await axios.get(`${BACKEND_URL}/dispositivos`)
        dispositivos.value = Array.isArray(res.data) ? res.data : []
        const ids = dispositivos.value.map(d => d.id)
        filters.selectedDevices.value = [...ids]
      } catch (e) {
        console.error("Error dispositivos:", e)
      }
    }

    async function fetchDatos() {
      try {
        const r = await axios.get(`${BACKEND_URL}/datos`)
        datosDummy.value = Array.isArray(r.data) ? r.data : []
        filters.filtrarDatos()
      } catch (e) {
        console.error("Error datos:", e)
      }
    }

    onMounted(async () => {
      await fetchDispositivos()
      await fetchDatos()
      await fetchManuales()

      // ✅ ahora sí, todos los datos existen → emit
      emit("update-kpis", {
        datos: filters.filteredDatos.value,
        manuales: manualesFiltrados.value,
        dispositivos: dispositivos.value
      })
    })

    watch(
      [filters.selectedDevices, filters.selectedRange, filters.fechaInicio, filters.fechaFin],
      () => {
        filtrarManuales()
        emit("update-kpis", {
          datos: filters.filteredDatos.value,
          manuales: manualesFiltrados.value,
          dispositivos: dispositivos.value
        })
      },
      { deep: true }
    )


    return {
      dispositivos,
      ...filters,
      manualesFiltrados
    }
  }
}
</script>

<style scoped></style>
