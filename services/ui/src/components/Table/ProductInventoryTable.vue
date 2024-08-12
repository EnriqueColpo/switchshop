<template>
	<el-table :data="tableData" max-height="400px" size="small" class="text-[8px] rounded-sm" scrollbar-always-on>
		<el-table-column prop="ProductName" label="Nombre" />
		<el-table-column prop="LocationId" label="Sucursal" />
		<el-table-column prop="CategoryName" label="Categoria" />
		<el-table-column prop="BrandName" label="Marca" />
		<el-table-column prop="Description" label="Descripción" />
		<el-table-column prop="Price" label="Precio" />
		<el-table-column prop="TotalStockQuantity" label="Cantidad Total" />
		<el-table-column prop="LastRestockDate" label="Última reposición" />
	</el-table>
</template>

<script lang="ts" setup>
	const props = defineProps({
		tableData: {
			type: Array,
			required: true,
		},
	})
</script>