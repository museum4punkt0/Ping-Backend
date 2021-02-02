import { builderType } from './types';
import { handleVisibleChat, onPlayButtonClick } from './chats';
export const addItem = (id, item, parent) => {
    return (dispatch) => {
        dispatch({
            type: builderType.ITEM_ADD,
            id,
            item,
            parent
        });
    }
}

export const uploadChat = text => dispatch => {
    dispatch({
        type: builderType.CHAT_UPLOAD_FROM_FILE,
        text
    });
    return Promise.resolve();
}

export const deleteItem = (item) => {
    return (dispatch) => {
        dispatch({
            type: builderType.ITEM_DELETE,
            id: item.id,
            item,
        });
    }
}

export const sortList = (newList, item) => dispatch => {
    dispatch({
        type: builderType.ITEMS_SORT,
        newList,
        item
    });
}

export const changeType = (index, item, payload) => dispatch => {
    dispatch({
        type: builderType.ITEM_CHANGE_TYPE,
        index,
        item,
        payload
    });
}

export const changeTextInput = (text, index, item) => dispatch => {
    dispatch({
        type: builderType.ITEM_TEXT_CHANGED,
        text,
        index,
        item
    });
}

export const saveImage = (file, index, item) => dispatch => {
    dispatch({
        type: builderType.ITEM_SAVE_IMAGE,
        file,
        index,
        item
    });
}

export const parseChatFrom = (initialId) => dispatch => {
    dispatch({
        type: builderType.CHAT_PLAY,
        initialId
    });
}

export const saveToClipboard = () => dispatch => {
    dispatch({
        type: builderType.CHAT_SAVE_TO_CLIPBOARD
    });
}

export const setNewNextId = (newNextId, currentItem) => dispatch => {
    dispatch({
        type: builderType.ITEM_SET_NEXT_ITEM,
        newNextId,
        currentItem
    });
}

export const resetAll = () => dispatch => {
    dispatch({
        type: builderType.CHAT_RESET
    });
}

export const changeAlertState = () => dispatch => {
    dispatch({
        type: builderType.ALERT_CHANGE_STATE
    });
}

export const setFocusedLine = (item) => dispatch => {
    dispatch({
        type: builderType.SET_FOCUSED_LINE,
        item
    });
}

export const checkChatSpecialLines = ({ id }) => (dispatch, getState) => {
    dispatch({
      type: builderType.CHAT_CHECK_SPECIAL_LINES,
    });
    const { wrongChatLinesIds } = getState().builder;
    if (!wrongChatLinesIds) {
      dispatch(handleVisibleChat(true));
      dispatch(parseChatFrom(id));
      dispatch(onPlayButtonClick(id));
    }
  };
  
  export const changeWrongLinesState = () => (dispatch) => {
    dispatch({
      type: builderType.WRONG_LINES_CHANGE_STATE,
    });
  };
