import { redirect } from '@sveltejs/kit';

/** @type {import('./$types').LayoutServerLoad} */
export const load = async ({ cookies, url }) => {
	const accessToken = cookies.get('access_token');
	const publicRoutes = ['/login', '/signup'];

	if (!accessToken && !publicRoutes.includes(url.pathname)) {
		throw redirect(303, '/login');
	}

	return {
		isAuthenticated: Boolean(accessToken)
	};
};
