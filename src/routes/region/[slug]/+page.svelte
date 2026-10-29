<script>
	import { Plot, Pointer, Line, AreaY, RuleX, RuleY, Dot, Text } from 'svelteplot';

	let { data } = $props();

	const metricConfigs = [
		{
			id: 'Temperature 2m',
			key: 'temperature_2m',
			label: 'Température (2 m)',
			shortLabel: 'Température',
			unit: '°C',
			color: '#f59e0b'
		},
		{
			id: 'Precipitation',
			key: 'precipitation',
			label: 'Précipitations',
			shortLabel: 'Pluie',
			unit: 'mm',
			color: '#38bdf8'
		},
		{
			id: 'Precipitation probability',
			key: 'precipitation_probability',
			label: 'Probabilité de pluie',
			shortLabel: 'Prob. pluie',
			unit: '%',
			color: '#818cf8'
		},
		{
			id: 'Wind Speed 10m',
			key: 'wind_speed_10m',
			label: 'Vitesse du vent (10 m)',
			shortLabel: 'Vent',
			unit: 'km/h',
			color: '#34d399'
		}
	];

	let metric = $state('Temperature 2m');
	let statusFilter = $state('all'); // 'all' | 'alerts' | 'sans_signal'
	let cultureFilter = $state('all');
	let selectedConseil = $state(null);

	let activeMetricConfig = $derived(metricConfigs.find((m) => m.id === metric) ?? metricConfigs[0]);

	let metricKey = $derived(metric ? metric.toLowerCase().split(' ').join('_') : 'temperature_2m');

	let metricData = $derived(
		data?.hourly_data?.[metricKey]
			? data.hourly_data[metricKey].map((val, i) => ({
					Time: new Date(data.hourly_data.date[i]),
					[metric]: Number(val)
				}))
			: []
	);

	let metricStats = $derived.by(() => {
		const raw = data?.hourly_data?.[metricKey]?.map(Number).filter((n) => !Number.isNaN(n)) ?? [];
		if (raw.length === 0) return { min: '—', max: '—', avg: '—', current: '—' };
		const min = Math.min(...raw);
		const max = Math.max(...raw);
		const avg = raw.reduce((a, b) => a + b, 0) / raw.length;
		return {
			current: raw[0]?.toFixed(1),
			min: min.toFixed(1),
			max: max.toFixed(1),
			avg: avg.toFixed(1)
		};
	});

	let conseils = $derived(Array.isArray(data?.conseils) ? data.conseils : []);

	let nombreConseilsActifs = $derived(conseils.filter((c) => c.statut !== 'sans_signal').length);

	let culturesDisponibles = $derived([...new Set(conseils.map((c) => c.culture).filter(Boolean))]);

	let filteredConseils = $derived(
		conseils.filter((c) => {
			if (statusFilter === 'alerts' && c.statut === 'sans_signal') return false;
			if (statusFilter === 'sans_signal' && c.statut !== 'sans_signal') return false;
			if (cultureFilter !== 'all' && c.culture !== cultureFilter) return false;
			return true;
		})
	);

	const locationNames = {
		gitega: 'Gitega',
		karusi: 'Karusi',
		bujumbura: 'Bujumbura Mairie',
		rutana: 'Rutana',
		buja_rural: 'Bujumbura Rural',
		buja_rural_imbo: 'Bujumbura Rural (Imbo)',
		buja_rural_mumirwa: 'Bujumbura Rural (Mumirwa)'
	};

	const cultureLabels = {
		mais: 'Maïs',
		haricot: 'Haricot',
		riz: 'Riz',
		banane: 'Banane',
		manioc: 'Manioc',
		sorgho: 'Sorgho',
		cafe: 'Café',
		the: 'Thé',
		pomme_de_terre: 'Pomme de terre'
	};

	function formatLocationName(slug) {
		if (!slug) return 'Zone';
		const lower = String(slug).toLowerCase();
		if (locationNames[lower]) return locationNames[lower];
		return String(slug)
			.replace(/_/g, ' ')
			.replace(/\b\w/g, (l) => l.toUpperCase());
	}

	function formatCulture(culture) {
		if (!culture) return 'Culture générale';
		const lower = String(culture).toLowerCase();
		if (cultureLabels[lower]) return cultureLabels[lower];
		return String(culture)
			.replace(/_/g, ' ')
			.replace(/\b\w/g, (l) => l.toUpperCase());
	}

	function formatStatut(statut) {
		if (!statut) return 'Inconnu';
		if (statut === 'sans_signal') return 'Sans signal';
		return String(statut)
			.replace(/_/g, ' ')
			.replace(/\b\w/g, (l) => l.toUpperCase());
	}

	function getStatutStyle(statut) {
		if (statut === 'sans_signal') {
			return {
				badge: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
				dot: 'bg-emerald-400',
				border: 'border-slate-800 hover:border-slate-700',
				messageBox: 'bg-slate-950/80 border-slate-800 text-slate-200'
			};
		}
		return {
			badge: 'bg-amber-500/15 text-amber-300 border-amber-500/40',
			dot: 'bg-amber-400 animate-ping',
			border: 'border-amber-500/40 hover:border-amber-500/60 shadow-lg shadow-amber-500/5',
			messageBox: 'bg-amber-500/10 border-amber-500/30 text-amber-100'
		};
	}

	function extractGauges(mesures) {
		if (!mesures || typeof mesures !== 'object') return { pairs: [], extras: [] };

		const knownPairs = [
			{
				id: 'pluie_24h',
				label: 'Pluie cumulée (24 h)',
				valKey: 'pluie_24h_mm',
				seuilKey: 'seuil_24h_mm',
				unit: 'mm'
			},
			{
				id: 'pluie_72h',
				label: 'Pluie cumulée (72 h)',
				valKey: 'pluie_72h_mm',
				seuilKey: 'seuil_72h_mm',
				unit: 'mm'
			},
			{
				id: 'rafales',
				label: 'Rafales de vent',
				valKey: 'rafales_kmh',
				seuilKey: 'seuil_rafales_kmh',
				unit: 'km/h'
			},
			{
				id: 'jours_secs',
				label: 'Jours secs consécutifs',
				valKey: 'jours_secs',
				seuilKey: 'seuil_jours_secs',
				unit: 'j'
			}
		];

		const usedKeys = new Set();
		const pairs = [];

		for (const item of knownPairs) {
			if (mesures[item.valKey] !== undefined && mesures[item.valKey] !== null) {
				usedKeys.add(item.valKey);
				usedKeys.add(item.seuilKey);
				const val = Number(mesures[item.valKey]);
				const seuil =
					mesures[item.seuilKey] !== undefined && mesures[item.seuilKey] !== null
						? Number(mesures[item.seuilKey])
						: null;
				const ratio = seuil && seuil > 0 ? (val / seuil) * 100 : 0;
				pairs.push({
					...item,
					value: val,
					seuil,
					percent: Math.min(100, Math.max(0, ratio)),
					rawPercent: Math.round(ratio)
				});
			}
		}

		const extras = Object.entries(mesures)
			.filter(([k, v]) => !usedKeys.has(k) && v !== null && v !== undefined)
			.map(([k, v]) => ({
				key: k.replace(/_/g, ' '),
				value: v
			}));

		return { pairs, extras };
	}

	function getGaugeColor(rawPercent) {
		if (rawPercent >= 100) return 'bg-rose-500';
		if (rawPercent >= 75) return 'bg-amber-400';
		return 'bg-indigo-500';
	}

	function getGaugeTextColor(rawPercent) {
		if (rawPercent >= 100) return 'text-rose-400';
		if (rawPercent >= 75) return 'text-amber-300';
		return 'text-slate-400';
	}

	function formatFullDateTime(date) {
		if (!date) return '';
		return new Intl.DateTimeFormat('fr-FR', {
			month: 'short',
			day: 'numeric',
			hour: '2-digit',
			minute: '2-digit',
			timeZone: 'UTC'
		}).format(date);
	}

	function handleKeydown(event) {
		if (event.key === 'Escape' && selectedConseil) {
			selectedConseil = null;
		}
	}
