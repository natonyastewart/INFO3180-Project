import type { RouteRecordRaw } from 'vue-router';
import emitter from '@/eventBus';
import { useGlobalStore } from '@/store';
import { createRouter, createWebHistory } from 'vue-router';
import { isAuthenticated } from '../services/auth';

const routes: Array<RouteRecordRaw> = [
	{
		path: '/',
		name: 'Home',
		component: () => import('../views/Home.vue'),
	},
	{
		path: '/register',
		name: 'Register',
		component: () => import('../views/Register.vue'),
		meta: { requiresNoAuth: true },
	},
	{
		path: '/login',
		name: 'Login',
		component: () => import('../views/Login.vue'),
		meta: { requiresNoAuth: true },
	},
	{
		path: '/logout',
		name: 'Logout',
		redirect: (to) => {
			// Clear token and user info from localStorage
			localStorage.removeItem('token');
			localStorage.removeItem('user');
			emitter.emit('auth:update');
			const gs = useGlobalStore();
			gs.logout();

			return { path: '/login' };
		},
		meta: { requiresAuth: true },
	},
	{
		path: '/profiles/new',
		name: 'NewProfile',
		component: () => import('../views/NewProfileView.vue'),
		meta: { requiresAuth: true },
	},
	{
		path: '/profiles/:id',
		name: 'ProfileDetail',
		component: () => import('@/views/ProfileDetailView.vue'),
		meta: { requiresAuth: true },
	},
	{
		path: '/profiles/favourites',
		name: 'Favorites',
		component: () => import('@/views/FavoritesReportView.vue'),
		meta: { requiresAuth: true },
	},

	{
		path: '/profiles',
		name: 'UserProfile',
		component: () => import('@/views/UserProfileView.vue'),
		meta: { requiresAuth: true },
	},

];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

// Navigation guard to check if user is authenticated
router.beforeEach((to, from, next) => {
	const authenticated = isAuthenticated();
	if (to.matched.some(record => record.meta.requiresNoAuth)
		&& authenticated) {
		next({
			path: '/',
		});
	} else if (to.matched.some(record => record.meta.requiresAuth) && !authenticated) {
		// This route requires auth, check if logged in
		next({
			path: '/login',
			query: { redirect: to.fullPath },
		});
	} else {
		next();
	}
});

export default router;
