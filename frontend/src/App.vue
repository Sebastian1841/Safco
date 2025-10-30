<template>
  <div class="fixed inset-0 flex flex-col bg-gray-100 overflow-hidden">
    <AppHeader @toggle-sidebar="toggleSidebar" />

    <div class="flex flex-1 overflow-hidden">
      <AppSidebar :isOpen="showSidebar" @update:isOpen="val => showSidebar = val" />

      <!-- Solo el área de contenido puede desplazarse -->
      <main class="flex-1 p-4 overflow-auto bg-[#f3f3f3]">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AppHeader from './components/AppHeader.vue'
import AppSidebar from './components/AppSidebar.vue'

const showSidebar = ref(false)
const toggleSidebar = () => {
  showSidebar.value = !showSidebar.value
}
</script>
