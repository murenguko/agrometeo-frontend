import { fail, redirect } from '@sveltejs/kit';
import { BASE_URL } from '$app/env/private';

/** @satisfies {import('./$types').Actions} */
export const actions = {
	default: async ({ request }) => {
		const data = await request.formData();
		const username = data.get('username');
		const password = data.get('password');
		const name = data.get('name');

		const response = await fetch(BASE_URL + '/user', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ username, name, password })
		});

		if (!response.ok) {
			const result = await response.json().catch(() => null);
			const errorMessage =
				typeof result?.detail === 'string'
					? result.detail
					: 'Impossible de créer le compte. Veuillez vérifier vos informations.';

			return fail(response.status, {
				error: errorMessage
			});
		}

		throw redirect(303, '/login?registered=true');
	}
};
