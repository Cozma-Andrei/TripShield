const Legend = () => {
	const getCrimeColor = (value: number) => {
		const red = Math.min(255, Math.floor((value / 100) * 255));
		const green = Math.min(255, Math.floor(((100 - value) / 100) * 255));
		return `rgb(${red}, ${green}, 0)`; // Generates color from green (low crime) to red (high crime)
	};

	return (
		<div
			className="legend-container"
			style={{
				position: 'absolute',
				top: '10px',
				left: '10px',
				backgroundColor: 'white',
				padding: '10px',
				borderRadius: '8px',
			}}
		>
			<h3 className="text-lg font-semibold">Crime Rate Legend</h3>
			<div className="legend" style={{ display: 'flex', flexDirection: 'row', alignItems: 'center' }}>
				<div className="legend-item" style={{ width: '40px', height: '10px', backgroundColor: getCrimeColor(0) }}></div>
				<span className="ml-2">Low Crime</span>

				<div
					className="legend-item ml-4"
					style={{ width: '40px', height: '10px', backgroundColor: getCrimeColor(50) }}
				></div>
				<span className="ml-2">Medium Crime</span>

				<div
					className="legend-item ml-4"
					style={{ width: '40px', height: '10px', backgroundColor: getCrimeColor(100) }}
				></div>
				<span className="ml-2">High Crime</span>
			</div>
		</div>
	);
};

export default Legend;
