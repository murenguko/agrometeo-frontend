<script>
	import './layout.css';
	import favicon from '#lib/assets/favicon.svg';
	import { page } from '$app/state';
	import { enhance } from '$app/forms';

	let { children } = $props();

	const isAuthRoute = $derived(page.url.pathname === '/login' || page.url.pathname === '/signup');
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>AgroMétéo Burundi</title>
</svelte:head>

<div
	class="flex min-h-screen flex-col bg-slate-950 text-slate-100 selection:bg-indigo-500/30 selection:text-indigo-200"
>
	{#if !isAuthRoute}
		<header class="sticky top-0 z-50 border-b border-slate-800/80 bg-slate-950/85 backdrop-blur-md">
			<div
				class="mx-auto flex h-16 max-w-7xl items-center justify-between gap-4 px-4 sm:px-6 lg:px-8"
			>
				<a href="/" class="group flex items-center gap-3">
					<div
						class="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-400 shadow-lg shadow-indigo-500/20 transition-transform group-hover:scale-105"
					>
						<svg
							class="h-5 w-5 text-slate-950"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2.2"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"
							/>
						</svg>
					</div>
					<div>
						<span class="text-base font-bold tracking-tight text-white">AgroMétéo</span>
						<span
							class="ml-1.5 hidden rounded-full border border-indigo-500/20 bg-indigo-500/10 px-2 py-0.5 text-xs font-medium text-indigo-300 sm:inline-block"
						>
							Burundi
						</span>
					</div>
				</a>

				<nav class="flex items-center gap-2 py-1">
					<a
						href="/"
						class="rounded-lg px-3 py-1.5 text-xs font-medium whitespace-nowrap transition-colors {page
							.url.pathname === '/'
							? 'bg-indigo-600 text-white shadow-sm shadow-indigo-500/30'
							: 'text-slate-400 hover:bg-slate-900 hover:text-slate-200'}"
					>
						Carte interactive
					</a>
					<form method="POST" action="/?/logout" use:enhance>
						<button
							type="submit"
							class="cursor-pointer rounded-lg px-3 py-1.5 text-xs font-medium whitespace-nowrap text-slate-400 transition-colors hover:bg-rose-500/10 hover:text-rose-300"
						>
							Déconnexion
						</button>
					</form>
				</nav>
			</div>
		</header>
	{/if}

	<main class="flex flex-1 flex-col">
		{@render children()}
	</main>
</div>
