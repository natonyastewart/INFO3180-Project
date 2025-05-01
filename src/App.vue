<script lang="ts" setup>
import type { UserData } from './store';
import { onMounted, onUnmounted, ref } from 'vue';

import NavBar from './components/NavBar.vue';
import emitter from './eventBus';
import { useGlobalStore } from './store';

interface FlashMessage {
	message: string;
	type: string;
}

const flashMessage = ref<FlashMessage>({
	message: '',
	type: 'info',
});

const store = useGlobalStore();

onMounted(() => {
	emitter.on('flash', (data) => {
		const { message, type = 'info' } = data;
		flashMessage.value = { message, type };

		setTimeout(() => {
			flashMessage.value = { message: '', type: 'info' };
		}, 3000);
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
	<div id="app">
		<NavBar />
		<div class="mt-4 py-12 w-full">
			<div v-if="flashMessage.message" :class="`alert alert-${flashMessage.type}`" role="alert">
				{{ flashMessage.message }}
			</div>
			<router-view />
		</div>
	</div>
</template>
