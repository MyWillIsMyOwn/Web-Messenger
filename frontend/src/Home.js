import './home.css';
import { Link } from "react-router-dom";
import { useEffect} from 'react';
import Navbar from './Navbar';
import Users from './Users';
import MessagesPanel from './Messages';
const Home = () => {

    useEffect(() =>{
        /////////////////////////////    Window Resizer    ////////////////////////////
        const resizer = document.getElementById('dragMe');
        const leftSide = resizer.previousElementSibling;
        const rightSide = resizer.nextElementSibling;

        // The current position of mouse
        let x = 0;

        // Width of left side
        let leftWidth = 0;

        // Handle the mousedown event
        // that's triggered when user drags the resizer
        const mouseDownHandler = function (e) {
            // Get the current mouse position
            x = e.clientX;
            leftWidth = leftSide.getBoundingClientRect().width;

            // Attach the listeners to `document`
            document.addEventListener('mousemove', mouseMoveHandler);
            document.addEventListener('mouseup', mouseUpHandler);
        };

        // Attach the handler
        resizer.addEventListener('mousedown', mouseDownHandler);

        const mouseMoveHandler = function (e) {
            // How far the mouse has been moved
            const dx = e.clientX - x;

            const newLeftWidth = ((leftWidth + dx) * 100) / resizer.parentNode.getBoundingClientRect().width;
            leftSide.style.width = `${newLeftWidth}%`;

            resizer.style.cursor = 'col-resize';
            document.body.style.cursor = 'col-resize';
            leftSide.style.userSelect = 'none';
            leftSide.style.pointerEvents = 'none';

            rightSide.style.userSelect = 'none';
            rightSide.style.pointerEvents = 'none';
        };

        const mouseUpHandler = function () {
            resizer.style.removeProperty('cursor');
            document.body.style.removeProperty('cursor');

            leftSide.style.removeProperty('user-select');
            leftSide.style.removeProperty('pointer-events');

            rightSide.style.removeProperty('user-select');
            rightSide.style.removeProperty('pointer-events');

            // Remove the handlers of `mousemove` and `mouseup`
            document.removeEventListener('mousemove', mouseMoveHandler);
            document.removeEventListener('mouseup', mouseUpHandler);
        };
    });
    return (
        <div className="main">
            <div className="main_div" id='main_div'>
                <Navbar />
                <Users />
                <div className="resizer" id='dragMe'>
                </div>
                <MessagesPanel />
            </div>
        </div>
    );
}
 
export default Home