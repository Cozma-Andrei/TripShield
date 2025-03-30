function LandingPage() {
	return (
		<div className="space-y-24">

			{/* Hero Section */}
			<section className="bg-green-100 py-20 px-6 rounded-xl shadow-md">
				<div className="max-w-4xl mx-auto text-center">
					<h1 className="text-5xl font-extrabold text-green-700 mb-6">Welcome to TripShield</h1>
					<p className="text-lg text-green-900 mb-8">
						Plan your travels smarter. Check crime rates, compare news sentiment, and make confident choices wherever you go.
					</p>
					<a
						href="/map"
						className="inline-block bg-green-600 text-white text-lg px-8 py-4 rounded-xl shadow-lg hover:bg-green-700 transition"
					>
						Explore the Safety Map
					</a>
				</div>
			</section>

			{/* Features */}
			<section className="max-w-6xl mx-auto px-6">
				<h2 className="text-3xl font-bold text-center text-green-800 mb-12">What TripShield Offers</h2>
				<div className="grid md:grid-cols-3 gap-10">
					<div className="bg-white p-6 rounded-xl shadow-md text-center hover:shadow-lg transition">
						<h3 className="text-xl font-semibold text-green-700 mb-2">City-Level Crime Stats</h3>
						<p className="text-gray-600">
							Get accurate, up-to-date crime and safety indexes for 400+ cities worldwide.
						</p>
					</div>
					<div className="bg-white p-6 rounded-xl shadow-md text-center hover:shadow-lg transition">
						<h3 className="text-xl font-semibold text-green-700 mb-2">Country Averages</h3>
						<p className="text-gray-600">
							Compare safety levels across countries using aggregated data from multiple cities.
						</p>
					</div>
					<div className="bg-white p-6 rounded-xl shadow-md text-center hover:shadow-lg transition">
						<h3 className="text-xl font-semibold text-green-700 mb-2">Clean & Interactive Map</h3>
						<p className="text-gray-600">
							Navigate a beautiful, interactive map to explore safe and unsafe zones before your next trip.
						</p>
					</div>
				</div>
			</section>

			{/* Call to Action */}
			<section className="bg-green-50 py-16 text-center rounded-xl shadow-inner mx-6">
				<h2 className="text-3xl font-bold text-green-700 mb-4">Ready to travel with confidence?</h2>
				<p className="text-gray-700 mb-6">Dive into our safety data and map your journey with peace of mind.</p>
				<a
					href="/map"
					className="inline-block bg-green-600 text-white px-8 py-4 text-lg rounded-xl hover:bg-green-700 transition"
				>
					Launch Map
				</a>
			</section>

		</div>
	);
}

export default LandingPage;
