import type { RouteRecordRaw } from 'vue-router';
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
	},
	{
		path: '/login',
		name: 'Login',
		component: () => import('../views/Login.vue'),
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
