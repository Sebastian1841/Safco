<template>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
    <LitrosPorIbutton :datos="datos" />
    <PorcentajeDato1 :datos="datos" />
    <PorcentajeDato2 :datos="datos" />
  </div>
</template>

<script setup>
import { defineProps } from "vue";
import LitrosPorIbutton from "./pies/LitrosPorIbutton.vue";
import PorcentajeDato1 from "./pies/PorcentajeDato1.vue";
import PorcentajeDato2 from "./pies/PorcentajeDato2.vue";

defineProps({
  datos: {
    type: Array,
    default: () => []
  }
});
</script>
