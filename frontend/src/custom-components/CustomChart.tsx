import * as React from 'react';
import { Bar, BarChart, CartesianGrid, XAxis } from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent } from '../components/ui/chart';

const chartConfig = {
	views: {
		label: 'Sentiment',
	},
	sentiment: {
		label: 'Sentiment',
		color: 'hsl(var(--chart-1))',
	},
} satisfies ChartConfig;

const CustomChart = ({ sentimentData }: { sentimentData: Record<string, string> | null }) => {
	// Provide a fallback for null or undefined sentimentData
	const chartData = sentimentData
		? Object.entries(sentimentData).map(([date, sentiment]) => ({
				date,
				sentiment: parseFloat(sentiment), // Convert sentiment value to a number
		  }))
		: []; // Default to an empty array if sentimentData is null or undefined

	// Calculate the total sentiment
	let total = chartData.reduce(
		(acc, { sentiment }) => {
			acc.sentiment += sentiment;
			return acc;
		},
		{ sentiment: 0 }
	);

	return (
		<Card className="mb-4">
			<CardHeader className="flex flex-col items-stretch space-y-0 border-b p-0 sm:flex-row">
				<div className="flex flex-1 flex-col justify-center gap-1 px-6 py-5 sm:py-6">
					<CardTitle>Bar Chart - Interactive</CardTitle>
					<CardDescription>
						{chartData.length > 0 ? 'Showing sentiment analysis for the given dates' : 'No data available'}
					</CardDescription>
				</div>
				<div className="flex">
					{['sentiment'].map((key) => {
						const chart = key as keyof typeof chartConfig;
						return (
							<button
								key={chart}
								data-active="sentiment"
								className="relative z-30 flex flex-1 flex-col justify-center gap-1 border-t px-6 py-4 text-left even:border-l data-[active=true]:bg-muted/50 sm:border-l sm:border-t-0 sm:px-8 sm:py-6"
							>
								<span className="text-xs text-muted-foreground">{chartConfig[chart].label}</span>
								<span className="text-lg font-bold leading-none sm:text-3xl">
									{(total.sentiment / chartData.length).toFixed(2)}
								</span>
							</button>
						);
					})}
				</div>
			</CardHeader>
			<CardContent className="px-2 sm:p-6">
				{chartData.length > 0 ? (
					<ChartContainer config={chartConfig} className="aspect-auto h-[250px] w-full">
						<BarChart
							accessibilityLayer
							data={chartData}
							margin={{
								left: 12,
								right: 12,
							}}
						>
							<CartesianGrid vertical={false} />
							<XAxis
								dataKey="date"
								tickLine={false}
								axisLine={false}
								tickMargin={8}
								minTickGap={32}
								tickFormatter={(value) => {
									const date = new Date(value);
									return date.toLocaleDateString('en-US', {
										month: 'short',
										day: 'numeric',
									});
								}}
							/>
							<ChartTooltip
								content={
									<ChartTooltipContent
										className="w-[150px]"
										nameKey="views"
										labelFormatter={(value) => {
											return new Date(value).toLocaleDateString('en-US', {
												month: 'short',
												day: 'numeric',
												year: 'numeric',
											});
										}}
									/>
								}
							/>
							<Bar dataKey="sentiment" fill={`var(--color-sentiment)`} />
						</BarChart>
					</ChartContainer>
				) : (
					<p className="text-center text-muted-foreground">No data to display</p>
				)}
			</CardContent>
		</Card>
	);
};

export default CustomChart;
