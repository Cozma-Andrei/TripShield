import * as React from 'react';
import { Check, ChevronsUpDown } from 'lucide-react';

import { cn } from '../lib/utils';
import { Button } from '../components/ui/button';
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from '../components/ui/command';
import { Popover, PopoverContent, PopoverTrigger } from '../components/ui/popover';
import { Badge } from '../components/ui/badge';
import { Link } from 'react-router-dom';

export default function ComboboxDemo({ frameworks }) {
	const [open, setOpen] = React.useState(false);
	const [value, setValue] = React.useState('');

	console.log(frameworks);

	return (
		<Popover open={open} onOpenChange={setOpen}>
			<PopoverTrigger asChild>
				<Button variant="outline" role="combobox" aria-expanded={open} className="w-[200px] justify-between">
					{value ? frameworks.find((framework) => framework.CityName === value) : 'Search for a city...'}
					<ChevronsUpDown className="opacity-50" />
				</Button>
			</PopoverTrigger>
			<PopoverContent className="w-[300px] p-0">
				<Command>
					<CommandInput placeholder="Search for a City..." className="h-9" />
					<CommandList>
						<CommandEmpty>No city found..</CommandEmpty>
						<CommandGroup className="gap-0">
							{frameworks?.map((framework) => (
								<Link to={framework['Visit Link']} key={framework.CityName}>
									<CommandItem
										// key={framework.CityName}
										value={framework.CityName}
										className="flex"
										onSelect={(currentValue, event) => {
											// event.preventDefault();
											setValue(currentValue === value ? '' : currentValue);
											setOpen(false);

											// Navigate to the link
											// if (framework['Visit Link']) {
											// 	window.location.href = framework['Visit Link'];
											// }
										}}
									>
										<div className="flex justify-between w-full">
											<span>{framework.CityName}</span>
											<Badge className="text-sm" variant={framework['Crime Index'] < 50 ? 'default' : 'destructive'}>
												{framework['Crime Index'] < 50 ? 'Safe' : 'Not Safe'} to visit
											</Badge>
										</div>
										<Check className={cn('ml-auto', value === framework.CityName ? 'opacity-100' : 'opacity-0')} />
									</CommandItem>
								</Link>
							)) || <CommandEmpty>No cities available</CommandEmpty>}
						</CommandGroup>
					</CommandList>
				</Command>
			</PopoverContent>
		</Popover>
	);
}
