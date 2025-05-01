import type { RouteRecordRaw } from 'vue-router';
import { createRouter, createWebHistory } from 'vue-router';

import { isAuthenticated } from '../services/auth';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import NewProfileView from '../views/NewProfileView.vue';
import ProfileDetailView from '@/views/ProfileDetailView.vue';
import FavoritesReportView from '@/views/FavoritesReportView.vue';
import UserProfileView from '@/views/UserProfileView.vue';

const routes: Array<RouteRecordRaw> = [
	{
		path: '/',
		name: 'Home',
		component: Home,
	},
	{
		path: '/register',
		name: 'Register',
		component: Register,
	},
	{
		path: '/login',
		name: 'Login',
		component: Login,
	},
	{
		path: '/logout',
		name: 'Logout',
		redirect: (to) => {
			// Clear token and user info from localStorage
			localStorage.removeItem('token');
			localStorage.removeItem('user');
			return { path: '/login' };
		},
	},
	{
		path: '/about',
		name: 'About',
		component: () => import('../views/AboutView.vue'),
	},
	{
		path: '/profiles/new',
		name: 'NewProfile',
		component: NewProfileView,
	},
	{
		path: '/profiles/:id',
		name: 'ProfileDetail',
		component: ProfileDetailView,
	},
	{
		path: '/profiles/favorites',
		name: 'Favorites',
		component: FavoritesReportView,
	},
	
	{
		path: '/profiles/me',
		name: 'UserProfile',
		component: UserProfileView,
	}
	  
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

// Navigation guard to check if user is authenticated
router.beforeEach((to, from, next) => {
	if (to.matched.some(record => record.meta.requiresAuth)) {
		// This route requires auth, check if logged in
		if (!isAuthenticated()) {
			next({
				path: '/login',
				query: { redirect: to.fullPath },
			});
		} else {
			next();
		}
	} else {
		next();
	}
});

export default router;
