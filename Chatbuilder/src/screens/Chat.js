import React from 'react';
import { 
    getChats, 
    changeActions, 
    handleVisibleChat,
    onPlayButtonClick
} from '../actions/chats';
import Dialogue from '../services/dialogue'
import { connect } from 'react-redux';
import '../styles/chatsStyle.css';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import ExpandLessIcon from '@material-ui/icons/ExpandLess';
import { types } from '../components/constants/types';
import { convertToArray } from '../services/parse';

const DIALOGUE_SPECIAL_ACTIONS = { EXIT: 'Exit', IMAGE: 'Image', COLLECTION: 'Collection'};
const imageRegEx = /(\|(\s+)?\|(\s+)?Image\d+)$/;

class Chat extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            nextId: 1,
            msgArray: [],
            responseMessages: [],
            chat: {},
            isTyping: false,
            parseChat: this.props.builder.parseChat
        }
        this.minimumMessageDelay = 2500;
        this.interval = null;
    }

    componentDidMount = () => {
        const {getChats, builder } = this.props;
        this.setState({ 
            parseChat: builder.parseChat,
            chat: getChats(builder.parseChat)
        });
        this.nextMessage();
    }

    componentDidUpdate() {
        this.scrollToBottom();
        const {getChats, builder, chats } = this.props;
        const {chatPlayLineId, parseChat} = this.state;
        if (
            chatPlayLineId !== chats.chatPlayLineId ||
            builder.parseChat.length !== parseChat.length ||
            (builder.parseChat.length !== parseChat.length &&
              !builder.parseChat.includes(parseChat))
          ) {
            this.setState({
              chat: getChats(builder.parseChat),
              msgArray: [],
              responseMessages: [],
              nextId: 1,
              parseChat: builder.parseChat,
              chatPlayLineId: chats.chatPlayLineId,
            });
            this.nextMessage();
          }
    }

    scrollToBottom = () => {
        this.messagesEnd.scrollIntoView({ behavior: "smooth" });
    }
      
    nextMessage = () => {
        clearInterval(this.interval);
        this.interval = setInterval( () => {
            let currentMessage = Dialogue.__getDialogue('Chats', this.state.nextId);
            if (currentMessage && currentMessage.next) {
                this.handleSpecialAction(currentMessage);
                this.setState({
                    nextId: currentMessage.next,
                    msgArray: [...this.state.msgArray, currentMessage],
                    isTyping: true
                });
            } else {
                if(currentMessage) {
                if(this.handleSpecialAction(currentMessage)) {
                    clearInterval(this.interval);
                    return;
                }
                this.setState({
                    msgArray: [...this.state.msgArray, currentMessage],
                    responseMessages: currentMessage.responses,
                    isTyping: false
                });
                clearInterval(this.interval);
                return;
            }
            clearInterval(this.interval);
            this.setState({ isTyping: false })
            return;
            }
        }, 1000);
    }

    handleSpecialAction(currentMessage) {
        if (currentMessage && currentMessage.text && currentMessage.text.indexOf('||') === 0) {
            const { builder: { listOfBlocks } } = this.props;
            const string = currentMessage.text.substr(2);
            const isImage = imageRegEx.test(currentMessage.text);
            if (isImage) {
              const oneList = convertToArray(listOfBlocks);
              const imageLine = oneList.find((line) => line.id === currentMessage.id);
              if (imageLine && imageLine.image) {
                currentMessage.image = URL.createObjectURL(imageLine.image);
              }
            }
            switch (string) {
                case DIALOGUE_SPECIAL_ACTIONS.EXIT: 
                case DIALOGUE_SPECIAL_ACTIONS.COLLECTION: 
                    this.setState({
                        isTyping: false
                    })
                    return true;
                default:
                    return;
            }
        }
        return false;
      }

    sendMessage = (item) => {
        let currentMessage = Dialogue.__getDialogue('Chats', item);
        if (currentMessage.action) {
            this.props.changeActions(currentMessage.action);
        }
        currentMessage.user = true;
        this.setState({
            responseMessages: [],
            msgArray: [...this.state.msgArray, currentMessage],
            nextId: currentMessage.next
        }, () => this.nextMessage())
    }

    typingAnimation = () => (
        <div className="typingBlocks">
          <span className='typing-dot'></span>
          <span className='typing-dot'></span>
          <span className='typing-dot'></span>
        </div>
      );
  
    onChatClose = () => {
        const { handleVisibleChat } = this.props;
        handleVisibleChat();
        clearInterval(this.interval);
    }

    render() {
        const { responseMessages, isTyping } = this.state;
        const { isVisible } = this.props.chats;
        return (
            <div className={`chatsWrapper ${isVisible}`}>
                <div className="iconWrapper">
                {
                    isVisible ? 
                    <ExpandMoreIcon 
                        className="iconChat"
                        onClick={this.onChatClose}
                    /> : 
                    <ExpandLessIcon 
                        className="iconChat"
                        onClick={() => this.props.handleVisibleChat()}
                    />
                }
                </div>
                <div className={`messagesWrapper ${isVisible}`}>
                    {this.state.msgArray.map( (item, index) => (
                        <div 
                            key={index} 
                            className={
                                item.user ? "userMessageBlocks" : "messageBlocks"
                            }>
                            {item.image ?
                            <img 
                                src={item.image} 
                                alt="img" 
                                className={
                                    this.props.chatID === 1 ? "image" : "fullImage"
                                }/> :
                            <p 
                                className="messageText">
                                {item.text}
                            </p>
                        }
                        </div>
                    ))}
                    {
                        isTyping ? 
                        this.typingAnimation() : 
                        null
                    }
                    <div 
                        style={{ 
                            float:"left", 
                            clear: "both" 
                        }}
                        ref={(el) => { this.messagesEnd = el; }}>
                    </div>
                </div>
                <div className={`inputWrapper ${isVisible}`}>
                   {responseMessages ? responseMessages.map( (item, index) => (
                        <button 
                            key={index}
                            className="button buttonAnswer"
                            onClick={() => this.sendMessage(item)}>
                            {Dialogue.__getDialogue('Chats', item).text.substr(0,100)}
                        </button>
                    )) : null}
                </div>
            </div>
        )
    }
}

const mapStateToProps = (state) => {
    return {
        chats: state.chats,
        builder: state.builder
    }
}

export default connect(
    mapStateToProps , { 
        getChats, 
        changeActions, 
        handleVisibleChat,
        onPlayButtonClick
    })(Chat);
