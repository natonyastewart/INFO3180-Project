import { z } from 'zod';

export const registerUserDto = z.object({
	username: z.string().min(1, 'Username is required'),
	password: z.string().min(6, 'Password must be at least 6 characters'),
	email: z.string().email('Please enter a valid email'),
	name: z.string().min(1, 'Name is required'),
});

export const loginDto = z.object({
	username: z.string().min(1, 'Username is required'),
	password: z.string().min(1, 'Password is required'),
});

export const createProfileDto = z.object({
	name: z.string().min(1, 'Name is required'),
	description: z.string().min(1, 'Description is required'),
	parish: z.string().min(1, 'Parish is required'),
	biography: z.string().optional(),
	sex: z.string().min(1, 'Sex is required'),
	race: z.string().min(1, 'Race is required'),
	birth_year: z.coerce.number().min(1900, 'Birth year must be after 1900').max(new Date().getFullYear(), 'Birth year cannot be in the future'),
	height: z.coerce.number().min(1, 'Height must be greater than 0'),
	fav_cuisine: z.string().optional(),
	fav_colour: z.string().optional(),
	fav_school_subject: z.string().optional(),
	political: z.boolean().optional().default(false),
	religious: z.boolean().optional().default(false),
	family_oriented: z.boolean().optional().default(false),
});

export type RegisterUserDto = z.infer<typeof registerUserDto>;
export type LoginDto = z.infer<typeof loginDto>;
export type ProfileDto = z.infer<typeof createProfileDto>;

// Profile interfaces
export interface Profile {
	id: string;
	userId: string;
	name: string;

	description: string;
	parish: string;
	biography: string;
	sex: string;
	race: string;
	birthYear: number;
	height: number;
	favCuisine: string;
	favColour: string;
	favSchoolSubject: string;
	political: boolean;
	religious: boolean;
	familyOriented: boolean;

	photo?: string;
	createdAt?: string;
	updatedAt?: string;
}

export interface ProfileSearchParams {
	gender?: string;
	minAge?: number;
	maxAge?: number;
	location?: string;
	interests?: string[];
	limit?: number;
	offset?: number;
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
	user: {
		id: string;
		username: string;
		email: string;
		name: string;
	};
}
