import normal_icon from './assets/normal.png';
import ignored_icon from './assets/ignored.png';
import default_profile_photo from './assets/default_photo.jpg';
import { Link } from "react-router-dom";
import { useContext, useEffect } from 'react';
import AuthContext from './context/AuthContext';
const Navbar = () => {
    useEffect(()=>{
        /////////////////////////////    Chat settings   ////////////////////////////
document.getElementById("profile_options").onclick = function() {
    console.log("TEST")
    var box = document.getElementById("user_settings_window")
    if (box.style.display === "none") {
      box.style.display = "block";
    } else {
      box.style.display = "none";
    }
  }

  var window_height = window.innerHeight;
  var window_widht = window.innerWidth;

window.addEventListener('resize', function(){
    window_height = window.innerHeight;
    window_widht = window.innerWidth;
    var box = document.getElementById("user_settings_window")
    if (window_height<=400){      
        box.classList.add("height")
    }
    else{
        box.classList.remove("height")
        
    }
    if (window_widht<=550){      
        box.classList.add("width")
    }
    else{
        box.classList.remove("width")
    }
    if (window_height<=400 && window_widht<=550){      
        box.classList.add("small")
    }
    else{
        box.classList.remove("small")
    }
})
///////////////////////////    User settings    ////////////////////////////
document.getElementById("user_profile_picture").onclick = function() {
    var box = document.getElementById("settings_window")
    if (box.style.display === "none") {
      box.style.display = "block";
    } else {
      box.style.display = "none";
    }
  }
  window.addEventListener('resize', function(){
    window_height = window.innerHeight;
    window_widht = window.innerWidth;
    var box = document.getElementById("settings_window")
    if (window_height<=320){      
        box.classList.add("height")
    }
    else{
        box.classList.remove("height")
    }
  });

    })
    let {logoutUser} = useContext(AuthContext)

    
    
    return (
        <div className="tool_panel">
        <div className="tools">
            <div className="chats checked" id='normal'>
                <img src={normal_icon} alt="messages" />
            </div>
            <div className="ignored" id='ignored'>
                <img src={ignored_icon} alt="ignored" />
            </div>
        </div>
        <div className="profile">
            <div className="profile_picture" id='user_profile_picture'>
                <img src={default_profile_photo} alt="default pic" />
            </div>
        </div>
        <div className="settings_window" id='settings_window' style={{display: 'none'}}>
            <div className="settings">
                <div className="change_photo">
                    <Link href="/update_photo">
                        <span style={{color: 'white', font: "large"}}>Change profile photo</span>
                    </Link>
                </div>
                <div className="change_password">
                    <Link href="/change_password/">
                        <span style={{color: 'white', font: "large"}}>Change password</span>
                    </Link>
                </div>
                <div className="delete_account">
                    <Link href="/delete_account/">
                        <span style={{color: 'white', font: "large"}}>Delete account</span>
                    </Link>
                </div>
            </div>
            <div className="logout">
                <span onClick={() => logoutUser()} style={{color: 'white', font: "large"}}>Logout</span>
            </div>
        </div>
    </div>
    );
}
 
export default Navbar;