<template>
  <div class="p-4 sm:p-6 bg-gray-50 min-h-screen font-sans">

    <!-- -------------------- Formularios Dato 1 y Dato 2 -------------------- -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
      <!-- Dato 1 -->
      <div class="bg-white p-4 sm:p-6 rounded-lg shadow-xl border border-gray-200">
        <h2 class="text-xl font-semibold text-blue-700 mb-4 flex items-center gap-2">
          Añadir Referencia: Dato 1
        </h2>
        <form @submit.prevent="addDato1" class="flex flex-col sm:flex-row gap-4 mb-4">
          <input type="text" v-model="newDato1Item" required
            class="flex-1 border border-gray-300 rounded-md p-2 text-sm focus:ring-blue-500 focus:border-blue-500"
            placeholder="Ej: Cliente D, Turno Mañana..." />
          <button type="submit"
            class="sm:w-auto px-4 py-2 bg-green-600 text-white font-medium rounded-md hover:bg-green-700 transition duration-150 shadow-md text-sm">
            Agregar
          </button>
        </form>
        <h3 class="text-sm font-bold text-gray-700 mt-6 mb-2 border-t pt-4">
          Datos Agregados: ({{ dato1Data.length }})
        </h3>
        <div class="max-h-40 overflow-y-auto border border-gray-100 rounded-md p-2 bg-gray-50">
          <ul v-if="dato1Data.length" class="space-y-1">
            <li v-for="item in dato1Data" :key="item.id"
              class="flex justify-between items-center bg-white p-2 rounded-md shadow-sm text-sm border border-gray-100">
              <span class="text-gray-800 font-medium">{{ item.nombre }}</span>
              <span class="text-xs text-gray-500 font-mono">ID: {{ item.id }}</span>
            </li>
          </ul>
          <p v-else class="text-sm text-gray-500 italic p-2 text-center">
            Aún no se han agregado referencias.
          </p>
        </div>
      </div>

      <!-- Dato 2 -->
      <div class="bg-white p-4 sm:p-6 rounded-lg shadow-xl border border-gray-200">
        <h2 class="text-xl font-semibold text-blue-700 mb-4 flex items-center gap-2">
          Añadir Referencia: Dato 2
        </h2>
        <form @submit.prevent="addDato2" class="flex flex-col sm:flex-row gap-4 mb-4">
          <input type="text" v-model="newDato2Item" required
            class="flex-1 border border-gray-300 rounded-md p-2 text-sm focus:ring-blue-500 focus:border-blue-500"
            placeholder="Ej: Proyecto Alfa, Turno Noche..." />
          <button type="submit"
            class="sm:w-auto px-4 py-2 bg-green-600 text-white font-medium rounded-md hover:bg-green-700 transition duration-150 shadow-md text-sm">
            Agregar
          </button>
        </form>
        <h3 class="text-sm font-bold text-gray-700 mt-6 mb-2 border-t pt-4">
          Datos Agregados: ({{ dato2Data.length }})
        </h3>
        <div class="max-h-40 overflow-y-auto border border-gray-100 rounded-md p-2 bg-gray-50">
          <ul v-if="dato2Data.length" class="space-y-1">
            <li v-for="item in dato2Data" :key="item.id"
              class="flex justify-between items-center bg-white p-2 rounded-md shadow-sm text-sm border border-gray-100">
              <span class="text-gray-800 font-medium">{{ item.nombre }}</span>
              <span class="text-xs text-gray-500 font-mono">ID: {{ item.id }}</span>
            </li>
          </ul>
          <p v-else class="text-sm text-gray-500 italic p-2 text-center">
            Aún no se han agregado referencias.
          </p>
        </div>
      </div>
    </div>

    <!-- -------------------- Formulario Consumo por Litros -------------------- -->
    <div class="bg-white p-4 sm:p-6 rounded-lg shadow-xl border border-gray-200">
      <h2 class="text-xl font-semibold text-blue-700 mb-4 flex items-center gap-2">
        Registro Manual de Consumo por Litros
      </h2>

      <form @submit.prevent="addLitrosControl" class="flex flex-col gap-4 mb-4">

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label for="control-date" class="block text-xs font-medium text-gray-700 mb-1">Fecha de Control</label>
            <input type="date" id="control-date" v-model="newLitrosControl.fecha" required
              class="w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-blue-500 focus:border-blue-500" />
          </div>

          <div>
            <label for="control-device" class="block text-xs font-medium text-gray-700 mb-1">Dispositivo/Vehículo</label>
            <select id="control-device" v-model="newLitrosControl.dispositivo" required
              class="w-full border border-gray-300 rounded-md p-2 text-sm bg-white focus:ring-blue-500 focus:border-blue-500">
              <option value="" disabled>
                <span v-if="loadingDevices">Cargando Dispositivos...</span>
                <span v-else-if="dispositivos.length === 0">No se encontraron dispositivos</span>
                <span v-else>Seleccione un Dispositivo</span>
              </option>
              <option v-for="device in dispositivos" :key="device.id" :value="device.id" :disabled="loadingDevices">
                {{ getOptionLabel(device) }}
              </option>
            </select>
          </div>
        </div>

        <div class="flex gap-4">
          <div class="flex-1">
            <label for="litros-inicio" class="block text-xs font-medium text-gray-700 mb-1">Litros Iniciales (Odómetro al Inicio)</label>
            <input type="number" id="litros-inicio" v-model.number="newLitrosControl.litros_inicio" required step="0.01"
              min="0" class="w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-blue-500 focus:border-blue-500" placeholder="0.00" />
          </div>
          <div class="flex-1">
            <label for="litros-final" class="block text-xs font-medium text-gray-700 mb-1">Litros Finales (Odómetro al Final)</label>
            <input type="number" id="litros-final" v-model.number="newLitrosControl.litros_final" required step="0.01"
              :min="0" class="w-full border border-gray-300 rounded-md p-2 text-sm focus:ring-blue-500 focus:border-blue-500" placeholder="0.00" />
          </div>
        </div>

        <div class="text-sm font-semibold p-2 rounded-md bg-red-100 text-red-800">
          ATENCIÓN: Para registrar el consumo, el valor final debe ser menor o igual al valor inicial.
        </div>

        <button type="submit" :disabled="loadingDevices || dispositivos.length === 0"
          class="sm:w-full px-4 py-2 bg-indigo-600 text-white font-medium rounded-md hover:bg-indigo-700 transition duration-150 shadow-md text-sm disabled:bg-gray-400">
          Registrar Consumo Manual
        </button>
      </form>

      <h3 class="text-sm font-bold text-gray-700 mt-6 mb-2 border-t pt-4">
        Controles de Consumo Registrados ({{ litrosControlData.length }})
      </h3>
      <div class="max-h-60 overflow-y-auto border border-gray-100 rounded-md p-2 bg-gray-50">
        <ul v-if="litrosControlData.length" class="space-y-1">
          <li v-for="item in litrosControlData" :key="item.id"
            class="flex flex-wrap justify-between items-center bg-white p-2 rounded-md shadow-sm text-sm border border-gray-100">

            <div class="flex flex-col sm:flex-row sm:items-center justify-between w-full">
              <span class="text-gray-800 font-bold">
                <span class="text-red-600">CONSUMO</span>: {{ getOptionLabelById(item.dispositivo) }}
              </span>
              <span class="text-xs text-gray-500 font-semibold mt-1 sm:mt-0">{{ item.fecha }}</span>
            </div>

            <div class="flex justify-between items-center w-full mt-1">
              <span class="text-xs text-gray-500">
                Inicio: **{{ item.litros_inicio }} L** | Fin: **{{ item.litros_final }} L**
              </span>
              <span class="bg-red-100 text-red-700 px-2 py-0.5 rounded-full font-bold text-xs whitespace-nowrap">
                Consumo: {{ Math.abs(item.diferencia_manual).toFixed(2) }} L
              </span>
            </div>
          </li>
        </ul>
        <p v-else class="text-sm text-gray-500 italic p-2 text-center">
          Aún no se han registrado controles manuales de litros.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
  name: "SafcoInputData",
  setup() {
    // -------------------- Dispositivos API --------------------
    const dispositivos = ref([]);
    const loadingDevices = ref(true);

    const fetchDispositivosConDatos = async () => {
      loadingDevices.value = true;
      try {
        const res = await axios.get("http://localhost:5000/dispositivos");
        dispositivos.value = res.data;
        console.log("✅ Dispositivos con datos:", dispositivos.value);
      } catch (err) {
        console.error("❌ Error al cargar dispositivos:", err);
        dispositivos.value = [];
      } finally {
        loadingDevices.value = false;
      }
    };
    onMounted(fetchDispositivosConDatos);

    const getOptionLabel = (device) => device.nombre;
    const getOptionLabelById = (id) => {
      const device = dispositivos.value.find(d => d.id === id);
      return device ? device.nombre : `Dispositivo ${id}`;
    };

    // -------------------- Dato 1 --------------------
    const newDato1Item = ref('');
    const dato1Data = ref([]);
    const dato1IdCounter = ref(1);
    const addDato1 = () => {
      if (newDato1Item.value.trim() !== '') {
        dato1Data.value.push({ id: dato1IdCounter.value++, nombre: newDato1Item.value.trim() });
        newDato1Item.value = '';
      }
    };

    // -------------------- Dato 2 --------------------
    const newDato2Item = ref('');
    const dato2Data = ref([]);
    const dato2IdCounter = ref(1);
    const addDato2 = () => {
      if (newDato2Item.value.trim() !== '') {
        dato2Data.value.push({ id: dato2IdCounter.value++, nombre: newDato2Item.value.trim() });
        newDato2Item.value = '';
      }
    };

    // -------------------- Consumo por Litros --------------------
    const today = new Date().toISOString().split('T')[0];
    const newLitrosControl = ref({ fecha: today, dispositivo: '', litros_inicio: null, litros_final: null });
    const litrosControlData = ref([]);
    const litrosControlIdCounter = ref(1);

    const addLitrosControl = () => {
      const { litros_inicio, litros_final } = newLitrosControl.value;
      if (litros_final > litros_inicio) {
        alert("Error: Los litros finales NO pueden ser mayores a los iniciales.");
        return;
      }
      litrosControlData.value.push({
        id: litrosControlIdCounter.value++,
        ...newLitrosControl.value,
        diferencia_manual: litros_final - litros_inicio,
      });
      newLitrosControl.value = { fecha: today, dispositivo: '', litros_inicio: null, litros_final: null };
    };

    return {
      dispositivos, loadingDevices, getOptionLabel, getOptionLabelById,
      newDato1Item, dato1Data, addDato1,
      newDato2Item, dato2Data, addDato2,
      newLitrosControl, litrosControlData, addLitrosControl
    };
  }
};
</script>

<style scoped>
/* Estilos opcionales */
</style>
