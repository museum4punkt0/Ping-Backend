import { builderType } from "../actions/types";
import {
    sortListById,
    parseEmojis,
    chatParser,
    parseChat,
    parseUploadedChat,
    insertElements,
    insertElement,
    convertToList,
    convertToArray,
    getWrongSpecialLines,
    deleteElement,
    checkOnMaxChildren
} from '../services/parse';
import moment from 'moment'
import { types } from "../components/constants/types";
import { addingChildren, addingMain, deletingChildren, deletingMain } from "../config/helpers";
import { type } from "os";

const InitialState = {
    listOfBlocks: [
        {
            id: 1,
            children: [],
            nextId: 1,
            type: types.text,
            message: '',
            image: '',
            isChild: false,
            isCustomNextId: false,
        }
    ],
    dragItem: {},
    destinationParent: {},
    countBlocks: 1,
    savedNextId: null,
    parseChat: `1 ||${types.exit}`,
    isCustomId: false,
    isUploadedText: false,
    focusId: null,
    isError: false,
    isIncorrectFile: false,
    errorMessage: '',
    focusedItem: null,
    wrongChatLinesIds: ''
}

export default function reducer(state = InitialState, action) {
    switch (action.type) {

        case builderType.ITEM_ADD:

            const { item: actionItem, parent: parentBlock, id: actionId } = action;
            const childrenCount = actionItem ? actionItem.children.length : 0;
            const countOfBlocks = convertToArray(state.listOfBlocks).length;
            const itemId = (actionId ? actionId + childrenCount : countOfBlocks) + 1;
            const nextId = parentBlock && itemId <= countOfBlocks ? countOfBlocks : itemId;

            const item = {
                id: itemId,
                children:[],
                nextId,
                type: types.text,
                message: '',
                image: '',
                isChild: actionItem?.isChild,
                isCustomNextId:false,
            };
            const items = insertElement(item,  [...state.listOfBlocks]);
            if (item.isChild) {
                let index = items.indexOf(parentBlock);
                item.nextId = parentBlock.id + parentBlock.children.length + 1;
                let cIndex = parentBlock.children.map(e => e.id).indexOf(actionId);
                parentBlock.children.splice(cIndex + 1, 0, item);
                items[index] = parentBlock;
                
            } else {
                let index = items.map(e => e.id).indexOf(actionId);
                index = index === -1 ? countOfBlocks + 1 : index;
                items.splice(index + 1, 0, item);
            }

           return {
            ...state,
            listOfBlocks: items,
            countBlocks: countOfBlocks + 1,
            focusId: item.id,
            addedElement: item,
            isIncorrectFile: false,
        }

        case builderType.ITEM_DELETE: {
            const { item: actionItem, id: actionId } = action;
            const countOfBlocks = convertToArray(state.listOfBlocks).length;
            const list = [...state.listOfBlocks];
            let parentBlock = null;
            if (actionItem.isChild) {
                parentBlock = state.listOfBlocks.find((el) =>
                    el.children.find((child) => child.id === actionId)
                );
                let index = list.indexOf(parentBlock);
                let cIndex = parentBlock.children.map(e => e.id).indexOf(actionId);
                parentBlock.children.splice(cIndex, 1);
                list[index] = parentBlock;
            } else {
                let index = list.map(e => e.id).indexOf(actionId);
                index = index === -1 ? countOfBlocks : index;
                list.splice(index, 1);
            }
            const items = deleteElement(actionItem,  [...list], parentBlock);

            return {
                ...state,
                listOfBlocks: items
            }
        }

        case builderType.ITEM_CHANGE_TYPE:
            let changedList = [...state.listOfBlocks];
            if (changedList[action.index]  && changedList[action.index].id === action.item.id) {
                if (action.payload === types.answer && action.index >= 1 && !changedList[action.index].children.length) { // moved item to children
                    const parent = changedList[action.index - 1];
                    const isMaxChildren = checkOnMaxChildren(parent);
                    if(isMaxChildren) return {...state};
                    const child = changedList[action.index];
                    child.type = types.text;
                    child.isChild = true;
                    changedList[action.index - 1].children.push(child);
                    changedList.splice(action.index, 1);
                } else {
                    changedList[action.index].type = action.payload;
                }
                changedList = insertElements(action.item, changedList, state.listOfBlocks)
            } 
            else {
                changedList.map((mainLine, mainIndex) => {
                    if (mainLine.children[action.index] && mainLine.children[action.index].id === action.item.id) {
                        if (action.payload === types.question) {
                            const child = mainLine.children[action.index];
                            child.type = types.text;
                            child.isChild = false;
                            child.children = mainLine.children.splice(action.index + 1, mainLine.children.length - 1);
                            mainLine.children.splice(action.index, 1);

                            changedList.splice(mainIndex + 1, 0, child);
                            mainLine.nextId = mainLine.children.length ?  mainLine.nextId : child.id - 1;
                        } else {
                            mainLine.children[action.index].type = action.payload;
                        }
                    }
                    return true;
                });
            }

            return {
                ...state,
                listOfBlocks: changedList,
            }

        case builderType.ITEMS_SORT:
            //insertElements(action.item, action.newList, state.listOfBlocks);
           // const sortedList = sortListById(action.newList, state.countBlocks);

            const { newList } = action;
            const { listOfBlocks } = state;
            const prevItems = convertToArray(listOfBlocks);
            const newItems = convertToArray(newList);
            let isIdenticalArrays = newItems.every((line, index) => line.id === prevItems[index].id);
            isIdenticalArrays = isIdenticalArrays && newList.length === listOfBlocks.length;

            return {
                ...state,
                listOfBlocks: !isIdenticalArrays
                    ? insertElements(action.item, newList, listOfBlocks)
                    : listOfBlocks,
                isCustomId: false,
                isUploadedText: false,
                isError: false
            }

        case builderType.ITEM_TEXT_CHANGED:
            let changeTextList = state.listOfBlocks;

            if (changeTextList[action.index] && changeTextList[action.index].id === action.item.id) {
                changeTextList[action.index].message = parseEmojis(action.text);
            } else {
                changeTextList.map( mainLine => {
                    if (mainLine.children[action.index] && mainLine.children[action.index].id === action.item.id) {
                        mainLine.children[action.index].message = parseEmojis(action.text);
                    }
                    return true;
                });
            }

            return {
                ...state,
                listOfBlocks: changeTextList
            }

        case builderType.ITEM_SAVE_IMAGE:
            let setImage = state.listOfBlocks;

            if (setImage[action.index] && setImage[action.index].id === action.item.id) {
                setImage[action.index].image = action.file;
            } else {
                setImage.map( mainLine => {
                    if (mainLine.children[action.index] && mainLine.children[action.index].id === action.item.id) {
                        mainLine.children[action.index].image = action.file;
                    }
                    return true;
                });
            }
            return {
                ...state,
                listOfBlocks: setImage
            }

        case builderType.CHAT_PLAY:
            const slicedList = state.listOfBlocks.filter(item => item.id >= action.initialId);
            let chat = convertToList(slicedList, true);
            chat = `1 You started a chat...  -> ${parseInt(chat)} \n` + chat;

            return {
                ...state,
                parseChat: chat
            }

        case builderType.CHAT_CHECK_SPECIAL_LINES:
            const oneListOfBlocks = convertToArray(state.listOfBlocks);
            const wrongChatLinesIds = getWrongSpecialLines(oneListOfBlocks).map(line => line.id);
            if(wrongChatLinesIds.length) {
                return {
                    ...state,
                    wrongChatLinesIds: wrongChatLinesIds.join(",")
                }
            }   
            return {
                ...state,
                wrongChatLinesIds: ''
            }

        case builderType.CHAT_SAVE_TO_CLIPBOARD:
             const { message: firstLine, image } = state.listOfBlocks[0] || InitialState;
             const chatParsed =  convertToList(state.listOfBlocks); /*state.isUploadedText ?
                parseUploadedChat(state.listOfBlocks, 1) :
                parseChat(state.listOfBlocks, 1); */
             const currentTime = moment().format(' YYYY-MM-DD HH`mm');
             const documentTitle = image?.name || firstLine?.slice(0,50).trim() || 'chat';
             //download file
             var element = document.createElement('a');
             element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(chatParsed));
             element.setAttribute('download', `${documentTitle} ${currentTime}.txt`);
             element.style.display = 'none';
             document.body.appendChild(element);
             element.click();
             document.body.removeChild(element);

             return {
                ...state,
             }

        case builderType.ITEM_SET_NEXT_ITEM:
            let currentList = state.listOfBlocks;
            if (action.currentItem.isChild) {
                currentList.map( item => {
                    if (item.children) {
                        item.children.map( child => {
                            if (child.id === action.currentItem.id) {
                                child.nextId = action.newNextId - 1;
                                child.isCustomId = true;
                                child.isCustomNextId = true;
                            }
                            return true;
                        })
                    }
                    return true;
                });
            } else {
                currentList.map( item => {
                    if (item.id === action.currentItem.id) {
                        item.nextId = action.newNextId - 1;
                        item.isCustomId = true;
                        item.isCustomNextId = true;
                    }
                    return true;
                });
            }

            return {
                ...state,
                listOfBlocks: currentList,
                isCustomId: true,
                isError: false
            }

        case builderType.CHAT_RESET:
            const initial = [
                {
                    id: 1,
                    children: [],
                    nextId: 1,
                    type: types.text,
                    message: '',
                    image: '',
                    isChild: false,
                }
            ];
            return {
                ...state,
                listOfBlocks: initial,
                dragItem: {},
                destinationParent: {},
                countBlocks: 1,
                savedNextId: null,
                parseChat: `0 ||${types.exit}`,
                isCustomId: false,
                isUploadedText: false,
                isError: false
            }

        case builderType.CHAT_UPLOAD_FROM_FILE:
            let isIncorrectFile = false;
            let { parsedList, errorMessage, isParserError } = chatParser(action.text);
            let size = parsedList.length;

            document.getElementById('uploadChat').value = '';

            if(isParserError) {
                return {
                    ...state,
                    isIncorrectFile: true,
                    errorMessage
                }
            }
            const oneList = convertToArray(parsedList);
            const isCorrectOrderId = oneList.every((el, index) => el.id === index + 1);
            if (!isCorrectOrderId) {
              const wrongLine = oneList.find((el, index) => el.id !== index + 1);
              parsedList = state.listOfBlocks;
              errorMessage = `This answer should be after the question: #${wrongLine.id + 1} ${wrongLine.message}`;
              isIncorrectFile = true;
            }

            for (let i of parsedList) {
                if (!i.nextId && i.children.length === 0) {
                    parsedList = state.listOfBlocks;
                    isIncorrectFile = true;
                    break
                }
            }

            if (!isIncorrectFile) {
                parsedList.map(item => size = size + item.children.length);
            }

            return {
                ...state,
                listOfBlocks: parsedList,
                countBlocks: size,
                isCustomId: true,
                isUploadedText: true,
                isIncorrectFile,
                errorMessage
            }

        case builderType.ALERT_CHANGE_STATE:
            return {
                ...state,
                isIncorrectFile: !state.isIncorrectFile
            }

        case builderType.SET_FOCUSED_LINE:
            return {
                ...state,
                focusedItem: action.item
            }

        case builderType.WRONG_LINES_CHANGE_STATE:
            return {
                ...state,
                wrongChatLinesIds: ""
            }

        default:
            return state;
    }
}
