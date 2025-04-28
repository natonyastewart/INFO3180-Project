<template>
	<div class="search-form mb-4">
		<h3>Search Profiles</h3>
		<form @submit.prevent="submitSearch">
			<div class="row g-3">
				<div class="col-md-3">
					<input type="text" class="form-control" v-model="searchParams.name" placeholder="Name" />
				</div>
				<div class="col-md-3">
					<input
						type="number"
						class="form-control"
						v-model="searchParams.birth_year"
						placeholder="Birth Year"
					/>
				</div>
				<div class="col-md-2">
					<select class="form-select" v-model="searchParams.sex">
						<option value="">Any Sex</option>
						<option value="Male">Male</option>
						<option value="Female">Female</option>
						<option value="Other">Other</option>
					</select>
				</div>
				<div class="col-md-2">
					<select class="form-select" v-model="searchParams.race">
						<option value="">Any Race</option>
						<option value="Black">Black</option>
						<option value="White">White</option>
						<option value="Asian">Asian</option>
						<option value="Hispanic">Hispanic</option>
						<option value="Mixed">Mixed</option>
						<option value="Other">Other</option>
					</select>
				</div>
				<div class="col-md-2">
					<button type="submit" class="btn btn-primary w-100">Search</button>
				</div>
			</div>
		</form>
	</div>
</template>

<script lang="ts">
export default {
	name: 'SearchForm',
	data() {
		return {
			searchParams: {
				name: '',
				birth_year: '',
				sex: '',
				race: '',
			},
		};
	},
	methods: {
		submitSearch() {
			// Filter out empty values
			const filteredParams = Object.fromEntries(Object.entries(this.searchParams).filter(([_, v]) => v !== ''));
			this.$emit('search', filteredParams);
		},
	},
};
</script>
