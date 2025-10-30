<template>
  <div class=" bg-gray-50 min-h-screen">
    <!-- Componente hijo -->
    <Tables />
  </div>
</template>

<script>
import Tables from '@/components/Tables/DataTables.vue'

export default {
  name: 'SafcoTables',
  components: {
    Tables
  }
}
</script>

<style scoped>
/* Puedes agregar estilos específicos del contenedor aquí */
</style>
