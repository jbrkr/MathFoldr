import React from "react";
import { Route, Switch , Redirect} from 'react-router-dom';
//import Home from "../components/Home";

//import Login from '../components/auth/Login';
//import Signup from '../components/auth/Signup';
//import Logout from '../components/auth/Logout';
//import Account from '../components/settings/Account';
//import Profile from '../components/settings/Profile';

import Error404 from '../components/Error/404';
import SearchPage from "../components/Search/SearchPage"

const AppRouter = ( props ) => {

    console.log("================================== AppRouter ======================================");

    function AuthenticatedRoute({ children, ...rest }) {
        // Get Auth Context
        const auth = useAuthContext();

        return (
          <Route
            {...rest}
            render={({ location }) =>
              auth.state.isAuthenticated ? (
                children
              ) : (
                <Redirect
                  to={{
                    pathname: "/login",
                    state: { from: location }
                  }}
                />
              )
            }
          />
        );
      }

    return (
        <React.Fragment>
            <Switch>
                <Route path="/" exact component={Home} />
                <Route path="/search" exact component={SearchPage} />
                <Route component={Error404} />
            </Switch>
        </React.Fragment>
    );
}

export default AppRouter;