</script>

<svelte:window onkeydown={handleKeydown} />

<div class="mx-auto w-full max-w-7xl space-y-8 px-4 py-8 sm:px-6 lg:px-8">
	<!-- Top Navigation & Location Header -->
	<div class="flex flex-col gap-5">
		<div>
			<a
				href="/"
				class="inline-flex items-center gap-2 text-xs font-medium text-slate-400 transition-colors hover:text-indigo-300"
			>
				<svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
					<path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
				</svg>
				<span>Retour à la carte des régions</span>
			</a>
		</div>

		<div
			class="flex flex-col justify-between gap-6 rounded-2xl border border-slate-800/90 bg-slate-900/70 p-6 shadow-xl lg:flex-row lg:items-center"
		>
			<div class="space-y-1.5">
				<div class="flex flex-wrap items-center gap-2.5">
					<span
						class="rounded-full border border-indigo-500/30 bg-indigo-500/15 px-2.5 py-0.5 text-[11px] font-semibold tracking-wider text-indigo-300 uppercase"
					>
						Station régionale
					</span>
					{#if data.timezone}
						<span class="font-mono text-xs text-slate-400">
							Fuseau : {data.timezone}
						</span>
					{/if}
				</div>
				<h1 class="text-2xl font-bold tracking-tight text-white sm:text-3xl">
					{formatLocationName(data.location)}
				</h1>
				<p class="text-xs text-slate-400 sm:text-sm">
					Bulletin météorologique horaire et avis agro-climatiques par culture
				</p>
			</div>

			<!-- Location Coordinates & Elevation Pills -->
			<div class="grid grid-cols-2 gap-3 sm:grid-cols-3">
				<div class="rounded-xl border border-slate-800/80 bg-slate-950/80 px-4 py-3">
					<div class="text-[11px] font-medium tracking-wider text-slate-500 uppercase">
						Latitude
					</div>
					<div class="mt-0.5 font-mono text-sm font-semibold text-white sm:text-base">
						{Number(data.latitude).toFixed(4)}°
					</div>
				</div>
				<div class="rounded-xl border border-slate-800/80 bg-slate-950/80 px-4 py-3">
					<div class="text-[11px] font-medium tracking-wider text-slate-500 uppercase">
						Longitude
					</div>
					<div class="mt-0.5 font-mono text-sm font-semibold text-white sm:text-base">
						{Number(data.longitude).toFixed(4)}°
					</div>
				</div>
				<div
					class="col-span-2 rounded-xl border border-slate-800/80 bg-slate-950/80 px-4 py-3 sm:col-span-1"
				>
					<div class="text-[11px] font-medium tracking-wider text-slate-500 uppercase">
						Altitude
					</div>
					<div class="mt-0.5 font-mono text-sm font-semibold text-indigo-300 sm:text-base">
						{data.elevation} m
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Weather Forecast Chart Card -->
	<section class="space-y-6 rounded-2xl border border-slate-800/90 bg-slate-900/70 p-6 shadow-xl">
		<div class="flex flex-col justify-between gap-4 md:flex-row md:items-center">
			<div>
				<h2 class="flex items-center gap-2 text-lg font-bold text-white">
					<svg
						class="h-5 w-5 text-indigo-400"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="2"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"
						/>
					</svg>
					<span>Prévisions horaires ({activeMetricConfig.label})</span>
				</h2>
				<p class="mt-0.5 text-xs text-slate-400">
					Survolez la courbe pour inspecter les valeurs horaires exactes (UTC)
				</p>
			</div>

			<!-- Metric Selector Tabs -->
			<div
				class="flex flex-wrap items-center gap-1.5 rounded-xl border border-slate-800 bg-slate-950 p-1.5"
			>
				{#each metricConfigs as m}
					<button
						type="button"
						onclick={() => (metric = m.id)}
						class="cursor-pointer rounded-lg px-3 py-1.5 text-xs font-medium transition-all {metric ===
						m.id
							? 'bg-indigo-600 text-white shadow-sm'
							: 'text-slate-400 hover:bg-slate-900 hover:text-slate-200'}"
					>
						{m.shortLabel}
						<span class="ml-0.5 opacity-70">({m.unit})</span>
					</button>
				{/each}
			</div>
		</div>

		<!-- Summary Stats for Selected Metric -->
		<div class="grid grid-cols-2 gap-3 sm:grid-cols-4">
			<div class="rounded-xl border border-slate-800/70 bg-slate-950/70 p-3.5">
				<div class="text-[11px] text-slate-400">Valeur initiale</div>
				<div class="mt-0.5 text-lg font-bold text-white">
					{metricStats.current}
					<span class="text-xs font-normal text-slate-400">{activeMetricConfig.unit}</span>
				</div>
			</div>
			<div class="rounded-xl border border-slate-800/70 bg-slate-950/70 p-3.5">
				<div class="text-[11px] text-slate-400">Minimum prévu</div>
				<div class="mt-0.5 text-lg font-bold text-cyan-300">
					{metricStats.min}
					<span class="text-xs font-normal text-slate-400">{activeMetricConfig.unit}</span>
				</div>
			</div>
			<div class="rounded-xl border border-slate-800/70 bg-slate-950/70 p-3.5">
				<div class="text-[11px] text-slate-400">Maximum prévu</div>
				<div class="mt-0.5 text-lg font-bold text-amber-300">
					{metricStats.max}
					<span class="text-xs font-normal text-slate-400">{activeMetricConfig.unit}</span>
				</div>
			</div>
			<div class="rounded-xl border border-slate-800/70 bg-slate-950/70 p-3.5">
				<div class="text-[11px] text-slate-400">Moyenne sur la période</div>
				<div class="mt-0.5 text-lg font-bold text-indigo-300">
					{metricStats.avg}
					<span class="text-xs font-normal text-slate-400">{activeMetricConfig.unit}</span>
				</div>
			</div>
		</div>

		<!-- Plot Container -->
		<div class="overflow-x-auto rounded-xl border border-slate-800/80 bg-slate-950/90 p-4">
			<Plot
				height={320}
				x={{
					type: 'utc',
					label: 'Date (UTC)',
					tickFormat: (d) =>
						new Intl.DateTimeFormat('fr-FR', {
							month: 'short',
							day: 'numeric',
							timeZone: 'UTC'
						}).format(d)
				}}
				y={{
					grid: true,
					label: `${activeMetricConfig.label} (${activeMetricConfig.unit})`
				}}
			>
				{#if metricData.length > 0}
					<AreaY
						data={metricData}
						x="Time"
						y={metric}
						fill={activeMetricConfig.color}
						opacity={0.12}
					/>
					<Line
						data={metricData}
						x="Time"
						y={metric}
						stroke={activeMetricConfig.color}
						strokeWidth={2.2}
					/>
					<Pointer data={metricData} x="Time" y={metric} maxDistance={30}>
						{#snippet children({ data: pointerData })}
							<RuleX data={pointerData} x="Time" opacity="0.35" />
							<RuleY data={pointerData} y={metric} opacity="0.35" />
							<Dot data={pointerData} x="Time" y={metric} r={5} fill={activeMetricConfig.color} />
							<Text
								data={pointerData}
								x="Time"
								y={metric}
								text={(d) =>
									`${formatFullDateTime(d.Time)} UTC — ${d[metric]} ${activeMetricConfig.unit}`}
								lineAnchor="bottom"
								dy={-12}
								fontWeight="bold"
							/>
						{/snippet}
					</Pointer>
				{/if}
			</Plot>
		</div>
	</section>

	<!-- Agricultural Advices (Conseils) Section -->
	<section class="space-y-6">
		<div class="flex flex-col justify-between gap-4 md:flex-row md:items-end">
			<div>
				<div
					class="mb-1 inline-flex items-center gap-2 text-xs font-semibold tracking-wider text-indigo-400 uppercase"
				>
					<span>Bulletins Agro-Climatiques</span>
				</div>
				<h2 class="text-xl font-bold text-white sm:text-2xl">
					Conseils & Évaluation des Seuils ({conseils.length})
				</h2>
				<p class="mt-0.5 text-xs text-slate-400 sm:text-sm">
					Synthèse par culture et sous-zone — cliquez sur un avis pour inspecter les mesures et
					limitations
				</p>
			</div>

			<!-- Filter Controls -->
			{#if conseils.length > 0}
				<div class="flex flex-wrap items-center gap-3">
					{#if culturesDisponibles.length > 1}
						<select
							bind:value={cultureFilter}
							aria-label="Filtrer par culture"
							class="rounded-xl border border-slate-800 bg-slate-900 px-3 py-2 text-xs font-medium text-slate-200 focus:border-indigo-500 focus:outline-none"
						>
							<option value="all">Toutes les cultures ({culturesDisponibles.length})</option>
							{#each culturesDisponibles as c}
								<option value={c}>{formatCulture(c)}</option>
							{/each}
						</select>
					{/if}

					<div
						class="flex items-center rounded-xl border border-slate-800 bg-slate-900 p-1 text-xs"
					>
						<button
							type="button"
							onclick={() => (statusFilter = 'all')}
							class="cursor-pointer rounded-lg px-3 py-1.5 font-medium transition-colors {statusFilter ===
							'all'
								? 'bg-slate-800 text-white'
								: 'text-slate-400 hover:text-slate-200'}"
						>
							Tous ({conseils.length})
						</button>
						<button
							type="button"
							onclick={() => (statusFilter = 'alerts')}
							class="cursor-pointer rounded-lg px-3 py-1.5 font-medium transition-colors {statusFilter ===
							'alerts'
								? 'bg-amber-500/20 text-amber-300'
								: 'text-slate-400 hover:text-slate-200'}"
						>
							Signaux actifs ({nombreConseilsActifs})
						</button>
						<button
							type="button"
							onclick={() => (statusFilter = 'sans_signal')}
							class="cursor-pointer rounded-lg px-3 py-1.5 font-medium transition-colors {statusFilter ===
							'sans_signal'
								? 'bg-emerald-500/20 text-emerald-300'
								: 'text-slate-400 hover:text-slate-200'}"
						>
							Sans signal ({conseils.length - nombreConseilsActifs})
						</button>
					</div>
				</div>
			{/if}
		</div>

		<!-- Overall Synthesis Banner -->
		{#if nombreConseilsActifs > 0}
			<div
				class="flex items-start gap-4 rounded-2xl border border-amber-500/30 bg-amber-500/10 p-5 text-amber-200"
			>
				<div
					class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-amber-500/30 bg-amber-500/20 text-amber-300"
				>
					<svg
						class="h-5 w-5"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="2"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
						/>
					</svg>
				</div>
				<div class="space-y-1">
					<h3 class="text-sm font-bold text-amber-100">
						{nombreConseilsActifs}
						{nombreConseilsActifs > 1
							? 'avis présentent un signal actif'
							: 'avis présente un signal actif'}
					</h3>
					<p class="text-xs text-amber-200/80">
						Certains seuils expérimentaux sont approchés ou franchis dans cette zone. Consultez les
						cartes ci-dessous pour le détail des règles déclenchées.
					</p>
				</div>
			</div>
		{:else if conseils.length > 0}
			<div
				class="flex items-start gap-4 rounded-2xl border border-emerald-500/25 bg-emerald-500/10 p-5 text-emerald-200"
			>
				<div
					class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-emerald-500/30 bg-emerald-500/20 text-emerald-300"
				>
					<svg
						class="h-5 w-5"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="2"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
						/>
					</svg>
				</div>
				<div class="space-y-1">
					<h3 class="text-sm font-bold text-emerald-100">
						Aucun seuil critique franchi ({conseils.length}
						{conseils.length > 1 ? 'évaluations' : 'évaluation'})
					</h3>
					<p class="text-xs text-emerald-200/80">
						Aucun seuil expérimental n'est franchi d'après les données disponibles.
					</p>
				</div>
			</div>
		{/if}

		<!-- Advice Cards Grid -->
		{#if filteredConseils.length > 0}
			<div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
				{#each filteredConseils as conseil}
					{@const style = getStatutStyle(conseil.statut)}
					<article
						class="border bg-slate-900/75 {style.border} flex flex-col justify-between gap-5 rounded-2xl p-6 transition-all"
					>
						<div class="space-y-4">
							<!-- Card Header: Culture, Zone/Sous-zone & Status Badge -->
							<div class="flex items-start justify-between gap-4">
								<div class="space-y-1">
									<div class="flex flex-wrap items-center gap-2">
										<span
											class="rounded-lg border border-indigo-500/30 bg-indigo-500/15 px-2.5 py-1 text-xs font-bold tracking-wide text-indigo-300"
										>
											🌱 {formatCulture(conseil.culture)}
										</span>
										<span class="text-xs font-medium text-slate-300">
											Zone : <strong class="text-white">{formatLocationName(conseil.zone)}</strong>
										</span>
										{#if conseil.sous_zone}
											<span
												class="rounded-md border border-slate-700 bg-slate-800 px-2 py-0.5 text-xs text-slate-300"
											>
												Sous-zone : {conseil.sous_zone}
											</span>
										{:else}
											<span
												class="rounded-md bg-slate-800/60 px-2 py-0.5 text-[11px] text-slate-500"
											>
												Toute la zone
											</span>
										{/if}
									</div>

									<div class="flex flex-wrap items-center gap-3 pt-1 text-[11px] text-slate-400">
										{#if conseil.date_evaluation}
											<span class="inline-flex items-center gap-1">
												<svg
													class="h-3.5 w-3.5 text-slate-500"
													fill="none"
													viewBox="0 0 24 24"
													stroke="currentColor"
													stroke-width="2"
												>
													<path
														stroke-linecap="round"
														stroke-linejoin="round"
														d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
													/>
												</svg>
												Évalué : {conseil.date_evaluation}
											</span>
										{/if}
										{#if conseil.duree_validite}
											<span class="rounded bg-slate-800 px-2 py-0.5 font-medium text-slate-300">
												Validité : {conseil.duree_validite}
											</span>
										{/if}
									</div>
								</div>

								<!-- Status Pill -->
								<span
									class="inline-flex shrink-0 items-center gap-1.5 rounded-full border px-3 py-1 text-xs font-semibold {style.badge}"
								>
									<span class="h-2 w-2 rounded-full {style.dot}"></span>
									{formatStatut(conseil.statut)}
								</span>
							</div>

							<!-- Main Advice Message -->
							{#if conseil.message}
								<div class="rounded-xl border p-4 text-sm leading-relaxed {style.messageBox}">
									{conseil.message}
								</div>
							{/if}

							<!-- Triggered Rules (if any) -->
							{#if Array.isArray(conseil.regles_declenchees) && conseil.regles_declenchees.length > 0}
								<div class="space-y-2">
									<div class="text-xs font-semibold tracking-wider text-amber-300 uppercase">
										Règles déclenchées ({conseil.regles_declenchees.length})
									</div>
									<div class="flex flex-wrap gap-2">
										{#each conseil.regles_declenchees as regle}
											<span
												class="rounded-lg border border-amber-500/30 bg-amber-500/15 px-2.5 py-1 text-xs font-medium text-amber-200"
											>
												{typeof regle === 'string' ? regle : JSON.stringify(regle)}
											</span>
										{/each}
									</div>
								</div>
							{/if}
						</div>

						<!-- Footer: Data Source & Modal Trigger Button -->
						<div
							class="flex flex-col justify-between gap-3 border-t border-slate-800/80 pt-4 text-xs sm:flex-row sm:items-center"
						>
							{#if conseil.source_donnees}
								<div class="truncate text-slate-400" title={conseil.source_donnees}>
									<span class="text-slate-500">Source :</span>
									{conseil.source_donnees}
								</div>
							{:else}
								<div></div>
							{/if}

							<button
								type="button"
								onclick={() => (selectedConseil = conseil)}
								class="inline-flex shrink-0 cursor-pointer items-center justify-center gap-2 rounded-xl border border-slate-700 bg-slate-800/90 px-3.5 py-2 font-medium text-slate-200 transition-all hover:border-indigo-500 hover:bg-indigo-600 hover:text-white"
							>
								<svg
									class="h-4 w-4"
									fill="none"
									viewBox="0 0 24 24"
									stroke="currentColor"
									stroke-width="2"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
									/>
								</svg>
								<span>Mesures & limitations</span>
							</button>
						</div>
					</article>
				{/each}
			</div>
		{:else}
			<div
				class="rounded-2xl border border-slate-800 bg-slate-900/50 p-8 text-center text-sm text-slate-400"
			>
				Aucun avis ne correspond aux filtres sélectionnés.
			</div>
		{/if}
	</section>
</div>

<!-- Modal for Mesures Utilisées & Limitations -->
{#if selectedConseil}
	{@const modalStyle = getStatutStyle(selectedConseil.statut)}
	{@const modalGauges = extractGauges(selectedConseil.mesures_utilisees)}
	<div
		class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 p-4 backdrop-blur-sm sm:p-6"
		role="dialog"
		aria-modal="true"
		aria-labelledby="modal-title"
		tabindex="-1"
		onclick={(e) => {
			if (e.target === e.currentTarget) selectedConseil = null;
		}}
	>
		<div
			class="flex max-h-[90vh] w-full max-w-2xl flex-col overflow-hidden rounded-2xl border border-slate-800 bg-slate-900 shadow-2xl"
		>
			<!-- Modal Header -->
			<div
				class="flex items-start justify-between gap-4 border-b border-slate-800 bg-slate-950/50 px-6 py-5"
			>
				<div class="space-y-1.5">
					<div class="flex flex-wrap items-center gap-2">
						<span
							class="rounded-lg border border-indigo-500/30 bg-indigo-500/15 px-2.5 py-1 text-xs font-bold text-indigo-300"
						>
							🌱 {formatCulture(selectedConseil.culture)}
						</span>
						<span
							class="inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-semibold {modalStyle.badge}"
						>
							<span class="h-1.5 w-1.5 rounded-full {modalStyle.dot}"></span>
							{formatStatut(selectedConseil.statut)}
						</span>
					</div>
					<h3 id="modal-title" class="text-lg font-bold text-white">
						Détails des mesures et limitations — {formatLocationName(selectedConseil.zone)}
						{#if selectedConseil.sous_zone}
							<span class="text-sm font-normal text-slate-400">({selectedConseil.sous_zone})</span>
						{/if}
					</h3>
					{#if selectedConseil.date_evaluation}
						<p class="text-xs text-slate-400">
							Évaluation : {selectedConseil.date_evaluation}
							{#if selectedConseil.duree_validite}
								• Validité : {selectedConseil.duree_validite}
							{/if}
						</p>
					{/if}
				</div>

				<button
					type="button"
					onclick={() => (selectedConseil = null)}
					aria-label="Fermer la fenêtre"
					class="cursor-pointer rounded-xl bg-slate-800/80 p-2 text-slate-400 transition-colors hover:bg-slate-800 hover:text-white"
				>
					<svg
						class="h-5 w-5"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="2"
					>
						<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
					</svg>
				</button>
			</div>

			<!-- Modal Body -->
			<div class="space-y-6 overflow-y-auto p-6">
				<!-- Measurements vs Thresholds (mesures_utilisees) -->
				<div class="space-y-3">
					<h4
						class="flex items-center gap-2 text-xs font-semibold tracking-wider text-indigo-400 uppercase"
					>
						<svg
							class="h-4 w-4"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
							/>
						</svg>
						<span>Mesures utilisées & Seuils de référence</span>
					</h4>

					{#if modalGauges.pairs.length > 0 || modalGauges.extras.length > 0}
						{#if modalGauges.pairs.length > 0}
							<div class="grid grid-cols-1 gap-3 sm:grid-cols-2">
								{#each modalGauges.pairs as g}
									<div class="space-y-2 rounded-xl border border-slate-800 bg-slate-950 p-3.5">
										<div class="flex items-center justify-between text-xs">
											<span class="font-medium text-slate-300">{g.label}</span>
											<span class="font-mono text-[11px] {getGaugeTextColor(g.rawPercent)}">
												{g.rawPercent}% du seuil
											</span>
										</div>

										<div class="flex items-baseline justify-between">
											<span class="font-mono text-lg font-bold text-white">
												{g.value} <span class="text-xs font-normal text-slate-400">{g.unit}</span>
											</span>
											{#if g.seuil !== null}
												<span class="font-mono text-xs text-slate-500">
													Seuil : {g.seuil}
													{g.unit}
												</span>
											{/if}
										</div>

										{#if g.seuil !== null}
											<div class="h-2 w-full overflow-hidden rounded-full bg-slate-800">
												<div
													class="h-full rounded-full transition-all duration-500 {getGaugeColor(
														g.rawPercent
													)}"
													style="width: {g.percent}%"
												></div>
											</div>
										{/if}
									</div>
								{/each}
							</div>
						{/if}

						{#if modalGauges.extras.length > 0}
							<div class="flex flex-wrap gap-2 pt-1">
								{#each modalGauges.extras as extra}
									<div class="rounded-lg border border-slate-800 bg-slate-950 px-3 py-1.5 text-xs">
										<span class="text-slate-400 capitalize">{extra.key} : </span>
										<span class="font-mono font-semibold text-slate-200">{extra.value}</span>
									</div>
								{/each}
							</div>
						{/if}
					{:else}
						<p class="text-xs text-slate-500 italic">
							Aucune mesure détaillée disponible pour cet avis.
						</p>
					{/if}
				</div>

				<!-- Limitations -->
				<div class="space-y-3">
					<h4
						class="flex items-center gap-2 text-xs font-semibold tracking-wider text-amber-400 uppercase"
					>
						<svg
							class="h-4 w-4"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
							/>
						</svg>
						<span>Précautions & limitations méthodologiques</span>
					</h4>

					{#if Array.isArray(selectedConseil.limitations) && selectedConseil.limitations.length > 0}
						<ul
							class="space-y-2.5 rounded-xl border border-slate-800 bg-slate-950 p-4 text-xs leading-relaxed text-slate-300"
						>
							{#each selectedConseil.limitations as lim}
								<li class="flex items-start gap-2.5">
									<span class="mt-1.5 h-1.5 w-1.5 shrink-0 rounded-full bg-indigo-400"></span>
									<span>{lim}</span>
								</li>
							{/each}
						</ul>
					{:else}
						<p class="text-xs text-slate-500 italic">Aucune limitation particulière mentionnée.</p>
					{/if}
				</div>

				{#if selectedConseil.source_donnees}
					<div
						class="flex items-center justify-between border-t border-slate-800/80 pt-3 text-xs text-slate-400"
					>
						<span class="font-medium text-slate-500">Source des données :</span>
						<span class="text-slate-300">{selectedConseil.source_donnees}</span>
					</div>
				{/if}
			</div>

			<!-- Modal Footer -->
			<div class="flex justify-end border-t border-slate-800 bg-slate-950/60 px-6 py-4">
				<button
					type="button"
					onclick={() => (selectedConseil = null)}
					class="cursor-pointer rounded-xl bg-slate-800 px-4 py-2 text-xs font-semibold text-white transition-colors hover:bg-slate-700"
				>
					Fermer
				</button>
			</div>
		</div>
	</div>
{/if}
