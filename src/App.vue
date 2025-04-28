<template>
	<div id="app">
		<NavBar />
		<div class="mt-4 py-12 w-full">
			<div v-if="flashMessage.message" :class="`alert alert-${flashMessage.type}`" role="alert">
				{{ flashMessage.message }}
			</div>
			<router-view />
		</div>
		<footer class="footer mt-5 py-3 bg-light">
			<div class="text-center">
				<p class="text-muted">JamDate &copy; {{ new Date().getFullYear() }}</p>
			</div>
		</footer>
	</div>
</template>

<script lang="ts" setup>
import { onMounted, onUnmounted, ref } from 'vue';
import { useStore } from 'vuex';

import NavBar from './components/NavBar.vue';
import emitter from './eventBus';
import { UserData, key } from './store';

interface FlashMessage {
	message: string;
	type: string;
}

const flashMessage = ref<FlashMessage>({
	message: '',
	type: 'info',
});

const store = useStore(key);

onMounted(() => {
	emitter.on('flash', data => {
		const { message, type = 'info' } = data;
		flashMessage.value = { message, type };

		setTimeout(() => {
			flashMessage.value = { message: '', type: 'info' };
		}, 3000);
	});

	const token = localStorage.getItem('token');
	if (token) {
		store.dispatch('setAuthenticated', true);
		const userData = JSON.parse(localStorage.getItem('user') || '{}') as UserData;
		store.dispatch('setUser', userData);
	}
});

onUnmounted(() => {
	emitter.off('flash');
});
</script>
