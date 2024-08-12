<script setup lang="ts">
import ProductInventoryForm from '../components/Forms/ProductInventoryForm.vue';
const redirectToProductDetail = async () => {
	console.log("should redirect to product detail")
}
</script>

<template #table>
    <div class="grid w-full h-110 grid-cols-3 p-1 mb-1 gap-2">
        <div class="w-full col-span-3">
            <ProductInventoryForm :onSubmitCallback="redirectToProductDetail" />
        </div>
    </div>
</template>

