<script lang="ts" setup>
import type { UserData } from './store';
import { Toaster } from '@/components/ui/sonner';

import { onMounted, onUnmounted } from 'vue';
import { toast } from 'vue-sonner';
import NavBar from './components/NavBar.vue';
import emitter from './eventBus';
import { useGlobalStore } from './store';

const store = useGlobalStore();

onMounted(() => {
	emitter.on('flash', (data) => {
		const { message, type = 'info' } = data;

		switch (type) {
			case 'success':
				toast.success(message);
				break;
			case 'error':
				toast.error(message);
				break;
			case 'warning':
				toast.warning(message);
				break;
			case 'info':
				toast.info(message);
				break;
		}
	});

	const token = localStorage.getItem('token');
	if (token) {
		store.setAuthenticated(true);
		const userData = JSON.parse(localStorage.getItem('user') || '{}') as UserData;
		store.setUser(userData);
	}
});

onUnmounted(() => {
	emitter.off('flash');
});
</script>

<template>
	<Toaster position="top-right" />

	<div id="app">
		<NavBar />
		<div class="mt-4 py-12 w-full">
			<router-view />
		</div>
	</div>
</template>
