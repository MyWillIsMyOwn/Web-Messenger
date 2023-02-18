import options_icon from './assets/options.png';
import default_profile_photo from './assets/default_photo.jpg';
import SendMessage from './SendMessage';
const MessagesPanel = () => {
    return (
        <div className="messages_panel">
                    <div className="user_info">
                        <div className="profile_picture">
                            <img src={default_profile_photo} alt="" className='pic'/>
                        </div>
                        <div className="profile_name">
                            <span style={{color: 'white', font:'large'}} id="current_user">Test</span>
                        </div>
                        <div className="profile_options" id='profile_options'>
                            <img src={options_icon} alt="options" className='options' />
                        </div>
                        <div className="user_settings_window" id='user_settings_window' style={{display: 'none'}}>
                            <div className="profile_view">
                                <div className="picture">
                                    <div className="photo"></div>
                                </div>
                                <div className="name">
                                    <span style={{color: 'white', font: 'large'}} id='current_user_in_settings'></span>
                                </div>
                            </div>
                            <div className="settings">
                                {/* TO RECREATE */}
                            </div>
                        </div>
                    </div>
                    <div className="separator">
                    </div>
                    <div className="messages" id='chat_log'>
                        {/* MESSAGES WILL BE DISPLAYED HERE */}
                    </div>
                    <SendMessage />
                </div>
    );
}
 
export default MessagesPanel;