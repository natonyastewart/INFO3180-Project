<script setup lang="ts">
import { Button } from '@/components/ui/button';
import Card from '@/components/ui/card/Card.vue';
import CardContent from '@/components/ui/card/CardContent.vue';
import CardHeader from '@/components/ui/card/CardHeader.vue';
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { registerUserDto } from '@/services/api.types';
import { toTypedSchema } from '@vee-validate/zod';

import { useForm } from 'vee-validate';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import emitter from '../eventBus';
import { register } from '../services/auth';

const formSchema = toTypedSchema(registerUserDto);

const loading = ref(false);
const error = ref<string | null>(null);
const router = useRouter();

const form = useForm({
	validationSchema: formSchema,
});

const onSubmit = form.handleSubmit(async (values) => {
	loading.value = true;
	error.value = null;

	try {
		await register(values);

		// Show success message
		emitter.emit('flash', {
			message: 'Registration successful! Please log in.',
			type: 'success',
		});

		// Redirect to login page
		router.push('/login');
	} catch (err: any) {
		error.value = err.message || 'Registration failed. Please try again.';
	} finally {
		loading.value = false;
	}
});
</script>

<template>
	<main>
		<div class="mt-5">
			<div class="flex justify-center">
				<div>
					<Card>
						<CardHeader class="text-xl font-bold">
							Register for JamDate
						</CardHeader>
						<CardContent>
							<div v-if="error" class="p-4 border border-danger rounded-lg bg-danger/10 text-danger mb-4">
								{{ error }}
							</div>

							<form class="space-y-6" @submit="onSubmit">
								<FormField v-slot="{ componentField }" name="username">
									<FormItem>
										<FormLabel>Username</FormLabel>
										<FormControl>
											<Input type="text" placeholder="Enter username" v-bind="componentField" />
										</FormControl>
										<FormMessage />
									</FormItem>
								</FormField>

								<FormField v-slot="{ componentField }" name="name">
									<FormItem>
										<FormLabel>Full Name</FormLabel>
										<FormControl>
											<Input
												type="text"
												placeholder="Enter your full name"
												v-bind="componentField"
											/>
										</FormControl>
										<FormMessage />
									</FormItem>
								</FormField>

								<FormField v-slot="{ componentField }" name="email">
									<FormItem>
										<FormLabel>Email</FormLabel>
										<FormControl>
											<Input
												type="email"
												placeholder="Enter your email"
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
										Register
									</Button>
								</div>
							</form>

							<div class="mt-3 text-center">
								Already have an account? <span class="text-primary">
									<router-link to="/login">
										Login here
									</router-link>
								</span>
							</div>
						</CardContent>
					</Card>
				</div>
			</div>
		</div>
	</main>
</template>
