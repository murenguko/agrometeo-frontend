import { redirect } from '@sveltejs/kit';

export const ssr = false;

/** @satisfies {import('./$types').Actions} */
export const actions = {
	logout: async ({ cookies }) => {
		cookies.delete('access_token', { path: '/' });
		throw redirect(303, '/login');
	}
};
