import type { Emitter } from 'mitt';
import mitt from 'mitt';

// Define event types
type Events = {
	'flash': { message: string; type?: string };
	'auth:update': void;
	[key: string]: any;
};

// Create a single event emitter instance to be shared across the app
const emitter: Emitter<Events> = mitt<Events>();

export default emitter;
