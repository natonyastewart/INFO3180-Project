import { defineStore } from 'pinia';

// Define user data interface
export interface UserData {
	id?: string;
	username?: string;
	email?: string;
	name?: string;
	[key: string]: any; // For any additional properties
}

// Define user state interface
export interface UserState {
	loggedIn: boolean;
	data: UserData | null;
}

// Define root state interface
export interface RootState {
	user: UserState;
}

export const useGlobalStore = defineStore('globalStore', {
	state: () => ({
		user: {
			loggedIn: false,
			data: null,
		},
	} as RootState),
	getters: {
		user(state): UserState {
			return state.user;
		},
	},
	actions: {
		async setAuthenticated(value: boolean): Promise<void> {
			this.user.loggedIn = value;
		},
		async setUser(user: UserData | null): Promise<void> {
			this.user.data = user;
		},
		async login(user: UserData): Promise<void> {
			this.user.data = user;
			this.user.loggedIn = true;
		},
		async logout(): Promise<void> {
			this.user.data = null;
			this.user.loggedIn = false;
		},
	},
});
