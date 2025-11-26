<template>
  <div class="fixed inset-0 flex flex-col bg-gray-100 overflow-hidden">
    <AppHeader @toggle-sidebar="toggleSidebar" />

    <div class="flex flex-1 overflow-hidden">
      <AppSidebar :isOpen="showSidebar" @update:isOpen="val => showSidebar = val" />

      <div class="flex flex-col flex-1">

        <!-- KPI GLOBAL -->
        <div class="p-2 bg-white shadow-md z-50 sticky top-0 border-b border-gray-200">
          <KpiCards :datos="kpiStore.datos" :manuales="kpiStore.manuales" :dispositivos="kpiStore.dispositivos"
            :cargas="kpiStore.cargas" />
        </div>


        <!-- 🔥 Contenido scrollable del router -->
        <main class="flex-1 p-4 overflow-auto bg-[#f3f3f3]">
          <router-view />
        </main>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AppHeader from './components/AppHeader.vue'
import AppSidebar from './components/AppSidebar.vue'
import KpiCards from "@/components/DashboardUi/KpiCards.vue"
import { kpiStore } from '@/stores/kpiStore.js'

const showSidebar = ref(false)
const toggleSidebar = () => showSidebar.value = !showSidebar.value
</script>
