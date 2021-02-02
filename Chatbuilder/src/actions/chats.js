import { chatsTypes } from './types';
import Dialogue from '../services/dialogue';

export const getChats = (chatID) => (dispatch) => {
    Dialogue.parse('Chats', chatID);
    const chat = Dialogue.dialogues;
    dispatch({ type: chatsTypes.CHATS_LOADED, payload: chat });
    return chat;
}

export const changeActions = (actions) => dispatch => {
    dispatch({
        type: chatsTypes.CHANGE_ACTIONS,
        payload: actions
    })
}

export const handleVisibleChat = (isVisible) => dispatch => {
    dispatch({
        type: chatsTypes.HANDLE_VISIBLE_CHAT,
        isVisible
    })
}

export const onPlayButtonClick = (id) => (dispatch) => {
    dispatch({
      type: chatsTypes.PLAY_BUTTON_CLICK,
      id
    })
}