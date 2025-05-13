import './assets/style.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Home } from './pages/Home'
import { AuthProvider } from './context/Auth/AuthContext'
import { Container } from './components/Organisms/Container'
import { Login } from './pages/Login'

export const App = () => (
	<AuthProvider>
		<BrowserRouter>
			<Routes>
				<Route
					path = "/" 
					element = {
						<Container component = { <Home /> } />
					} 
				/>
				<Route
					path = "/login" 
					element = {
						<Container component = { <Login /> } />
					} 
				/>
			</Routes>
		</BrowserRouter>
	</AuthProvider>
)
