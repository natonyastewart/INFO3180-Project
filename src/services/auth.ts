import type { LoginDto, RegisterUserDto } from '@/services/api.types';
import type { UserData } from '@/store';
import { API_URL } from '@/constants';
import axios from 'axios';

export const register = async (userData: RegisterUserDto) => {
	try {
		const response = await axios.post(`${API_URL}/register`, userData);
		return response.data;
	} catch (error: any) {
		throw error.response ? error.response.data : error;
	}
};

export const login = async (credentials: LoginDto) => {
	try {
		const response = await axios.post(`${API_URL}/auth/login`, credentials);
		if (response.data.token) {
			localStorage.setItem('token', response.data.token);
			localStorage.setItem('user', JSON.stringify(response.data.user));
		}
		return response.data;
	} catch (error: any) {
		throw error.response ? error.response.data : error;
	}
};

export const logout = async () => {
	try {
		await axios.post(
			`${API_URL}/auth/logout`,
			{},
			{
				headers: { Authorization: `Bearer ${getToken()}` },
			},
		);
		localStorage.removeItem('token');
		localStorage.removeItem('user');
	} catch (error) {
		console.error('Logout error:', error);
		// Still clear local storage even if API call fails
		localStorage.removeItem('token');
		localStorage.removeItem('user');
	}
};

export const getToken = (): string | null => {
	return localStorage.getItem('token');
};

export const getCurrentUser = (): UserData | null => {
	const userStr = localStorage.getItem('user');
	return userStr ? JSON.parse(userStr) : null;
};

export const isAuthenticated = (): boolean => {
	return !!getToken();
};

// Setup axios interceptor to include token in every request
axios.interceptors.request.use(
	(config) => {
		const token = getToken();
		if (token && config.headers) {
			config.headers.Authorization = `Bearer ${token}`;
		}
		return config;
	},
	(error) => {
		return Promise.reject(error);
	},
);
