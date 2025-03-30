import React, { useEffect } from "react"; 
import { JSX } from "react/jsx-runtime";
export default function RankPage(){
        const [countryData, setCountryData] = React.useState([]);
    
    // Simulated API call to fetch crime rates (replace with actual API)
	const fetchCrimeRates = async () => {
		const url = import.meta.env.VITE_API_URL + '/average_by_all_countries';
		try {
			const response = await fetch(url);
			const data = await response.json();
			if (!response.ok) {
				throw new Error('Network response was not ok');
			}
			setCountryData(data);
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	};
    useEffect(() => {
		// Fetch crime rates when the component mounts
		fetchCrimeRates();
	}, []);

    let elementsCrime: JSX.Element[]=[];
    countryData.sort((a,b)=>{return b.average_crime_index-a.average_crime_index}).slice(0,10).forEach((ctr)=>{
        elementsCrime.push(<>
            <div className="flex-col items-center">
                <b className="text-sm font-medium text-black dark:text-blue-500 hover:underline">{ctr.country}</b>
                <div className="flex w-2/4 h-5 mx-4 bg-gray-200 rounded-sm dark:bg-gray-700">
                    <div className="h-5 bg-red-800 rounded-sm" style={{width: ctr.average_crime_index+"%"}}></div>
                    <span className="text-sm font-medium text-gray-500 dark:text-gray-400">{ctr.average_crime_index+"%"}</span>
                </div>
            </div>
        </>)
        
    })
    let elementsSafety: JSX.Element[]=[];
    countryData.sort((a,b)=>{return b.average_safety_index-a.average_safety_index}).slice(0,10).forEach((ctr)=>{
        elementsSafety.push(<>
            <div className="flex-col items-center">
                <b className="text-sm font-medium text-black dark:text-blue-500 hover:underline">{ctr.country}</b>
                <div className="flex w-2/4 h-5 mx-4 bg-gray-200 rounded-sm dark:bg-gray-700">
                    <div className="h-5 bg-green-800 rounded-sm" style={{width: ctr.average_safety_index+"%"}}></div>
                    <span className="text-sm font-medium text-gray-500 dark:text-gray-400">{ctr.average_safety_index+"%"}</span>
                </div>
            </div>
        </>)
        
    })
    return (
		<div className="flex-col space-y-24">
            <div className="space-y-10">
            <b className="text-xl">Crime data leader board</b>
            
            {elementsCrime.map((item, index) => (
            <div key={index}>{item}</div>
        ))}
            </div>
            <div className="space-y-10">
            <b className="text-xl">Safety leader board</b>
            
            {elementsSafety.map((item, index) => (
            <div key={index}>{item}</div>
        ))}
            </div>
        </div>   

	);
}