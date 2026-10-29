import { fail, redirect } from '@sveltejs/kit';
import { BASE_URL } from '$app/env/private';

/** @satisfies {import('./$types').Actions} */

export const actions ={
    default: async ({request, cookies}) => {
        const data = await request.formData();
        const username = data.get('username');
        const password = data.get('password');

        //Format data as URLSearchParams because OAuth2PasswordRequestForm expects form-data
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);


        const response = await fetch(BASE_URL + '/token', {
            method:'POST',
            headers : { 'Content-Type':'application/x-www-form-urlencoded'},
            body: formData
        });

        if (!response.ok){
            return fail(400, {error: 'Incorrect username or password'});
        }

        const tokenData = await response.json();
        const accessToken = tokenData.access_token;

        cookies.set('access_token',accessToken, {
            path:'/',
            httpOnly: true,
            secure: false, //set to true in production
            sameSite: 'strict',
            maxAge: 60 * 60
        });

        throw redirect(303, '/');

    }
}