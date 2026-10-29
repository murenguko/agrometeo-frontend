<script>
	import { Map, TileLayer, Marker, Popup } from 'sveaflet';

	let regions = [
		{
			id: 1,
			locationName: 'Gitega',
			locationDenomination: 'gitega',
			subtitle: 'Hautes terres centrales',
			lat: -3.42708,
			long: 29.92463
		},
		{
			id: 2,
			locationName: 'Karusi',
			locationDenomination: 'karusi',
			subtitle: 'Bassin de la Ruvubu',
			lat: -3.10139,
			long: 30.16278
		},
		{
			id: 3,
			locationName: 'Bujumbura Mairie',
			locationDenomination: 'bujumbura',
			subtitle: 'Plaine de l’Imbo & Littoral',
			lat: -3.38193,
			long: 29.36142
		},
		{
			id: 4,
			locationName: 'Rutana',
			locationDenomination: 'rutana',
			subtitle: 'Sud-Est & Kumoso',
			lat: -3.9279,
			long: 29.992
		},
		{
			id: 5,
			locationName: 'Bujumbura Rural (Imbo)',
			locationDenomination: 'buja_rural_imbo',
			subtitle: 'Plaine de l’Imbo',
			lat: -3.45,
			long: 29.32
		},
		{
			id: 6,
			locationName: 'Bujumbura Rural (Mumirwa)',
			locationDenomination: 'buja_rural_mumirwa',
			subtitle: 'Contreforts de Mumirwa',
			lat: -3.5122,
			long: 29.3715
		}
	];
</script>

<div class="w-full h-[540px] lg:h-[620px] rounded-2xl overflow-hidden border border-slate-800 shadow-2xl relative z-0">
	<Map
		options={{
			center: [-3.42, 29.85],
			zoom: 8.5
		}}
	>
		<TileLayer url={'https://tile.openstreetmap.org/{z}/{x}/{y}.png'} />

		{#each regions as region (region.id)}
			<Marker latLng={[region.lat, region.long]} options={{ title: region.locationName }}>
				<Popup>
					<div class="p-1 min-w-[160px]">
						<div class="font-bold text-slate-900 text-sm">{region.locationName}</div>
						<div class="text-xs text-slate-500 mb-2">{region.subtitle}</div>
						<a
							href="/region/{region.locationDenomination}"
							class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-600 text-white! text-xs font-semibold hover:bg-indigo-500 transition-colors no-underline"
						>
							<span>Voir météo & conseils</span>
							<span>→</span>
						</a>
					</div>
				</Popup>
			</Marker>
		{/each}
	</Map>
</div>
