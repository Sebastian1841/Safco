<template>
  <div class="p-3 sm:p-4 bg-gray-50 min-h-screen font-sans">

    <div v-if="showDropdownDevices || showDropdownDates" @click="closeAllDropdowns" class="fixed inset-0 z-10"></div>

    <div class="flex flex-col lg:flex-row justify-between items-center mb-4 gap-3">

      <button @click="emitirModalNivel"
        class="px-3 py-1.5 bg-green-600 text-white font-medium rounded-md hover:bg-green-700 transition shadow-sm text-xs sm:text-sm">
        Ver Nivel de Estanque
      </button>

      <div class="flex flex-wrap justify-end items-center gap-3 w-full lg:w-auto">

        <!-- dropdown dispositivos (no tocado) -->
        <div class="relative z-20" v-click-outside="closeDropdownDevices">
          <button @click="toggleDropdown('devices')"
            class="flex items-center gap-1 px-3 py-1.5 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 transition shadow-sm text-xs sm:text-sm">
            <SvgIcon name="chevron-down" class="w-4 h-4" />
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

        <!-- dropdown fechas (no tocado) -->
        <div class="relative z-20" v-click-outside="closeDropdownDates">
          <button @click="toggleDropdown('dates')"
            class="flex items-center gap-1 px-3 py-1.5 bg-blue-600 text-white font-medium rounded-md hover:bg-blue-700 transition duration-150 shadow-sm text-xs sm:text-sm">
            <SvgIcon name="calendar-range" class="w-3 h-3 sm:w-4 sm:h-4" />
            <span>Rango de Fechas</span>
          </button>

          <div v-if="showDropdownDates"
            class="absolute z-20 mt-1 right-0 bg-white border border-gray-300 rounded-lg shadow-xl p-3 w-64">

            <div class="mb-3 border-b pb-3 border-gray-100">
              <label class="text-xs font-semibold">Selección Rápida:</label>
              <select v-model="selectedRange" @change="applyDateRange(selectedRange)"
                class="w-full border px-2 py-1.5 text-xs rounded-md bg-white">
                <option :value="null" disabled>-- Rango Predefinido --</option>
                <option v-for="option in dateOptions" :key="option.key" :value="option.key">{{ option.label }}</option>
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

      <!-- ⭐ CAMBIO NECESARIO -->
      <CakeChart :fecha-inicio="fechaInicio" :fecha-fin="fechaFin" :selected-devices="selectedDevices"
        :selected-range="selectedRange" />

      <BarsChart :fecha-inicio="fechaInicio" :fecha-fin="fechaFin" :selected-devices="selectedDevices"
        :selected-range="selectedRange" :dispositivos="dispositivos" />
    </div>

    <ModalNivelEstanque v-if="showModalNivel" :nivelFijo="nivelFijo" :nivelMovil="nivelMovil" :maxFijo="maxFijoTotal"
      :maxMovil="maxMovilTotal" :historial="historial" :dispositivos="dispositivos" @cerrar="showModalNivel = false" />
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from "vue";
import axios from "axios";

import ModalNivelEstanque from "@/components/DashboardUi/ModalNivelEstanque.vue";
import CakeChart from "@/components/DashboardUi/CakeChart.vue";
import BarsChart from "@/components/DashboardUi/BarsChart.vue";
import SvgIcon from "@/components/icons/SvgIcon.vue";

import { useDataFilters } from "@/utils/useDataFilters.js";
import { kpiStore } from "@/stores/kpiStore.js";

