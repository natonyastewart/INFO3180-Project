<script setup lang="ts">
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { FormControl, FormField, FormItem, FormLabel } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { SearchIcon } from 'lucide-vue-next';
import { useForm } from 'vee-validate';

const emit = defineEmits(['search']);

const form = useForm({
	initialValues: {
		name: '',
		birth_year: '',
		sex: '',
		race: '',
	},
});

const submitSearch = form.handleSubmit((values) => {
	// Filter out empty values
	const filteredParams = Object.fromEntries(Object.entries(values).filter(([_, v]) => v !== '' && v !== '*'));
	emit('search', filteredParams);
});
</script>

<template>
	<Card class="mb-4 p-6 w-fit">
		<h3 class="text-xl font-bold mb-4">
			Search Profiles
		</h3>
		<form @submit="submitSearch">
			<div class="grid grid-cols-1 tablet:flex gap-4">
				<!-- Name Field -->
				<div>
					<FormField v-slot="{ componentField }" name="name">
						<FormItem>
							<FormLabel>Name</FormLabel>
							<FormControl>
								<Input type="text" placeholder="Enter name" v-bind="componentField" />
							</FormControl>
						</FormItem>
					</FormField>
				</div>

				<!-- Birth Year Field -->
				<div>
					<FormField v-slot="{ componentField }" name="birth_year">
						<FormItem>
							<FormLabel>Birth Year</FormLabel>
							<FormControl>
								<Input type="number" placeholder="Enter birth year" v-bind="componentField" />
							</FormControl>
						</FormItem>
					</FormField>
				</div>

				<!-- Sex Field -->
				<div>
					<FormField v-slot="{ componentField }" name="sex">
						<FormItem>
							<FormLabel>Sex</FormLabel>
							<Select v-bind="componentField">
								<FormControl>
									<SelectTrigger class="w-full">
										<SelectValue placeholder="Any Sex" />
									</SelectTrigger>
								</FormControl>
								<SelectContent>
									<SelectGroup>
										<SelectItem value="*">
											Any Sex
										</SelectItem>
										<SelectItem value="Male">
											Male
										</SelectItem>
										<SelectItem value="Female">
											Female
										</SelectItem>
										<SelectItem value="Other">
											Other
										</SelectItem>
									</SelectGroup>
								</SelectContent>
							</Select>
						</FormItem>
					</FormField>
				</div>

				<!-- Race Field -->
				<div>
					<FormField v-slot="{ componentField }" name="race">
						<FormItem>
							<FormLabel>Race</FormLabel>
							<Select v-bind="componentField">
								<FormControl>
									<SelectTrigger class="w-full">
										<SelectValue placeholder="Any Race" />
									</SelectTrigger>
								</FormControl>
								<SelectContent>
									<SelectGroup>
										<SelectItem value="*">
											Any Race
										</SelectItem>
										<SelectItem value="Black">
											Black
										</SelectItem>
										<SelectItem value="White">
											White
										</SelectItem>
										<SelectItem value="Asian">
											Asian
										</SelectItem>
										<SelectItem value="Hispanic">
											Hispanic
										</SelectItem>
										<SelectItem value="Mixed">
											Mixed
										</SelectItem>
										<SelectItem value="Other">
											Other
										</SelectItem>
									</SelectGroup>
								</SelectContent>
							</Select>
						</FormItem>
					</FormField>
				</div>

				<!-- Submit Button -->
				<div class="w-full tablet:w-fit self-end">
					<Button type="submit" class="w-full">
						<SearchIcon />
						Search
					</Button>
				</div>
			</div>
		</form>
	</Card>
</template>
