import photo_icon from './assets/photoicon.png';
import send_icon from './assets/sendbutton.png';
import { useEffect, useRef } from 'react';
const SendMessage = () => {
    const textareaRef = useRef(null);
    useEffect(() => {
      const textarea = textareaRef.current;
  
      const handleInput = () => {
        textarea.style.height = 'auto';
        textarea.style.height = `${textarea.scrollHeight}px`;
      };
  
      textarea.addEventListener('input', handleInput);
  
      return () => {
        textarea.removeEventListener('input', handleInput);
      };
    }, []);
    return (
        <div className="message_type">
        <div className="message_content">
            <input type="text" name='receiver' id='receiver' value="" hidden />
            <textarea name="msg" className="text_field" id="chat-message-input" rows="1"
            placeholder="Write message..." style={{color: 'white'}} ref={textareaRef}></textarea>
            {/* add script to resize */}
            <img src={photo_icon} alt="photo_icon" className='photo'/>
        </div>
        <div className="send_button">
            <input type="image" id='chat-message-submit' src={send_icon} alt='send_button'/>
        </div>
    </div>
    );
}
 
export default SendMessage;