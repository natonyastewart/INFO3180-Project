import type { ApiResponse, CreateFavouriteDto, Favourite, Profile, ProfileDto, ProfileSearchParams, ProfileWithUser, TopFavourite, User } from './api.types';

import { API_URL } from '@/constants';
import axios from 'axios';

// User related API calls
export const getUserById = async (userId: number) => {
	const response = await axios.get<ApiResponse<Omit<User, 'email'>>>(`${API_URL}/users/${userId}`);
	return response.data;
};

export const getUserFavorites = async () => {
	const response = await axios.get<ApiResponse<Favourite[]>>(`${API_URL}/users/favourites`);
	return response.data;
};

export const getTopFavorites = async (threshold = 20) => {
	const response = await axios.get<ApiResponse<TopFavourite[]>>(`${API_URL}/users/favourites/${threshold}`);
	return response.data;
};

// Profile related API calls
export const createProfile = async (data: ProfileDto) => {
	const response = await axios.post<ApiResponse<Profile>>(`${API_URL}/profiles`, data);
	return response.data;
};

export const getProfiles = async () => {
	const response = await axios.get<ApiResponse<Profile[]>>(`${API_URL}/profiles`);
	return response.data;
};

export const getProfileById = async (profileId: number) => {
	const response = await axios.get<ApiResponse<Profile>>(`${API_URL}/profiles/${profileId}`);
	return response.data;
};

export const addToFavorites = async (data: CreateFavouriteDto) => {
	const response = await axios.post<ApiResponse<Favourite>>(`${API_URL}/profiles/favourite`, data);
	return response.data;
};

export const getProfileMatches = async (profileId: number) => {
	const response = await axios.get<ApiResponse<ProfileWithUser[]>>(`${API_URL}/profiles/matches/${profileId}`);
	return response.data;
};

// Search profiles
export const searchProfiles = async (searchParams?: ProfileSearchParams) => {
	const response = await axios.get<ApiResponse<Profile[]>>(`${API_URL}/search`, {
		params: searchParams,
	});
	return response.data;
};
