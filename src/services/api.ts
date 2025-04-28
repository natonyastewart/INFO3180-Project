import axios from 'axios';

import { ApiResponse, Profile, ProfileSearchParams } from './api.types';
import { API_URL } from '@/constants';

// User related API calls
export const getUserById = async (userId: string): Promise<ApiResponse<any>> => {
	const response = await axios.get(`${API_URL}/users/${userId}`);
	return response.data;
};

export const getUserFavorites = async (userId: string): Promise<ApiResponse<Profile[]>> => {
	const response = await axios.get(`${API_URL}/users/${userId}/favourites`);
	return response.data;
};

export const getTopFavorites = async (count = 20): Promise<ApiResponse<Profile[]>> => {
	const response = await axios.get(`${API_URL}/users/favourties/${count}`);
	return response.data;
};

// Profile related API calls
export const getAllProfiles = async (): Promise<ApiResponse<Profile[]>> => {
	const response = await axios.get(`${API_URL}/profiles`);
	return response.data;
};

export const getProfileById = async (profileId: string): Promise<ApiResponse<Profile>> => {
	const response = await axios.get(`${API_URL}/profiles/${profileId}`);
	return response.data;
};

export const createProfile = async (profileData: Partial<Profile>): Promise<ApiResponse<Profile>> => {
	const response = await axios.post(`${API_URL}/profiles`, profileData);
	return response.data;
};

export const addToFavorites = async (userId: string): Promise<ApiResponse<any>> => {
	const response = await axios.post(`${API_URL}/profiles/${userId}/favourite`);
	return response.data;
};

export const getProfileMatches = async (profileId: string): Promise<ApiResponse<Profile[]>> => {
	const response = await axios.get(`${API_URL}/profiles/matches/${profileId}`);
	return response.data;
};

// Search profiles
export const searchProfiles = async (searchParams: ProfileSearchParams): Promise<ApiResponse<Profile[]>> => {
	const response = await axios.get(`${API_URL}/search`, {
		params: searchParams,
	});
	return response.data;
};
