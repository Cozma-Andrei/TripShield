import Map from "../custom-components/Map";

function MapPage() {
	return (
		<div className="w-full h-screen overflow-hidden flex flex-col">
			<div className="flex-1 overflow-hidden">
				<Map />
			</div>
		</div>
	);
}

export default MapPage;
