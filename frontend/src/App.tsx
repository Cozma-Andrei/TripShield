import './App.css';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
} from "react-router-dom";

import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuIndicator,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger,
  NavigationMenuViewport,
} from "./components/ui/navigation-menu";
import { cn } from "./lib/utils";

import LandingPage from './pages/LandingPage';
import MapPage from './pages/MapPage';
import RankPage from './pages/RankPage'
function App() {
	return (
		<Router>
			<nav className="w-full bg-green-100 shadow-sm px-6 py-3 flex items-center justify-between">
				<div className="text-2xl font-extrabold text-green-700 tracking-tight">
					TripShield
				</div>

				<NavigationMenu>
					<NavigationMenuList>
						<NavigationMenuItem>
							<Link to="/" className={cn("px-4 py-2 text-green-800 hover:text-green-900 font-medium")}>
								Home
							</Link>
						</NavigationMenuItem>

						<NavigationMenuItem>
							<Link to="/map" className={cn("px-4 py-2 text-green-800 hover:text-green-900 font-medium")}>
								Map
							</Link>
						</NavigationMenuItem>
						<NavigationMenuItem>
							<Link to="/rank" className={cn("px-4 py-2 text-green-800 hover:text-green-900 font-medium")}>
								Ranking Countries
							</Link>
						</NavigationMenuItem>
					</NavigationMenuList>

					<NavigationMenuIndicator />
					<NavigationMenuViewport />
				</NavigationMenu>
			</nav>

			<div className="p-6">
				<Routes>
					<Route path="/" element={<LandingPage />} />
					<Route path="/map" element={<MapPage />} />
					<Route path='/rank' element={<RankPage />}/>
				</Routes>
			</div>
		</Router>
	);
}

export default App;
