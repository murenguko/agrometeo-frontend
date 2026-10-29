<script>
	import { enhance } from '$app/forms';

	let { form } = $props();
	let loading = $state(false);
	let showPassword = $state(false);
</script>

<div class="relative flex-1 flex items-center justify-center min-h-screen px-4 py-12 overflow-hidden bg-slate-950">
	<!-- Ambient decorative glow -->
	<div class="pointer-events-none absolute -top-40 -right-40 w-96 h-96 rounded-full bg-indigo-600/15 blur-3xl"></div>
	<div class="pointer-events-none absolute -bottom-40 -left-40 w-96 h-96 rounded-full bg-emerald-500/10 blur-3xl"></div>

	<div class="relative w-full max-w-md">
		<!-- Brand Header -->
		<div class="flex flex-col items-center mb-8 text-center">
			<div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo-500 to-cyan-400 flex items-center justify-center shadow-xl shadow-indigo-500/25 mb-4">
				<svg class="w-7 h-7 text-slate-950" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.2">
					<path stroke-linecap="round" stroke-linejoin="round" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z" />
				</svg>
			</div>
			<h1 class="text-2xl font-bold tracking-tight text-white">Créer un compte AgroMétéo</h1>
			<p class="text-sm text-slate-400 mt-1">
				Inscrivez-vous pour accéder aux données météo et alertes agro-climatiques
			</p>
		</div>

		<!-- Sign Up Card -->
		<div class="bg-slate-900/80 backdrop-blur-xl border border-slate-800/90 rounded-2xl p-6 sm:p-8 shadow-2xl">
			{#if form?.error}
				<div class="mb-5 flex items-start gap-3 rounded-xl bg-rose-500/10 border border-rose-500/30 px-4 py-3 text-xs text-rose-300">
					<svg class="w-4 h-4 text-rose-400 shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
					</svg>
					<span>{form.error}</span>
				</div>
			{/if}

			<form
				id="signupForm"
				method="POST"
				class="space-y-5"
				use:enhance={() => {
					loading = true;
					return async ({ update }) => {
						loading = false;
						await update();
					};
				}}
			>
				<!-- Full Name Input -->
				<div>
					<label for="name" class="block text-xs font-medium text-slate-300 mb-1.5">
						Nom complet
					</label>
					<div class="relative">
						<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3.5 text-slate-500">
							<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
								<path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
							</svg>
						</div>
						<input
							name="name"
							type="text"
							id="name"
							required
							autocomplete="name"
							placeholder="Jean Ndayishimiye"
							class="w-full pl-10 pr-3.5 py-2.5 bg-slate-950/90 border border-slate-800 rounded-xl text-sm text-white placeholder-slate-500 transition-colors focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20"
						/>
					</div>
				</div>

				<!-- Email / Username Input -->
				<div>
					<label for="email" class="block text-xs font-medium text-slate-300 mb-1.5">
						Adresse e-mail
					</label>
					<div class="relative">
						<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3.5 text-slate-500">
							<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
								<path stroke-linecap="round" stroke-linejoin="round" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
							</svg>
						</div>
						<input
							name="username"
							type="email"
							id="email"
							required
							autocomplete="email"
							placeholder="nom@exemple.com"
							class="w-full pl-10 pr-3.5 py-2.5 bg-slate-950/90 border border-slate-800 rounded-xl text-sm text-white placeholder-slate-500 transition-colors focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20"
						/>
					</div>
				</div>

				<!-- Password Input -->
				<div>
					<label for="password" class="block text-xs font-medium text-slate-300 mb-1.5">
						Mot de passe
					</label>
					<div class="relative">
						<div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3.5 text-slate-500">
							<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
								<path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
							</svg>
						</div>
						<input
							name="password"
							type={showPassword ? 'text' : 'password'}
							id="password"
							required
							minlength="6"
							autocomplete="new-password"
							placeholder="Minimum 6 caractères"
							class="w-full pl-10 pr-10 py-2.5 bg-slate-950/90 border border-slate-800 rounded-xl text-sm text-white placeholder-slate-500 transition-colors focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20"
						/>
						<button
							type="button"
							onclick={() => (showPassword = !showPassword)}
							class="absolute inset-y-0 right-0 flex items-center pr-3 text-slate-500 hover:text-slate-300 transition-colors"
							aria-label="Afficher ou masquer le mot de passe"
						>
							{#if showPassword}
								<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
									<path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
								</svg>
							{:else}
								<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
									<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
									<path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
								</svg>
							{/if}
						</button>
					</div>
				</div>

				<!-- Submit Button -->
				<button
					type="submit"
					disabled={loading}
					class="w-full py-2.5 px-4 bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 disabled:opacity-60 text-white font-semibold text-sm rounded-xl shadow-lg shadow-indigo-600/25 transition-all flex items-center justify-center gap-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-slate-900 cursor-pointer"
				>
					{#if loading}
						<svg class="w-4 h-4 animate-spin text-white" fill="none" viewBox="0 0 24 24">
							<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
							<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
						</svg>
						<span>Création du compte...</span>
					{:else}
						<span>S'inscrire</span>
						<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3" />
						</svg>
					{/if}
				</button>
			</form>

			<!-- Login Link -->
			<div class="mt-6 pt-5 border-t border-slate-800/80 text-center text-xs text-slate-400">
				Vous avez déjà un compte ?
				<a
					href="/login"
					class="ml-1 text-indigo-400 hover:text-indigo-300 font-semibold hover:underline focus:outline-none focus:underline"
				>
					Se connecter
				</a>
			</div>
		</div>
	</div>
</div>

