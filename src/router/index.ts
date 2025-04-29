import { RouteRecordRaw, createRouter, createWebHistory } from 'vue-router';

import { isAuthenticated } from '../services/auth';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import NewProfileView from '../views/NewProfileView.vue';
import ProfileDetailView from '..@/views/ProfileDetailView.vue';
import FavouritesReportView from '..@/views/FavouritesReportView.vue';


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
		redirect: to => {
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
		path: '/profiles/:profile_id', 
		name: 'Profile',
		component: ProfileDetailView 
	},
	{ 
		path: '/profiles/favourites',
		name: 'Favorites', 
		component: FavouritesReportView 
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
