<script setup lang="ts">
import { Button } from '@/components/ui/button';
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { loginDto } from '@/services/api.types';
import { toTypedSchema } from '@vee-validate/zod';
import { useForm } from 'vee-validate';
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import emitter from '../eventBus';
import { login } from '../services/auth';

const formSchema = toTypedSchema(loginDto);

const loading = ref(false);
const error = ref<string | null>(null);
const router = useRouter();
const route = useRoute();

const form = useForm({
	validationSchema: formSchema,
});

const onSubmit = form.handleSubmit(async (values) => {
	loading.value = true;
	error.value = null;

	try {
		await login(values);

		emitter.emit('auth:update');

		emitter.emit('flash', {
			message: 'Login successful!',
			type: 'success',
		});

		const redirectPath = route.query.redirect?.toString() || '/';
		router.push(redirectPath);
	} catch (err) {
		error.value = 'Invalid username or password';
	} finally {
		loading.value = false;
	}
});
</script>

<template>
	<div class="login">
		<div class="mt-5">
			<div class="row justify-content-center">
				<div class="col-md-6">
					<div class="card">
						<div class="card-header bg-primary text-white">
							<h3 class="mb-0">
								Login to JamDate
							</h3>
						</div>
						<div class="card-body">
							<div v-if="error" class="alert alert-danger">
								{{ error }}
							</div>

							<form @submit="onSubmit">
								<FormField v-slot="{ componentField }" name="username">
									<FormItem>
										<FormLabel>Username</FormLabel>
										<FormControl>
											<Input
												type="text"
												placeholder="Enter your username"
												v-bind="componentField"
											/>
										</FormControl>
										<FormMessage />
									</FormItem>
								</FormField>

								<FormField v-slot="{ componentField }" name="password">
									<FormItem>
										<FormLabel>Password</FormLabel>
										<FormControl>
											<Input
												type="password"
												placeholder="Enter your password"
												v-bind="componentField"
											/>
										</FormControl>
										<FormMessage />
									</FormItem>
								</FormField>

								<div class="d-grid gap-2 mt-4">
									<Button type="submit" class="w-full" :disabled="loading">
										<span
											v-if="loading"
											class="spinner-border spinner-border-sm me-2"
											role="status"
										/>
										Login
									</Button>
								</div>
							</form>

							<div class="mt-3 text-center">
								Don't have an account? <router-link to="/register">
									Register here
								</router-link>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>
