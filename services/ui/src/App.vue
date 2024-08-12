<script setup lang="ts">
import { Authenticator } from '@aws-amplify/ui-vue';
import '@aws-amplify/ui-vue/styles.css';
import NavigationMenu from './components/NavigationMenu/NavigationMenu.vue'
import Splitter from './components/Splitter/Splitter.vue'
import ProductInventoryLayout from './layouts/ProductInventoryLayout.vue';
import CreateProductInventoryLayout from './layouts/CreateProductInventoryLayout.vue';
import {ref, computed} from "vue"

const routes: any = {
	"/": ProductInventoryLayout,
	"/crear-producto": CreateProductInventoryLayout
}

const currentPath = ref(window.location.hash)

window.addEventListener('hashchange', () => {
  currentPath.value = window.location.hash
})

const currentView = computed(() => {
	let _path = currentPath.value

	if (_path !== "/") {
		_path = currentPath.value.slice(1)
	}

	if (Object.keys(routes).includes(_path)) {
		const route: any = routes[_path]
		return route
	} else {
		return undefined
	}
})

</script>

<template>
	<Authenticator username-alias="email" :login-mechanisms="['email']">
		<template v-slot="{ signOut }">
			<NavigationMenu :signOut="signOut"/>

			<div class="pt-1 w-full items-center">
				<Splitter>
					<template #content>
						<component :is="currentView" />
					</template>
				
				</Splitter>
			</div>
		</template>
	</Authenticator>
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
