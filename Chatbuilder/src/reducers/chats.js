import { chatsTypes } from "../actions/types";

const INITIAL_STATE = {
  chats: [],
  actions: {
    a0: null,
    a1: null,
    a2: null,
    a3: null,
    a4: null
  },
  isVisible: false
};

export default function reducer(state = INITIAL_STATE, action) {
  switch (action.type) {
      
    case chatsTypes.CHATS_LOADED:
      return { ...state, chats: action.payload };

    case chatsTypes.CHANGE_ACTIONS:
      const { variable, operation, value } = action.payload;
      switch (operation) {
        case '+':
          return Object.assign({}, state, state.actions[variable] = state.actions[variable] + +value);
        case '-':
          return Object.assign({}, state, state.actions[variable] = state.actions[variable] - +value);
        default:
          return true;
      }

      case chatsTypes.HANDLE_VISIBLE_CHAT:
        return {
          ...state,
          isVisible: action.isVisible ? action.isVisible : !state.isVisible
        }
        
    
    case chatsTypes.PLAY_BUTTON_CLICK:
       return {
          ...state,
          chatPlayLineId: action.id
       }
      
      default:
          return state;
  }
}