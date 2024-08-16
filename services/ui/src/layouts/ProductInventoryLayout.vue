<script setup lang="ts">
import { reactive, onMounted } from "vue";
import '@aws-amplify/ui-vue/styles.css';
import axios from 'axios';
const API_URL = import.meta.env.VITE_VUE_APP_API_URL || 'http://localhost:8000/api';
import ProductInventoryTable from '../components/Table/ProductInventoryTable.vue';
import { getConfiguration } from '../auth/getConfiguration';

const productInventory = reactive({ data: [] })

const fetchProductInventory = async () => {
	const configuration = await getConfiguration()
	const response = await axios.get(
		`${API_URL}/health-check`,
		configuration
	)
	productInventory.data = response.data.results
}

onMounted(() => {
	fetchProductInventory();
})

</script>

<template #table>
    <div class="grid w-full h-110 grid-cols-3 p-1 mb-1 gap-2">
        <div class="w-full col-span-3">

            <ProductInventoryTable :table-data="productInventory.data" />
        </div>
    </div>

</template>