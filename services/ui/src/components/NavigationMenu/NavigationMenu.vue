<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { ref } from 'vue'
import {
    NavigationMenuItem,
    NavigationMenuLink,
    NavigationMenuList,
    NavigationMenuRoot,
    NavigationMenuTrigger,
    NavigationMenuViewport,
} from 'radix-vue'
import './style.css'

const currentTrigger = ref('')

const props = defineProps({
    signOut: {
        type: Function,
        required: true,
    }
})

</script>

<template>
    <NavigationMenuRoot v-model="currentTrigger" class="NavigationMenuRoot">
        <NavigationMenuList class="NavigationMenuList">
            <NavigationMenuItem>
                <img src="../../assets/switch_small.png" :style="{ height: '26px' }" />
            </NavigationMenuItem>

            <NavigationMenuItem>
                <NavigationMenuLink
                    class="NavigationMenuLink"
                    href="#/"
                >
                    Home    
                </NavigationMenuLink>
            </NavigationMenuItem>

            <NavigationMenuItem>
                <NavigationMenuLink
                    class="NavigationMenuLink"
                    href="#/crear-producto"
                >
                    Nuevo producto    
                </NavigationMenuLink>
            </NavigationMenuItem>

            <NavigationMenuItem>
                <NavigationMenuTrigger class="NavigationMenuTrigger">
                    Ventas
                    <Icon icon="radix-icons:caret-down" class="CaretDown" />
                </NavigationMenuTrigger>
            </NavigationMenuItem>

            <NavigationMenuItem class="NavigationMenuLink">
                <button
                    class="NavigationButton"
                    :style="{ padding: 0, margin: 0 }"
                    @click="props.signOut"
                >
                    Salir
                </button>
            </NavigationMenuItem>
        </NavigationMenuList>

        <div class="ViewportPosition">
            <NavigationMenuViewport class="NavigationMenuViewport" />
        </div>
    </NavigationMenuRoot>
</template>
