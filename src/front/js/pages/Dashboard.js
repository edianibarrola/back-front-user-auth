import React from "react";
import { Context } from "../store/appContext";

export function Dashboard() {
	const { store, actions } = React.useContext(Context);

	return (
		<div>
			<h3>Dashboard</h3>
			<button className="btn btn-outline-primary" onClick={() => actions.logout()}>
				Exit
			</button>
		</div>
	);
}
