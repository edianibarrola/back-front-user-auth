import React from "react";
import { useHistory } from "react-router-dom";
import { Context } from "../store/appContext";

export function SecurePage(props) {
	const { store, actions } = React.useContext(Context);
	const history = useHistory();

	React.useEffect(
		() => {
			if (!store.authToken) {
				history.push("/login");
			}
		},
		[store.authToken]
	);

	return <>{props.children}</>;
}
