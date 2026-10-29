<script>
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	const isUnauthorized = $derived(page.status === 401 || page.status === 403);

	onMount(() => {
		if (isUnauthorized) {
			const timer = setTimeout(() => {
				goto('/login');
			}, 3000);

			return () => clearTimeout(timer);
		}
	});
</script>

<div class="flex flex-1 items-center justify-center p-4">
	<div class="w-full max-w-md rounded-2xl border border-slate-800 bg-slate-900/80 p-8 text-center shadow-xl">
		<div class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-rose-500/15 text-rose-400 border border-rose-500/30">
			<svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
				<path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
			</svg>
		</div>

		<h1 class="text-2xl font-bold text-white">{page.status}</h1>
		<p class="mt-2 text-sm text-slate-300">
			{page.error?.message || 'Une erreur est survenue'}
		</p>

		{#if isUnauthorized}
			<p class="mt-4 text-xs text-amber-300 animate-pulse">
				Redirection vers la page de connexion dans 3 secondes...
			</p>
		{:else}
			<a
				href="/"
				class="mt-6 inline-flex items-center justify-center rounded-xl bg-indigo-600 px-4 py-2 text-xs font-semibold text-white transition-colors hover:bg-indigo-500"
			>
				Retour à l'accueil
			</a>
		{/if}
	</div>
</div>

