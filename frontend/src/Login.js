import { useContext } from "react";
import AuthContext from "./context/AuthContext";

const Login = () => {
    let {loginUser} = useContext(AuthContext)
    return (
        <div className="container">
            <div className="heading">Log in</div>
            <form onSubmit={loginUser}>
                <div className="card-details">
                    <div className="card-box">
                        <span className="details">Username</span>
                        <input type="text" name="username" placeholder="username" />
                    </div>
                    <div className="card-box">
                        <span className="details">Password</span>
                        <input type="password" name="password" placeholder="password" />
                    </div>
                </div>
                <div className="button">
                    <input type="submit" name="Log into" value="Log in" />
                </div>
            </form>
        </div>
    );
}
 
export default Login;