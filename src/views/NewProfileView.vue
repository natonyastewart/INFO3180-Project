<script setup lang="ts">
import { Button } from '@/components/ui/button';
import Card from '@/components/ui/card/Card.vue';
import CardContent from '@/components/ui/card/CardContent.vue';
import CardHeader from '@/components/ui/card/CardHeader.vue';
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { createProfileDto } from '@/services/api.types';
import { toTypedSchema } from '@vee-validate/zod';
import { useForm } from 'vee-validate';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import emitter from '../eventBus';
import { createProfile, uploadProfilePhoto } from '../services/api';

const formSchema = toTypedSchema(createProfileDto);

const loading = ref(false);
const error = ref<string | null>(null);
const router = useRouter();
const selectedFile = ref<File | null>(null);

const form = useForm({
	validationSchema: formSchema,
	initialValues: {
		description: '',
		parish: '',
		biography: '',
		sex: '',
		race: '',
		birth_year: new Date().getFullYear() - 30,
		height: 65,
		fav_cuisine: '',
		fav_colour: '',
		fav_school_subject: '',
		political: false,
		religious: false,
		family_oriented: false,
	},
});

const handleFileUpload = (event: Event) => {
	const input = event.target as HTMLInputElement;
	const file = input.files?.[0];
	if (file) {
		selectedFile.value = file;
	}
};

const onSubmit = form.handleSubmit(async (values) => {
	loading.value = true;
	error.value = null;

	try {
		const res = await createProfile(values);

		if (selectedFile.value && res.data) {
			await uploadProfilePhoto(res.data.id, selectedFile.value);
		}
		// Show success message
		emitter.emit('flash', {
			message: 'Profile created successfully!',
			type: 'success',
		});

		// Redirect to profiles page
		router.push('/profiles');
	} catch (err: any) {
		error.value = err.message || 'Something went wrong while creating your profile.';
	} finally {
		loading.value = false;
	}
});
</script>

<template>
	<main>
		<div class="mt-5">
			<div class="flex justify-center">
				<Card class="w-full max-w-3xl">
					<CardHeader class="text-xl font-bold">
						Create Your Profile
					</CardHeader>
					<CardContent>
						<div v-if="error" class="p-4 border border-destructive rounded-lg bg-destructive/10 text-destructive mb-4">
							{{ error }}
						</div>

						<form class="space-y-6" @submit="onSubmit">
							<!-- Profile Image Upload -->
							<div class="space-y-2">
								<FormLabel>Profile Picture</FormLabel>
								<Input type="file" accept="image/*" @change="handleFileUpload" />
							</div>

							<!-- Description -->
							<FormField v-slot="{ componentField }" name="description">
								<FormItem>
									<FormLabel>Description</FormLabel>
									<FormControl>
										<Input type="text" placeholder="Enter description" v-bind="componentField" />
									</FormControl>
									<FormMessage />
								</FormItem>
							</FormField>

							<!-- Parish -->
							<FormField v-slot="{ componentField }" name="parish">
								<FormItem>
									<FormLabel>Parish</FormLabel>
									<FormControl>
										<Input type="text" placeholder="Enter parish" v-bind="componentField" />
									</FormControl>
									<FormMessage />
								</FormItem>
							</FormField>

							<!-- Biography -->
							<FormField v-slot="{ componentField }" name="biography">
								<FormItem>
									<FormLabel>Biography</FormLabel>
									<FormControl>
										<textarea
											v-bind="componentField"
											class="flex h-20 w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-xs focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
											placeholder="Tell us about yourself"
										/>
									</FormControl>
									<FormMessage />
								</FormItem>
							</FormField>

							<!-- Sex & Race -->
							<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
								<FormField v-slot="{ componentField }" name="sex">
									<FormItem>
										<FormLabel>Sex</FormLabel>
										<FormControl>
											<select
												v-bind="componentField"
												class="flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-base shadow-xs transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50"
											>
												<option disabled value="">
													Select your sex
												</option>
												<option>Male</option>
												<option>Female</option>
												<option>Non-Binary</option>
												<option>Prefer Not To Say</option>
												<option>Other</option>
											</select>
										</FormControl>
										<FormMessage />
									</FormItem>
								</FormField>

								<FormField v-slot="{ componentField }" name="race">
									<FormItem>
										<FormLabel>Race</FormLabel>
										<FormControl>
											<Input type="text" placeholder="Enter race" v-bind="componentField" />
										</FormControl>
										<FormMessage />
									</FormItem>
								</FormField>
							</div>

							<!-- Birth Year & Height -->
							<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
								<FormField v-slot="{ componentField }" name="birth_year">
									<FormItem>
										<FormLabel>Birth Year</FormLabel>
										<FormControl>
											<Input type="number" min="1900" :max="new Date().getFullYear()" v-bind="componentField" />
										</FormControl>
										<FormMessage />
									</FormItem>
								</FormField>

								<FormField v-slot="{ componentField }" name="height">
									<FormItem>
										<FormLabel>Height (inches)</FormLabel>
										<FormControl>
											<Input type="number" step="0.1" v-bind="componentField" />
										</FormControl>
										<FormMessage />
									</FormItem>
								</FormField>
							</div>

							<!-- Cuisine & Colour -->
							<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
								<FormField v-slot="{ componentField }" name="fav_cuisine">
									<FormItem>
										<FormLabel>Favorite Cuisine</FormLabel>
										<FormControl>
											<Input type="text" v-bind="componentField" />
										</FormControl>
										<FormMessage />
									</FormItem>
								</FormField>

								<FormField v-slot="{ componentField }" name="fav_colour">
									<FormItem>
										<FormLabel>Favorite Colour</FormLabel>
										<FormControl>
											<Input type="text" v-bind="componentField" />
										</FormControl>
										<FormMessage />
									</FormItem>
								</FormField>
							</div>

							<!-- Favorite School Subject -->
							<FormField v-slot="{ componentField }" name="fav_school_subject">
								<FormItem>
									<FormLabel>Favorite School Subject</FormLabel>
									<FormControl>
										<Input type="text" v-bind="componentField" />
									</FormControl>
									<FormMessage />
								</FormItem>
							</FormField>

							<!-- Checkboxes -->
							<div class="flex flex-wrap gap-6 mt-6">
								<FormField v-slot="{ componentField }" name="political">
									<FormItem class="flex items-center space-x-2">
										<FormControl>
											<input type="checkbox" v-bind="componentField">
										</FormControl>
										<FormLabel>Political</FormLabel>
									</FormItem>
								</FormField>

								<FormField v-slot="{ componentField }" name="religious">
									<FormItem class="flex items-center space-x-2">
										<FormControl>
											<input type="checkbox" v-bind="componentField">
										</FormControl>
										<FormLabel>Religious</FormLabel>
									</FormItem>
								</FormField>

								<FormField v-slot="{ componentField }" name="family_oriented">
									<FormItem class="flex items-center space-x-2">
										<FormControl>
											<input type="checkbox" v-bind="componentField">
										</FormControl>
										<FormLabel>Family Oriented</FormLabel>
									</FormItem>
								</FormField>
							</div>

							<!-- Submit Button -->
							<Button type="submit" class="w-full" :disabled="loading">
								<span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status" />
								Submit Profile
							</Button>
						</form>
					</CardContent>
				</Card>
			</div>
		</div>
	</main>
</template>
