<template>
	<div class="card h-100">
		<img :src="profile.photo || '/default-profile.jpg'" class="card-img-top" alt="Profile Photo" />
		<div class="card-body">
			<h5 class="card-title">{{ profile.name }}</h5>
			<p class="card-text">
				<strong>Parish:</strong> {{ profile.parish }}<br />
				<strong>Age:</strong> {{ calculateAge(profile.birth_year) }}<br />
				<strong>Sex:</strong> {{ profile.sex }}
			</p>
			<div class="d-flex justify-content-between">
				<router-link :to="`/profiles/${profile.id}`" class="btn btn-primary"> View more details </router-link>
				<favorite-button
					:profile-id="profile.id"
					:is-favorite="isFavorite"
					@toggle="$emit('toggle-favorite')"
				/>
			</div>
		</div>
	</div>
</template>

<script lang="ts">
import FavoriteButton from './FavoriteButton.vue';

export default {
	name: 'ProfileCard',
	components: {
		FavoriteButton,
	},
	props: {
		profile: {
			type: Object,
			required: true,
		},
		isFavorite: {
			type: Boolean,
			default: false,
		},
	},
	methods: {
		calculateAge(birthYear) {
			const currentYear = new Date().getFullYear();
			return currentYear - birthYear;
		},
	},
};
</script>
