<template>
  <div class="w-full p-4 bg-white rounded-lg shadow space-y-2">
    <p class="text-xs font-semibold text-gray-600">Litros por Dato 1</p>

    <div class="w-full h-60 sm:h-72 md:h-80 lg:h-96 relative">
      <canvas ref="canvas" class="w-full h-full"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick, defineProps } from "vue";
import { Chart, PieController, ArcElement, Tooltip, Legend } from "chart.js";
Chart.register(PieController, ArcElement, Tooltip, Legend);

const props = defineProps({
  datos: { type: Array, default: () => [] }
});

const canvas = ref(null);
let chart = null;

function render() {
  if (chart) { chart.destroy(); chart = null; }
  if (!canvas.value) return;

  const totals = {};
  props.datos.forEach(d => {
    if (!d.dato1_nombre) return;
    totals[d.dato1_nombre] = (totals[d.dato1_nombre] || 0) + (Number(d.litros) || 0);
  });

  const labels = Object.keys(totals);
  const values = Object.values(totals);

  const ctx = canvas.value.getContext("2d");
  chart = new Chart(ctx, {
    type: "pie",
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: [
          "#3B82F6",
          "#60A5FA",
          "#FF7F50",
          "#FBBF24",
          "#34D399",
          "#A78BFA",
          "#F87171",
          "#F472B6"
        ]
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { position: "bottom" },
        tooltip: {
          callbacks: {
            label: ({ label, raw }) => ` ${label}: ${raw.toFixed(2)} L`
          }
        }
      }
    }
  });
}

onMounted(() => nextTick(render));
watch(() => props.datos, () => nextTick(render), { deep: true });
</script>
