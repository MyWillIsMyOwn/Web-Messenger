import { useEffect, useState, useContext } from "react";
import AuthContext from "./context/AuthContext";
import default_profile_photo from './assets/default_photo.jpg';
import { Link } from "react-router-dom";
const Users = () => {
    let {authTokens, logoutUser, user} = useContext(AuthContext)
    const [chats, setChats] = useState([]);
    useEffect(()=>{
        getUsers()
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])
    let getUsers = async()=>{
        let response = await fetch('http://127.0.0.1:8000/api/chats/', {
            method:'GET',
            headers:{
                'Content-Type': 'application/json', 
                'Authorization': 'Bearer ' + String(authTokens.access)
            }
        })
        let data = await response.json()
        if (response.status ===200){
            setChats(data)
            console.log(data)
        }else if(response.statusText === 'Unauthorized'){
            logoutUser()
        }
    }
    return (
        <div className="users_panel" style={{width: "400px"}}>
            <div className="search">
                <div className="info">Chats</div>
                <div className="type">
                    <textarea className='text_field' name='' rows="1" id='search_here' placeholder='Search...' style={{color: 'white'}}></textarea>
                </div>
            </div>
                <div className="users_display infinite_container" id='box'>
                    <div id='chats'>
                        {chats.map(chat=>(
                        <Link to={`/chat/${chat.chat_id}`}>
                            <div className="user infinite-item" id={chat.chat_id}>
                                <div className="user_container">
                                    <div className="profile_picture">
                                        <img src={default_profile_photo} alt="default pic" />
                                    </div>
                                    <div className="user_details">
                                        <div className="user_nickname">{chat.interlocutor}</div>
                                        {chat.last_message_owner === user.user_id && <div className="last_message">You: {chat.last_message_body}</div>}
                                        {chat.last_message_owner !== user.user_id && <div className="last_message">{chat.last_message_body}</div>}
                                    </div>
                                </div>
                            </div>
                        </Link>
                        ))}
                    </div>
                    <div className='hidden' id='blocked_list'></div>
                    <span id='more' hidden style={{color: 'white', display: 'none'}}>More users</span>
                    <div id='unknown' style={{display: 'none'}}></div>
                </div>
        </div>
    );
}
 
export default Users;