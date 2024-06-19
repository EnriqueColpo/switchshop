<script setup lang="ts">
	import { Authenticator } from '@aws-amplify/ui-vue';
	import { reactive, onMounted } from "vue";
	import { Auth } from 'aws-amplify';
	import '@aws-amplify/ui-vue/styles.css';
	import axios from 'axios';

	const API_URL = import.meta.env.VITE_VUE_APP_API_URL || 'http://localhost:8000/api';

	const createBrandForm = reactive({ name: '' })
	const brands = reactive({ data: [] })

	const getConfiguration = async () => {
		const session = await Auth.currentSession()
		const idToken = session.getIdToken()
		const configuration = {
			headers: {
				Authorization: idToken.getJwtToken(),
			}
		}

		return configuration
	}

	const createBrand = async () => {
		const configuration = await getConfiguration()

		const paylaod = {
			name: createBrandForm.name
		}

		await axios.post(
			`${API_URL}/brands/`,
			paylaod,
			configuration
		)

		createBrandForm.name = ''
		await fetchBrands()
	}

	const fetchBrands = async () => {
		const configuration = await getConfiguration()

		const response = await axios.get(
			`${API_URL}/brands/`,
			configuration
		)

		brands.data = response.data.results
	}

	onMounted(() => {
		fetchBrands();
	})

</script>

<template>
	<authenticator username-alias="email" :login-mechanisms="['email']">
		<template v-slot="{ signOut }">
			<el-menu class="el-menu" mode="horizontal" :ellipsis="false">
				<!-- <div class="flex-grow"/> -->
				<el-menu-item index="0" @click="signOut">Sign Out</el-menu-item>
			</el-menu>
			<br />

			<el-row>
				<el-col :span="12" :offset="8">
					<el-card class="box-card">
						<el-form :model="createBrandForm" label-width="120px">
							<el-form-item label="Brand name">
								<el-input v-model="createBrandForm.name" />
							</el-form-item>
							<el-form-item>
								<el-button type="primary" @click="createBrand">Create</el-button>
							</el-form-item>
						</el-form>
					</el-card>
				</el-col>
			</el-row>
			<br />
			<el-row>
				<el-col :span="12" :offset="8">
					<el-card class="box-card">
						<template #header>
							<div class="card-header">
								<span>Brands</span>
							</div>
						</template>
						<el-table :data="brands.data">
							<el-table-column prop="name" label="Name" />
							<el-table-column fixed="right" label="Actions" width="120">
								<!-- <template #default="scope"> -->
								<!-- <el-button link type="primary" size="large"
											@click="closeTask(scope.row.id)">Close</el-button> -->
								<!-- </template> -->
							</el-table-column>
						</el-table>
					</el-card>
				</el-col>
			</el-row>
		</template>
	</authenticator>
</template>



<style lang="scss">
[data-amplify-authenticator] {
	--amplify-components-authenticator-router-box-shadow: 0 0 16px var(--amplify-colors-overlay-10);
	--amplify-components-authenticator-router-border-width: 0;
	--amplify-components-authenticator-form-padding: var(--amplify-space-medium) var(--amplify-space-xl) var(--amplify-space-xl);
	--amplify-components-button-primary-background-color: var(--amplify-colors-neutral-100);
	--amplify-components-fieldcontrol-focus-box-shadow: 0 0 0 2px var(--amplify-colors-purple-60);
	--amplify-components-tabs-item-active-border-color: var(--amplify-colors-neutral-100);
	--amplify-components-tabs-item-color: var(--amplify-colors-neutral-80);
	--amplify-components-tabs-item-active-color: var(--amplify-colors-purple-100);
	--amplify-components-button-link-color: var(--amplify-colors-purple-80);
}

.flex-grow {
	flex-grow: 1;
}
</style>
