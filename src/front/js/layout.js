import React from "react";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import ScrollToTop from "./component/scrollToTop";

import { Home } from "./pages/home";
import injectContext from "./store/appContext";

import { RegisterUser } from "./pages/RegisterUser";
import { LoginUser } from "./pages/LoginUser";
import { Dashboard } from "./pages/Dashboard";
import { Navbar } from "./component/navbar";
import { Footer } from "./component/footer";
import { SecurePage } from "./component/SecurePage";

//create your first component
const Layout = () => {
	//the basename is used when your project is published in a subdirectory and not in the root of the domain
	// you can set the basename on the .env file located at the root of this project, E.g: BASENAME=/react-hello-webapp/
	const basename = process.env.BASENAME || "";

	return (
		<div className="d-flex flex-column h-100">
			<BrowserRouter basename={basename}>
				<ScrollToTop>
					<Switch>
						<Route exact path="/">
							<Home />
						</Route>

						<Route exact path="/register">
							<RegisterUser />
						</Route>

						<Route exact path="/login">
							<LoginUser />
						</Route>

						<Route exact path="/dashboard">
							<SecurePage>
								<Dashboard />
							</SecurePage>
						</Route>

						<Route>
							<h1>Not found!</h1>
						</Route>
					</Switch>
					<Footer />
				</ScrollToTop>
			</BrowserRouter>
		</div>
	);
};

export default injectContext(Layout);
