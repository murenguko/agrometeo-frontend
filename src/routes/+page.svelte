<script>
	import Leaflet from '../lib/components/Leaflet.svelte';

	const regions = [
		{
			name: 'Gitega',
			slug: 'gitega',
			zone: 'Plateau central',
			coords: '-3.43°, 29.92°'
		},
		{
			name: 'Karusi',
			slug: 'karusi',
			zone: 'Centre-Est (Ruvubu)',
			coords: '-3.10°, 30.16°'
		},
		{
			name: 'Bujumbura Mairie',
			slug: 'bujumbura',
			zone: 'Plaine de l’Imbo',
			coords: '-3.38°, 29.36°'
		},
		{
			name: 'Rutana',
			slug: 'rutana',
			zone: 'Sud-Est',
			coords: '-3.93°, 29.99°'
		},
		{
			name: 'Bujumbura Rural',
			slug: 'buja_rural',
			zone: 'Mumirwa & Imbo',
			coords: '-3.51°, 29.37°',
			subRegions: [
				{ name: 'Imbo', slug: 'buja_rural_imbo' },
				{ name: 'Mumirwa', slug: 'buja_rural_mumirwa' }
			]
		}
	];
</script>

<div class="max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
	<div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
		<div>
			<span class="inline-flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wider text-indigo-400 mb-2">
				<span class="w-2 h-2 rounded-full bg-indigo-400 animate-pulse"></span>
				Surveillance Agro-Météorologique
			</span>
			<h1 class="text-2xl sm:text-3xl font-bold text-white tracking-tight">
				Sélectionnez une zone d'observation
			</h1>
			<p class="text-sm text-slate-400 mt-1">
				Cliquez sur un marqueur de la carte ou choisissez directement une province pour consulter les prévisions horaires et les avis agricoles.
			</p>
		</div>
	</div>

	<div class="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start">
		<!-- Quick Region List -->
		<div class="lg:col-span-1 space-y-3">
			<div class="text-xs font-semibold uppercase tracking-wider text-slate-400 px-1">
				Zones couvertes ({regions.length})
			</div>
			{#each regions as region}
				{#if region.subRegions}
					<div
						class="group block p-4 rounded-xl bg-slate-900/70 hover:bg-slate-900 border border-slate-800/80 hover:border-indigo-500/50 transition-all shadow-sm"
					>
						<div class="flex items-center justify-between">
							<div>
								<h2 class="text-sm font-semibold text-white group-hover:text-indigo-300 transition-colors">
									{region.name}
								</h2>
								<p class="text-xs text-slate-400 mt-0.5">{region.zone}</p>
							</div>
							<div class="w-8 h-8 rounded-lg bg-slate-800/80 group-hover:bg-indigo-500/20 flex items-center justify-center text-slate-400 group-hover:text-indigo-300 transition-colors">
								<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
								</svg>
							</div>
						</div>
						<div class="mt-2.5 flex items-center gap-1.5 text-[11px] font-mono text-slate-500">
							<svg class="w-3.5 h-3.5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
								<path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
							</svg>
							<span>{region.coords}</span>
						</div>
						<div class="hidden group-hover:grid grid-cols-2 gap-2 mt-3 pt-3 border-t border-slate-800">
							{#each region.subRegions as sub}
								<a
									href="/region/{sub.slug}"
									class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-indigo-600 text-xs font-medium text-slate-200 hover:text-white text-center transition-colors"
								>
									{sub.name}
								</a>
							{/each}
						</div>
					</div>
				{:else}
					<a
						href="/region/{region.slug}"
						class="group block p-4 rounded-xl bg-slate-900/70 hover:bg-slate-900 border border-slate-800/80 hover:border-indigo-500/50 transition-all shadow-sm"
					>
						<div class="flex items-center justify-between">
							<div>
								<h2 class="text-sm font-semibold text-white group-hover:text-indigo-300 transition-colors">
									{region.name}
								</h2>
								<p class="text-xs text-slate-400 mt-0.5">{region.zone}</p>
							</div>
							<div class="w-8 h-8 rounded-lg bg-slate-800/80 group-hover:bg-indigo-500/20 flex items-center justify-center text-slate-400 group-hover:text-indigo-300 transition-colors">
								<svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7" />
								</svg>
							</div>
						</div>
						<div class="mt-2.5 flex items-center gap-1.5 text-[11px] font-mono text-slate-500">
							<svg class="w-3.5 h-3.5 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
								<path stroke-linecap="round" stroke-linejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
							</svg>
							<span>{region.coords}</span>
						</div>
					</a>
				{/if}
			{/each}
		</div>

		<!-- Interactive Leaflet Map -->
		<div class="lg:col-span-3">
			<Leaflet />
		</div>
	</div>
</div>
