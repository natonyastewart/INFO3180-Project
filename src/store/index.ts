import { InjectionKey } from 'vue';
import { createStore, Store } from 'vuex';

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

// Define injection key
export const key: InjectionKey<Store<RootState>> = Symbol();

export default createStore<RootState>({
	state: {
		user: {
			loggedIn: false,
			data: null,
		},
	},
	getters: {
		user(state): UserState {
			return state.user;
		},
	},
	mutations: {
		SET_LOGGED_IN(state, value: boolean): void {
			state.user.loggedIn = value;
		},
		SET_USER(state, data: UserData | null): void {
			state.user.data = data;
		},
	},
	actions: {
		async setAuthenticated({ commit }, value: boolean): Promise<void> {
			commit('SET_LOGGED_IN', value);
		},
		async setUser({ commit }, user: UserData | null): Promise<void> {
			commit('SET_USER', user);
		},
		async login({ commit }, user: UserData): Promise<void> {
			commit('SET_USER', user);
			commit('SET_LOGGED_IN', true);
		},
		async logout({ commit }): Promise<void> {
			commit('SET_USER', null);
			commit('SET_LOGGED_IN', false);
		},
	},
});
