<template>
	<div class="register">
		<div class="mt-5">
			<div class="row justify-content-center">
				<div class="col-md-6">
					<div class="card">
						<div class="card-header bg-primary text-white">
							<h3 class="mb-0">Register for JamDate</h3>
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

								<FormField v-slot="{ componentField }" name="photo">
									<FormItem>
										<FormLabel>Profile Photo</FormLabel>
										<FormControl>
											<Input
												type="file"
												accept="image/*"
												@change="handleFileUpload"
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
										></span>
										Register
									</Button>
								</div>
							</form>

							<div class="mt-3 text-center">
								Already have an account? <router-link to="/login">Login here</router-link>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { Button } from '@/components/ui/button';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
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
const photoFile = ref<File | null>(null);
const router = useRouter();

const form = useForm({
	validationSchema: formSchema,
});

const handleFileUpload = (event: Event) => {
	const target = event.target as HTMLInputElement;
	if (target.files && target.files.length > 0) {
		photoFile.value = target.files[0];
	}
};

const onSubmit = form.handleSubmit(async values => {
	loading.value = true;
	error.value = null;

	try {
		await register(values, photoFile.value);

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
