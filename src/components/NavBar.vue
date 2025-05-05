<script lang="ts" setup>
import type { UserData } from '../store';
import {
	NavigationMenu,
	NavigationMenuItem,
	NavigationMenuLink,
	NavigationMenuList,
} from '@/components/ui/navigation-menu';

import UserDropdownMenu from '@/components/UserDropdownMenu.vue';
import { onMounted, onUnmounted, ref } from 'vue';
import emitter from '../eventBus';
import { getCurrentUser, isAuthenticated } from '../services/auth';

const currentUser = ref<UserData | null>(null);
const isLoggedIn = ref<boolean>(false);

const updateAuthStatus = () => {
	isLoggedIn.value = isAuthenticated();
	currentUser.value = getCurrentUser();
};

onMounted(() => {
	updateAuthStatus();

	emitter.on('auth:update', updateAuthStatus);
});

onUnmounted(() => {
	emitter.off('auth:update', updateAuthStatus);
});
</script>

<template>
	<nav class="bg-primary text-background border-b border-border/20 p-4 flex items-center justify-between">
		<router-link class="font-bold text-2xl" to="/">
			JamDate
		</router-link>
		<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
			<span class="navbar-toggler-icon" />
		</button>
		<NavigationMenu>
			<NavigationMenuList>
				<template v-if="isLoggedIn">
					<NavigationMenuItem>
						<NavigationMenuLink href="/">
							Home
						</NavigationMenuLink>
					</NavigationMenuItem>
					<UserDropdownMenu />
				</template>
				<template v-else>
					<NavigationMenuItem>
						<NavigationMenuLink href="/login">
							Login
						</NavigationMenuLink>
					</NavigationMenuItem>
					<NavigationMenuItem>
						<NavigationMenuLink href="/register">
							Register
						</NavigationMenuLink>
					</NavigationMenuItem>
				</template>
			</NavigationMenuList>
		</NavigationMenu>
	</nav>
</template>
