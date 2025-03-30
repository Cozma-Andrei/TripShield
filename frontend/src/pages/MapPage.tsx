import Map from "../custom-components/Map";

function MapPage() {
	return (
		<div className="w-full h-screen flex items-center justify-center">
			{/* 80% height and width of screen, centered */}
			<div className="w-full h-full overflow-hidden rounded-xl shadow border">
				<Map />
			</div>
		</div>
	);
}

export default MapPage;
