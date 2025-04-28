<template>
	<nav class="bg-primary text-background border-b border-border/20 p-4 flex items-center justify-between">
		<router-link class="font-bold text-2xl" to="/">JamDate</router-link>
		<button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
			<span class="navbar-toggler-icon"></span>
		</button>
		<NavigationMenu>
			<NavigationMenuList>
				<template v-if="isLoggedIn">
					<NavigationMenuItem>
						<NavigationMenuLink href="/"> Home </NavigationMenuLink>
					</NavigationMenuItem>
				</template>
				<template v-else>
					<NavigationMenuItem>
						<NavigationMenuLink href="/login"> Login </NavigationMenuLink>
					</NavigationMenuItem>
					<NavigationMenuItem>
						<NavigationMenuLink href="/register"> Register </NavigationMenuLink>
					</NavigationMenuItem>
				</template>
			</NavigationMenuList>
		</NavigationMenu>
		<!-- <div class="collapse navbar-collapse" id="navbarNav">
			<ul class="navbar-nav me-auto">
				<li class="nav-item" v-if="isLoggedIn">
					<router-link class="nav-link" to="/">Home</router-link>
				</li>
			</ul>
			<ul class="navbar-nav ms-auto">
				<template v-if="isLoggedIn">
					<li class="nav-item">
						<router-link class="nav-link" :to="`/users/${currentUser?.id}`">My Profile</router-link>
					</li>
					<li class="nav-item">
						<router-link class="nav-link" to="/profiles/new">New Profile</router-link>
					</li>
					<li class="nav-item">
						<router-link class="nav-link" to="/profiles/favourites">Favorites</router-link>
					</li>
					<li class="nav-item">
						<router-link class="nav-link" to="/logout">Logout</router-link>
					</li>
				</template>
				<template v-else>
					<li class="nav-item">
						<router-link class="nav-link" to="/login">Login</router-link>
					</li>
					<li class="nav-item">
						<router-link class="nav-link" to="/register">Register</router-link>
					</li>
				</template>
			</ul>
		</div> -->
	</nav>
</template>

<script lang="ts" setup>
import {
	NavigationMenu,
	NavigationMenuItem,
	NavigationMenuLink,
	NavigationMenuList,
} from '@/components/ui/navigation-menu';
import { onMounted, onUnmounted, ref } from 'vue';

import emitter from '../eventBus';
import { getCurrentUser, isAuthenticated } from '../services/auth';
import { UserData } from '../store';

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
