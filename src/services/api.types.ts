import { z } from 'zod';

// User registration and authentication DTOs
export const registerUserDto = z.object({
	username: z.string().min(3, 'Username must be between 3 and 80 characters').max(80, 'Username must be between 3 and 80 characters'),
	password: z.string().min(8, 'Password must be at least 8 characters'),
	email: z.string().email('Please enter a valid email').max(120, 'Email must be less than 120 characters'),
	name: z.string().min(1, 'Name is required').max(120, 'Name must be less than 120 characters'),
	photo: z.instanceof(File).optional(),
});

export const loginDto = z.object({
	username: z.string().min(1, 'Username is required'),
	password: z.string().min(1, 'Password is required'),
});

// Profile creation and update DTO
export const createProfileDto = z.object({
	description: z.string().min(1, 'Description is required').max(255, 'Description must be less than 255 characters'),
	parish: z.string().min(1, 'Parish is required').max(100, 'Parish must be less than 100 characters'),
	biography: z.string().min(1, 'Biography is required'),
	sex: z.string().min(1, 'Sex is required').max(20, 'Sex must be less than 20 characters'),
	race: z.string().min(1, 'Race is required').max(100, 'Race must be less than 100 characters'),
	birth_year: z.coerce
		.number()
		.min(1900, `Birth year must be between 1900 and ${new Date().getFullYear() - 18}`)
		.max(new Date().getFullYear() - 18, 'You must be at least 18 years old'),
	height: z.coerce
		.number()
		.min(1, 'Height must be a positive number')
		.max(300, 'Height must be less than 300'),
	fav_cuisine: z.string().min(1, 'Favorite cuisine is required').max(100, 'Favorite cuisine must be less than 100 characters'),
	fav_colour: z.string().min(1, 'Favorite colour is required').max(50, 'Favorite colour must be less than 50 characters'),
	fav_school_subject: z.string().min(1, 'Favorite school subject is required').max(100, 'Favorite school subject must be less than 100 characters'),
	political: z.boolean().default(false),
	religious: z.boolean().default(false),
	family_oriented: z.boolean().default(false),
});

// Search parameters for profile search - updated to match backend SearchRequestSchema
export const profileSearchParamsDto = z.object({
	name: z.string().optional(),
	birth_year: z.coerce.number().optional(),
	sex: z.string().optional(),
	race: z.string().optional(),
});

// Favourite creation DTO - updated to match backend FavouriteRequestSchema
export const createFavouriteDto = z.object({
	userId: z.number().int().positive('User ID must be a positive integer'),
});

// Type exports from zod schemas
export type RegisterUserDto = z.infer<typeof registerUserDto>;
export type LoginDto = z.infer<typeof loginDto>;
export type ProfileDto = z.infer<typeof createProfileDto>;
export type ProfileSearchParamsDto = z.infer<typeof profileSearchParamsDto>;
export type CreateFavouriteDto = z.infer<typeof createFavouriteDto>;

// User interfaces
export interface User {
	id: number;
	username: string;
	name: string;
	email: string;
	photo?: string;
	date_joined: string;
}

// User info interface (minimal user information)
export interface UserInfo {
	id: number;
	name: string;
	photo?: string;
}

// Profile interfaces
export interface Profile {
	id: number;
	user_id: number;
	description: string;
	parish: string;
	biography: string;
	sex: string;
	race: string;
	birth_year: number;
	height: number;
	fav_cuisine: string;
	fav_colour: string;
	fav_school_subject: string;
	political: boolean;
	religious: boolean;
	family_oriented: boolean;
}

// Profile with user information interface
export interface ProfileWithUser extends Omit<Profile, 'user_id'> {
	user_id: number;
	user: UserInfo;
}

// Favourite interfaces
export interface Favourite {
	id: number;
	user_id: number;
	fav_user_id: number;
	created_at: string;
}

// Top favourite user interface - updated to match backend TopFavouriteSchema
export interface TopFavourite {
	user_id: number;
	name: string;
	favourite_count: number;
}

// API response interfaces
export interface ApiResponse<T> {
	success: boolean;
	message?: string;
	data?: T;
	errors?: Record<string, string[]>;
}

export interface AuthResponse {
	token: string;
	refreshToken: string;
	user: User;
}

// Search parameters interface - updated to match backend SearchRequestSchema
export interface ProfileSearchParams {
	name?: string;
	birth_year?: number;
	sex?: string;
	race?: string;
}