export default {
  name: "SafcoDashboard",
  components: { CakeChart, BarsChart, ModalNivelEstanque, SvgIcon },

  setup() {
    const BACKEND_URL = "http://localhost:5000";

    const cargasCombustible = ref([]);
    const dispositivos = ref([]);
    const datosDummy = ref([]);
    const manuales = ref([]);
    const manualesFiltrados = ref([]);
    const showModalNivel = ref(false);

    let filters = useDataFilters(datosDummy, dispositivos, fetchDatos);

    // ⭐ NUEVO — datos EXCLUSIVOS para los charts Pie
    const datosCharts = ref([]);

    function emitirModalNivel() {
      showModalNivel.value = true;
    }

    /* ===========================
       CARGAS (NO TOCADO)
    ============================ */
    async function fetchNiveles() {
      const res = await axios.get(`${BACKEND_URL}/cargas_combustible`);
      cargasCombustible.value = Array.isArray(res.data) ? res.data : [];
    }

    /* ===========================
       MANUALES (NO TOCADO)
    ============================ */
    async function fetchManuales() {
      const r = await axios.get(`${BACKEND_URL}/litros_control`);
      manuales.value = Array.isArray(r.data) ? r.data : [];
      filtrarManuales();
    }

    function filtrarManuales() {
      const now = new Date();
      const last24 = new Date(now.getTime() - 24 * 3600 * 1000);

      let result = [...manuales.value];

      if (filters.selectedDevices.value.length)
        result = result.filter(m =>
          filters.selectedDevices.value.includes(Number(m.dispositivo))
        );

      if (filters.selectedRange.value === "last_week")
        result = result.filter(m => new Date(m.fecha) >= now - 7 * 86400000);

      else if (filters.selectedRange.value === "last_month")
        result = result.filter(m => new Date(m.fecha) >= now - 30 * 86400000);

      else if (filters.fechaInicio.value && filters.fechaFin.value) {
        const ini = new Date(filters.fechaInicio.value);
        const fin = new Date(filters.fechaFin.value + "T23:59:59");
        result = result.filter(m => new Date(m.fecha) >= ini && new Date(m.fecha) <= fin);
      }

      else result = result.filter(m => new Date(m.fecha) >= last24);

      manualesFiltrados.value = result;
    }

    /* ===========================
       NIVELES + HISTORIAL (NO TOCADO)
    ============================ */
    const nivelesCalculados = computed(() => {
      const eventos = [];

      const nombreEstanque = id =>
        id === 1 ? "Estanque Fijo" : id === 2 ? "Estanque Móvil" : "Estanque";

      if (!cargasCombustible.value.length) {
        return {
          fijo: 0,
          movil: 0,
          maxFijo: 0,
          maxMovil: 0,
          eventos: []
        };
      }

      const primeraCarga = cargasCombustible.value
        .map(c => new Date(`${c.fecha}T${c.hora}`))
        .sort((a, b) => a - b)[0];

      let raw = [];

      cargasCombustible.value.forEach(c => {
        raw.push({
          tipo: "carga",
          dispositivo: Number(c.dispositivo_id),
          fechaISO: `${c.fecha}T${c.hora}`,
          cantidad: Number(c.litros_total)
        });
      });

      datosDummy.value.forEach(d => {
        const fechaTB = new Date(d.fecha);

        if (fechaTB >= primeraCarga) {
          raw.push({
            tipo: "descarga",
            dispositivo: Number(d.dispositivo_id),
            fechaISO: d.fecha,
            cantidad: Number(d.litros)
          });
        }
      });

      raw.sort((a, b) => new Date(a.fechaISO) - new Date(b.fechaISO));

      let nivelFijo = 0;
      let nivelMovil = 0;
      let maxFijo = 0;
      let maxMovil = 0;

      raw.forEach(ev => {
        const fechaObj = new Date(ev.fechaISO);

        let totalPosterior = 0;

        if (ev.dispositivo === 1) {
          if (ev.tipo === "carga") nivelFijo += ev.cantidad;
          if (ev.tipo === "descarga") nivelFijo -= ev.cantidad;
          totalPosterior = nivelFijo;
          maxFijo = Math.max(maxFijo, totalPosterior);
        }

        if (ev.dispositivo === 2) {
          if (ev.tipo === "carga") nivelMovil += ev.cantidad;
          if (ev.tipo === "descarga") nivelMovil -= ev.cantidad;
          totalPosterior = nivelMovil;
          maxMovil = Math.max(maxMovil, totalPosterior);
        }

        eventos.push({
          tipo: ev.tipo,
          descripcion: ev.tipo === "carga" ? "Carga registrada" : "Descarga de combustible",
          cantidad: ev.cantidad,
          estanque: nombreEstanque(ev.dispositivo),
          total_posterior: totalPosterior,
          fecha_texto: fechaObj.toLocaleDateString("es-CL"),
          hora_texto: fechaObj.toLocaleTimeString("es-CL", { hour12: false }),
          _orden: fechaObj.getTime()
        });
      });

      return {
        fijo: nivelFijo,
        movil: nivelMovil,
        maxFijo,
        maxMovil,
        eventos: eventos.sort((a, b) => b._orden - a._orden)
      };
    });

    /* ===========================
       DISPOSITIVOS Y DATOS (NO TOCADO)
    ============================ */
    async function fetchDispositivos() {
      const res = await axios.get(`${BACKEND_URL}/dispositivos`);
      dispositivos.value = Array.isArray(res.data) ? res.data : [];
      filters.selectedDevices.value = dispositivos.value.map(d => d.id);
    }

    async function fetchDatos() {
      const r = await axios.get(`${BACKEND_URL}/datos`);
      datosDummy.value = Array.isArray(r.data) ? r.data : [];
      filters.filtrarDatos();

      // ⭐ PRIMER CARGA DE DATOS PARA CHARTS
      datosCharts.value = [...filters.filteredDatos.value];
    }

    /* ===========================
       MOUNT (NO TOCADO)
    ============================ */
    onMounted(async () => {
      await fetchDispositivos();
      await fetchDatos();
      await fetchManuales();
      await fetchNiveles();

      kpiStore.updateKPIs({
        datos: filters.filteredDatos.value,
        manuales: manualesFiltrados.value,
        dispositivos: dispositivos.value,
        cargas: cargasCombustible.value
      });
    });

    /* ===========================
       WATCHERS (⭐ AQUÍ SE ARREGLA TODO)
    ============================ */
    watch(
      [filters.selectedDevices, filters.selectedRange, filters.fechaInicio, filters.fechaFin],
      () => {
        // ⭐ ACTUALIZA PIE CHARTS SIEMPRE
        datosCharts.value = [...filters.filteredDatos.value];

        filtrarManuales();

        kpiStore.updateKPIs({
          datos: filters.filteredDatos.value,
          manuales: manualesFiltrados.value,
          dispositivos: dispositivos.value,
          cargas: cargasCombustible.value
        });
      },
      { deep: true }
    );

    return {
      showModalNivel,
      emitirModalNivel,
      dispositivos,

      datosCharts,

      nivelFijo: computed(() => nivelesCalculados.value.fijo),
      nivelMovil: computed(() => nivelesCalculados.value.movil),
      maxFijoTotal: computed(() => nivelesCalculados.value.maxFijo),
      maxMovilTotal: computed(() => nivelesCalculados.value.maxMovil),
      historial: computed(() => nivelesCalculados.value.eventos),

      ...filters,
      manualesFiltrados
    };
  }
};
</script>

<style scoped></style>
