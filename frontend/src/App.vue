<template>
  <div class="fixed inset-0 flex flex-col bg-gray-100 overflow-hidden">



    <AppHeader @toggle-sidebar="toggleSidebar" />

    <div class="flex flex-1 overflow-hidden">
      <AppSidebar :isOpen="showSidebar" @update:isOpen="val => showSidebar = val" />

      <main class="flex-1 p-4 overflow-auto bg-[#f3f3f3]">
        <!-- ✅ KPI SIEMPRE ARRIBA, EN TODA LA APP -->
        <div class="p-2 bg-white shadow-md z-50">
          <KpiCards :datos="kpiDatos" :manuales="kpiManuales" :dispositivos="kpiDispositivos" />
        </div>
        <!-- ✅ Los filtros quedan en el dashboard, y lo que produce se envía acá -->
        <router-view @update-kpis="updateKPIs" />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AppHeader from './components/AppHeader.vue'
import AppSidebar from './components/AppSidebar.vue'
import KpiCards from "@/components/DashboardUi/KpiCards.vue"

const showSidebar = ref(false)
const toggleSidebar = () => showSidebar.value = !showSidebar.value

// ✅ KPI DATA capturada desde el dashboard
const kpiDatos = ref([])
const kpiManuales = ref([])
const kpiDispositivos = ref([])

function updateKPIs({ datos, manuales, dispositivos }) {
  kpiDatos.value = datos || []
  kpiManuales.value = manuales || []
  kpiDispositivos.value = dispositivos || []
}
</script>
