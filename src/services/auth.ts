import type { ApiResponse, AuthResponse, LoginDto, RegisterUserDto } from '@/services/api.types';
import type { UserData } from '@/store';
import type { AxiosError } from 'axios';
import { API_URL } from '@/constants';
import axios from 'axios';

// Flag to prevent multiple refresh token requests
let isRefreshing = false;
// Queue of callbacks to be executed after token refresh
let refreshSubscribers: ((token: string) => void)[] = [];

// Function to add callbacks to the queue
const subscribeTokenRefresh = (callback: (token: string) => void) => {
	refreshSubscribers.push(callback);
};

// Function to execute all callbacks with the new token
const onTokenRefreshed = (token: string) => {
	refreshSubscribers.forEach(callback => callback(token));
	refreshSubscribers = [];
};

export const register = async ({ photo, ...userData }: RegisterUserDto): Promise<ApiResponse<AuthResponse>> => {
	const formData = new FormData();
	Object.entries(userData).forEach(([key, value]) => {
		formData.append(key, value);
	});

	if (photo) {
		console.debug('Adding photo to formData');
		formData.append('photo', photo);
	}

	try {
		const response = await axios.post<ApiResponse<AuthResponse>>(`${API_URL}/register`, formData, {
			headers: {
				'Content-Type': 'multipart/form-data',
			},
		});

		if (response.data.data?.token) {
			localStorage.setItem('token', response.data.data.token);
			localStorage.setItem('refreshToken', response.data.data.refreshToken);
			localStorage.setItem('user', JSON.stringify(response.data.data.user));
		}
		return response.data;
	} catch (error: any) {
		throw error.response ? error.response.data : error;
	}
};

export const login = async (credentials: LoginDto): Promise<ApiResponse<AuthResponse>> => {
	try {
		const response = await axios.post<ApiResponse<AuthResponse>>(`${API_URL}/auth/login`, credentials);
		if (response.data.data?.token) {
			localStorage.setItem('token', response.data.data.token);
			localStorage.setItem('refreshToken', response.data.data.refreshToken);
			localStorage.setItem('user', JSON.stringify(response.data.data.user));
		}
		return response.data;
	} catch (error: any) {
		throw error.response ? error.response.data : error;
	}
};

export const refreshToken = async (): Promise<string> => {
	try {
		const refreshToken = getRefreshToken();
		if (!refreshToken) {
			throw new Error('No refresh token available');
		}

		const response = await axios.post<ApiResponse<{ token: string }>>(`${API_URL}/auth/refresh`, {}, {
			headers: { Authorization: `Bearer ${refreshToken}` },
		});

		if (response.data.data?.token) {
			localStorage.setItem('token', response.data.data.token);
			return response.data.data.token;
		}
		throw new Error('Failed to refresh token');
	} catch (error: any) {
		// If refresh token is invalid, logout the user
		localStorage.removeItem('token');
		localStorage.removeItem('refreshToken');
		localStorage.removeItem('user');
		throw error;
	}
};

export const logout = async (): Promise<ApiResponse<void>> => {
	try {
		const response = await axios.post<ApiResponse<void>>(
			`${API_URL}/auth/logout`,
			{},
			{
				headers: { Authorization: `Bearer ${getToken()}` },
			},
		);
		localStorage.removeItem('token');
		localStorage.removeItem('refreshToken');
		localStorage.removeItem('user');
		return response.data;
	} catch (error: any) {
		console.error('Logout error:', error);
		// Still clear local storage even if API call fails
		localStorage.removeItem('token');
		localStorage.removeItem('refreshToken');
		localStorage.removeItem('user');
		throw error.response ? error.response.data : error;
	}
};

export const getToken = (): string | null => {
	return localStorage.getItem('token');
};

export const getRefreshToken = (): string | null => {
	return localStorage.getItem('refreshToken');
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

// Setup axios interceptor to handle token refresh
axios.interceptors.response.use(
	(response) => {
		return response;
	},
	async (error: AxiosError) => {
		const originalRequest = error.config;

		// If error is not 401 or original request doesn't exist, reject
		if (!error.response || error.response.status !== 401 || !originalRequest) {
			return Promise.reject(error);
		}

		console.debug('Received 401 axios error. Checking if we need to refresh our token.');

		const data = error.response.data as ApiResponse<void>;
		if (!data.errors?.auth.filter(s => s.includes('expired token')).length) {
			console.debug('Token is not expired. Rejecting with original error.');
			return Promise.reject(error);
		}

		console.debug('Token is expired. Attempting to refresh token.');

		// Check if we're already refreshing to avoid multiple refresh requests
		if (isRefreshing) {
			console.debug('Token refresh already in progress. Waiting for it to complete.');
			// Wait for the token to be refreshed
			return new Promise<string>((resolve) => {
				subscribeTokenRefresh((token: string) => {
					// Replace the expired token and retry
					if (originalRequest.headers) {
						originalRequest.headers.Authorization = `Bearer ${token}`;
					}
					resolve(axios(originalRequest));
				});
			});
		}

		console.debug('No token refresh in progress, starting a new process...');

		// Set refreshing flag
		isRefreshing = true;

		try {
			// Try to refresh the token
			console.debug('Attempting to refresh token...');
			const newToken = await refreshToken();
			console.debug('Token refreshed successfully.');

			// Update the original request with the new token
			if (originalRequest.headers) {
				console.debug('Setting new auth header...');
				originalRequest.headers.Authorization = `Bearer ${newToken}`;
				console.debug('New auth header set.');
			}

			// Notify all subscribers that the token has been refreshed
			console.debug('Notifying subscribers of token refresh...');
			onTokenRefreshed(newToken);
			console.debug('Subscribers notified.');

			// Reset refreshing flag
			isRefreshing = false;

			// Retry the original request with the new token
			console.debug('Retrying original request with new token...');
			return axios(originalRequest);
		} catch (refreshError) {
			console.log('Error refreshing token:', refreshError);

			// Reset refreshing flag
			isRefreshing = false;

			// Clear auth data if refresh failed
			localStorage.removeItem('token');
			localStorage.removeItem('refreshToken');
			localStorage.removeItem('user');

			// Reject with the original error
			return Promise.reject(error);
		}
	},
);
