<script setup lang="ts">
import { reactive } from "vue";
import { getConfiguration } from '../../auth/getConfiguration';
import axios from 'axios';

const API_URL = import.meta.env.VITE_VUE_APP_API_URL || 'http://localhost:8000/api';

const props = defineProps({
    onSubmitCallback: {
        type: Function,
        required: true,
    }
})

const createProductInventoryForm = reactive({
    product_name: "",
    location_id: "switch",
    category_name: "",
    brand_name: "",
    description: "",
    price: "",
    total_stock_quantity: "",
    last_restock_date: "",
    inventory: ""
})

const createBrand = async () => {
	const configuration = await getConfiguration()

	const paylaod = {
        product_name: createProductInventoryForm.product_name,
        location_id: createProductInventoryForm.location_id,
        category_name: createProductInventoryForm.category_name,
        brand_name: createProductInventoryForm.brand_name,
        description: createProductInventoryForm.description,
        price: createProductInventoryForm.price,
        total_stock_quantity: createProductInventoryForm.total_stock_quantity,
        last_restock_date: createProductInventoryForm.last_restock_date,
        inventory: JSON.parse(createProductInventoryForm.inventory || "[]"),
	}

    try {
        await axios.post(
            `${API_URL}/product_inventory/`,
            paylaod,
            configuration
        )
    } catch (error) {
        console.error(error)
    }

    createProductInventoryForm.product_name = ""
    createProductInventoryForm.location_id = ""
    createProductInventoryForm.category_name = ""
    createProductInventoryForm.brand_name = ""
    createProductInventoryForm.description = ""
    createProductInventoryForm.price = ""
    createProductInventoryForm.total_stock_quantity = ""
    createProductInventoryForm.last_restock_date = ""
    createProductInventoryForm.inventory = ""
	await props.onSubmitCallback()
}
</script>

<template>
    <div class="grid w-full h-110 grid-cols-3 p-1 mb-1 gap-2">
        <div class="w-full col-span-3">
            <input
                v-model="createProductInventoryForm.product_name"
                type="text"
                placeholder="Nombre"
                class="w-full pl-2 h-6 rounded-sm ring-1 ring-slate-200 shadow-sm text-[8px]"
            />
        </div>

        <div class="w-full col-span-3">
            <input
                v-model="createProductInventoryForm.category_name"
                type="text"
                placeholder="Categoria"
                class="w-full pl-2 h-6 rounded-sm ring-1 ring-slate-200 shadow-sm text-[8px]"
            />
        </div>

        <div class="w-full col-span-3">
            <input
                v-model="createProductInventoryForm.brand_name"
                type="text"
                placeholder="Marca"
                class="w-full pl-2 h-6 rounded-sm ring-1 ring-slate-200 shadow-sm text-[8px]"
            />
        </div>
        <div class="w-full col-span-3">
            <input
                v-model="createProductInventoryForm.description"
                type="text"
                placeholder="Descripción"
                class="w-full pl-2 h-6 rounded-sm ring-1 ring-slate-200 shadow-sm text-[8px]"
            />
        </div>
        <div class="w-full col-span-3">
            <input
                v-model="createProductInventoryForm.price"
                type="text"
                placeholder="Precio"
                class="w-full pl-2 h-6 rounded-sm ring-1 ring-slate-200 shadow-sm text-[8px]"
            />
        </div>
        <div class="w-full col-span-3">
            <input
                v-model="createProductInventoryForm.total_stock_quantity"
                type="text"
                placeholder="Cantidad total"
                class="w-full pl-2 h-6 rounded-sm ring-1 ring-slate-200 shadow-sm text-[8px]"
            />
        </div>
        <div class="w-full col-span-3">
            <input
                v-model="createProductInventoryForm.last_restock_date"
                type="text"
                placeholder="Fecha de reposición"
                class="w-full pl-2 h-6 rounded-sm ring-1 ring-slate-200 shadow-sm text-[8px]"
            />
        </div>
        <div class="w-full col-span-3">
            <input
                v-model="createProductInventoryForm.inventory"
                type="text"
                placeholder="Inventario"
                class="w-full pl-2 h-6 rounded-sm ring-1 ring-slate-200 shadow-sm text-[8px]"
            />
        </div>
        <div class="w-full col-span-3">
            <button
                @click="createBrand"
                class="w-full h-6 rounded-sm ring-1 ring-slate-200 shadow-sm text-center bg-[#EEEEEE] text-[8px]"
            >
                Enviar
            </button>
        </div>
    </div>
</template>