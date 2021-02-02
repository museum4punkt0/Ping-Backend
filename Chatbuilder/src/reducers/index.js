import { combineReducers } from "redux";

import chats from './chats';
import builder from './builder';

export default combineReducers({ builder, chats });