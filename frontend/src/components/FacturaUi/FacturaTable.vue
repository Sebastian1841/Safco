<template>
    <div class="bg-white rounded-xl shadow p-4">
        <!-- TABLA -->
        <div class="border rounded-lg overflow-hidden">

            <!-- HEADER TABLA -->
            <div class="flex items-center bg-gray-800 text-white p-3 font-semibold text-xs uppercase tracking-wider">
                <div class="w-10 flex justify-center">
                    <input type="checkbox" :checked="isAllSelected" @change="toggleSelectAll"
                        class="h-4 w-4 rounded border-gray-300" />
                </div>
                <div class="w-32">N° Factura</div>
                <div class="flex-1">Producto</div>
                <div class="w-24 text-right">Litros</div>
                <div class="w-32 text-center">Fecha</div>
                <div class="w-32 text-right">Total</div>
            </div>

            <!-- CUERPO TABLA -->
            <div class="max-h-[55vh] overflow-y-auto divide-y divide-gray-200">

                <div v-for="f in paginated" :key="f.id" class="flex items-center p-3 text-sm hover:bg-blue-50">
                    <!-- Checkbox fila -->
                    <div class="w-10 flex justify-center">
                        <input type="checkbox" :value="f.id" v-model="selected"
                            class="h-4 w-4 rounded border-gray-300" />
                    </div>

                    <div class="w-32 font-mono">{{ f.numero_factura }}</div>

                    <div class="flex-1 truncate">{{ f.producto }}</div>

                    <div class="w-24 text-right font-semibold">
                        {{ Math.round(f.litros).toLocaleString("es-CL") }} L
                    </div>

                    <div class="w-32 text-center">
                        {{ f.fecha }}
                    </div>

                    <div class="w-32 text-right font-bold text-green-600">
                        ${{ f.total.toLocaleString("es-CL") }}
                    </div>
                </div>

            </div>
        </div>

        <!-- PAGINACIÓN -->
        <div
            class="flex justify-between items-center mt-4 text-xs text-gray-700 bg-white p-3 rounded-lg shadow-inner border border-gray-200">

            <div class="flex items-center gap-2">
                <span class="font-medium">Filas:</span>
                <select v-model.number="rows" class="border rounded px-2 py-1 bg-gray-50 focus:ring-blue-500">
                    <option v-for="n in [5, 10, 20, 30, 40]" :key="n">{{ n }}</option>
                </select>
            </div>

            <div class="flex items-center gap-3">
                <button @click="prevPage" :disabled="page === 1"
                    class="px-2 py-1 bg-gray-100 border rounded hover:bg-blue-600 hover:text-white disabled:opacity-50">
                    <SvgIcon name="chevron-left" class="w-3 h-3" />
                </button>

                <span>Pág. <b>{{ page }}</b> / <b>{{ totalPages }}</b></span>

                <button @click="nextPage" :disabled="page === totalPages"
                    class="px-2 py-1 bg-gray-100 border rounded hover:bg-blue-600 hover:text-white disabled:opacity-50">
                    <SvgIcon name="chevron-right" class="w-3 h-3" />
                </button>
            </div>

        </div>

    </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import SvgIcon from '@/components/icons/SvgIcon.vue';

const props = defineProps({
    facturas: Array,
    modelValue: { type: Array, default: () => [] }
});

const emit = defineEmits(["update:modelValue"]);

const selected = ref([...props.modelValue]);

// Emitimos cada vez que cambie
watch(selected, (val) => emit("update:modelValue", val));

// Seleccionar todo
const isAllSelected = computed(() =>
    props.facturas.length > 0 && selected.value.length === props.facturas.length
);

const toggleSelectAll = () => {
    if (isAllSelected.value) selected.value = [];
    else selected.value = props.facturas.map((x) => x.id);
};



// PAGINACIÓN
const rows = ref(5);
const page = ref(1);

const totalPages = computed(() =>
    Math.ceil(props.facturas.length / rows.value)
);

const paginated = computed(() => {
    const start = (page.value - 1) * rows.value;
    return props.facturas.slice(start, start + rows.value);
});

watch([rows, () => props.facturas], () => {
    page.value = 1;
});

const nextPage = () => {
    if (page.value < totalPages.value) page.value++;
};

const prevPage = () => {
    if (page.value > 1) page.value--;
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.25s;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>
