import { z } from 'zod';

export const registerUserDto = z.object({
	username: z.string(),
	password: z.string(),
	email: z.string().email(),
	name: z.string(),
});

export const loginDto = z.object({
	username: z.string(),
	password: z.string(),
});

export type RegisterUserDto = z.infer<typeof registerUserDto>;
export type LoginDto = z.infer<typeof loginDto>;

// Profile interfaces
export interface Profile {
	id: string;
	userId: string;
	name: string;
	gender: string;
	age: number;
	location: string;
	bio?: string;
	interests?: string[];
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
