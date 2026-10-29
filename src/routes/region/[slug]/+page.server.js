import { error, redirect } from '@sveltejs/kit';
import { BASE_URL } from '$app/env/private';

const base_url = BASE_URL;

export const load = async ({ cookies, fetch, params }) => {
	const accessToken = cookies.get('access_token');

	if (!accessToken) {
		throw redirect(307, '/login');
	}

	const location = params.slug;
	const url = base_url + '/' + location;

	const res = await fetch(url, {
		headers: {
			Authorization: `Bearer ${accessToken}`
		}
	});

	if (!res.ok) {
		if (res.status === 401 || res.status === 403) {
			cookies.delete('access_token', { path: '/' });
		}
		throw error(res.status, 'Unauthorized request');
	}

	const data = await res.json();
	return data;
};
