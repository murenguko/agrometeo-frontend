import { fail, redirect } from '@sveltejs/kit';
import { BASE_URL } from '$app/env/private';

/** @satisfies {import('./$types').Actions} */

export const actions ={
    default: async ({request, cookies}) => {
        const data = await request.formData();
        const username = data.get('username');
        const password = data.get('password');
        const name = data.get('name');

        //Format data as URLSearchParams because OAuth2PasswordRequestForm expects form-data
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        formData.append('name', name)


        const response = await fetch(BASE_URL + '/user', {
            method:'POST',
            headers : { 'Content-Type':'application/x-www-form-urlencoded'},
            body: formData
        });

        if (!response.ok){
            return fail(400, {error: 'Cannot register new user'});
        }

        throw redirect(303, '/login');

    }
}