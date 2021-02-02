import { types } from "../components/constants/types";
import { toArray } from "react-emoji-render";

const DIALOGUE_IDS_FOR_SPECIAL_ACTIONS = {
    EXIT: '10001',
    CAM: '10002',
    MAP: '10003', 
    IMAGE: '10004', 
    COLLECTION: '10005', 
    IMAGETAKEN: '10007' 
};
let _imageCounter = 0;
const newLineChar = '/n'
const nextItemRegEx = /(->)\s*\d+$/;
const choicesRegEx = /(\[\s*\d+\s*\])$|\[(\s*\d+\s*,?\s*){1,}\]$/;
const exitRegEx = /(\|(\s+)?\|(\s+)?Exit)$/;
const collectionRegEx = /(\|(\s+)?\|(\s+)?Collection)$/;

export const chatParser = (text) => {
  let parsedList = [];
  let errorMessage = "";
  const allLinesIds = [];
  let isParserError = false;
  const lines = text
                .match(/^.*((\r\n|\n|\r)|$)/gm)
                .filter(line => line.replace(/^\s*$/, ''));
  let lostChildrenId = [];
  const EXIT_ID = lines.length;

  lines.map((line, index) => {
    if (line && line.trim() && !isParserError) {
      let hasChildren = true;
      const dialogue = {};
      let dialogue_line = line.trim();
      const isExit = exitRegEx.test(dialogue_line);
      const isCollection = collectionRegEx.test(dialogue_line);

      if (!parseInt(dialogue_line) && parseInt(dialogue_line) !== 0) {
        errorMessage = `In this line you must enter line number: ${dialogue_line}`;
        return (isParserError = true);
      }
      dialogue.id = parseInt(dialogue_line);

      dialogue.children = [];
      dialogue.type = types.text;
      dialogue_line = dialogue_line
        .substr(dialogue.id.toString().length)
        .trim();

      const searchArrowWithId = dialogue_line.match(nextItemRegEx);
      const searchChoices = dialogue_line.match(choicesRegEx);

      if(!searchArrowWithId && !searchChoices && !isExit && !isCollection){
        errorMessage = `Something is wrong with this line #${dialogue.id}: ${dialogue_line}`;
        return (isParserError = true);
      }

      if (dialogue_line.indexOf("->") !== -1) {
        if (!searchArrowWithId) {
          errorMessage = `The next element is incorrect in line #${dialogue.id}: ${dialogue_line}`;
          return (isParserError = true);
        }
        const lineId = +searchArrowWithId[0].match(/\d+/)[0];
        if(lineId === dialogue.id) {
          errorMessage = `The next element (${lineId}) can't be equal to line number #${dialogue.id}: ${dialogue_line}`;
          return (isParserError = true);
        }
        hasChildren = false;
        const nextIndex = lines.map((i) => parseInt(i)).indexOf(lineId);
        dialogue_line = dialogue_line.substr(0, searchArrowWithId.index);
        dialogue.nextId = nextIndex === -1 ? EXIT_ID : nextIndex;
      }

      dialogue_line = dialogue_line.trim();

      if (dialogue_line.indexOf("[") !== -1 && hasChildren) {
        
        if (!searchChoices) {
          errorMessage = `Answers are incorrect in this line: ${dialogue_line}`;
          return (isParserError = true);
        }
        let choices = searchChoices[0].replace(/\s/g, "");
        choices = JSON.parse(choices);

        const isAnswersIdsUnique = checkUniqueAnswersIds(parsedList, choices);
        if(isAnswersIdsUnique){
          errorMessage = `Another question already refers to answer(s) from this line #${dialogue.id}: ${dialogue_line}`;
          return (isParserError = true);  
        }

        const isNextIdsBigger = choices.every(choice => choice > dialogue.id);
        if(!isNextIdsBigger){
          errorMessage = `Numbers in answers must be bigger than line number #${dialogue.id}: ${dialogue_line}`;
          return (isParserError = true);  
        }
        dialogue.children = choices;
        lostChildrenId = [...lostChildrenId, choices].flat();
        dialogue_line = dialogue_line.substr(0, searchChoices.index);
      }

      if (dialogue_line.trim().split("||")[1]) {
        //special action
        switch (dialogue_line.trim().split("||")[1]) {
          case types.exit:
            dialogue.type = types.exit;
            dialogue.nextId = EXIT_ID;
            dialogue.text = dialogue_line.trim();
            break;

          case types.collection:
            dialogue.type = dialogue_line.trim().split("||")[1];
            dialogue.text = dialogue_line.trim();
            dialogue.nextId = EXIT_ID;
            break;
          case types.cam:
          case types.map:
            dialogue.type = dialogue_line.trim().split("||")[1];
            dialogue.text = dialogue_line.trim();
            break;
          default:
            if (dialogue_line.trim().split("||")[1].includes(types.image)) {
              dialogue.type = types.image;
              dialogue.text = dialogue_line.trim().split("||")[1];
            }
            break;
        }
      } 
      else {
        dialogue.text = dialogue_line.trim();
      }

      const isLineIdDublicated = checkUniqueLineId(allLinesIds, dialogue.id)
      if(isLineIdDublicated && dialogue.type === types.text){
        errorMessage = `Line number isn't unique: ${dialogue_line}`;
        return (isParserError = true);
      }
      allLinesIds.push(dialogue.id);

      if (lostChildrenId.indexOf(dialogue.id) !== -1) {
        // eslint-disable-next-line no-loop-func
        parsedList.map((item) => {
          if (item.childrenId && item.childrenId.includes(dialogue.id)) {
            const childId = lines.map((i) => parseInt(i)).indexOf(dialogue.id);
            item.children.push({
              id: childId + 1,
              children: [],
              nextId: dialogue.nextId,
              type: dialogue.type,
              message: dialogue.text,
              image: "",
              isChild: true,
              isCustomId: true,
            });
          }
          return true;
        });
      } else if (dialogue.text || dialogue.type === types.image) {
        parsedList.push({
          id: index + 1,
          children: [],
          childrenId: dialogue.children,
          nextId: dialogue.nextId,
          type: dialogue.type,
          message: dialogue.text,
          image: "",
          isChild: false,
          isCustomId: true,
        });
      }
    }
  });
  return { parsedList, errorMessage, isParserError };
};

const checkUniqueAnswersIds = (list, choices) => {
  const childrenIds = [];
  list
    .filter((line) => line.childrenId.length)
    .map((line) => line.childrenId.map((child) => childrenIds.push(child)));
  return childrenIds.some(id => choices.includes(id));
};

const checkUniqueLineId = (array, lineId) => array.some(id => id === lineId);

export const sortListById = (newList, sizeOfArray) => {
    newList.map( (item, index) => { 
        //change id for main items
        if (index === 0 ){
            item.id = index+1;
            item.nextId = item.id;
        } else {
            const { children } = newList[index - 1];
            
            item.id =  children.length === 0 ? newList[index-1].id + 1 : newList[index - 1].id + children.length+1;
            item.nextId = newList[index].id
            item.isCustomId = false;
        } 
        return true;
    });
    
    if (newList.length > 1) {
        //change id for last item
        newList[newList.length - 1].nextId = sizeOfArray;
    }

    newList.map( (item, index) => {
        //change id for child items
        if (item.children.length !== 0) {
            item.children.map( (childItem, childIndex) => {
                childItem.id = item.id + childIndex + 1;
                childItem.nextId = newList[index+1] ? newList[index+1].id - 1 : childItem.id;
                childItem.isCustomId = false;
                return true;
            })
        }
        return true;
    });

    return newList;
}

export const parseEmojis = value => {
  const emojisArray = toArray(value);

  const newValue = emojisArray.reduce((previous, current) => {
    if (typeof current === "string") {
      return previous + current;
    }
    return previous + current.props.children;
  }, "");

  return newValue;
};

export const parseChat = (stateList, firstMessage) => {
    let cutList = stateList.filter( item => item.id > firstMessage - 1);
    cutList.map( item => {
        item.message = item.message.replace(/(\r\n|\n|\r)/gm, "");
        return true;
    })
     //delete empty string
    let list = cutList.filter( item => !(/^ *$/.test(item.message)) || item.type !== types.text);
    let chat = [];
    let countAllChildren = 0;
    list.map(i => countAllChildren += i.children.length);
    const lastIndex = list[list.length - 1].id;
    list.map( (item, index) => {
        switch (item.type) {
            case types.question:
            case types.answer:
            case types.text:
                if (item.children.length === 0) {
                    chat.push(`${item.id} ${item.message} -> ${item.nextId + 1}`);
                } else {
                    let childId = [],
                        childItems = [];
                    item.children.map(child => {
                        childId.push(child.id);
                        childItems.push(`${child.id} ${child.message} -> ${child.nextId + 1}`);
                    });
                    chat.push(`${item.id} ${item.message} [${childId}]`);
                    chat = chat.concat(childItems);
                }
                break;
  
            case types.cam:
            case types.collection:
            case types.map:
                chat.push(`${item.id} ||${item.type} -> ${item.nextId + 1}`);
                break;
  
            case types.image:
                chat.push(`${item.id} ||${types.image}${item.id} -> ${item.nextId+1}`);
                break;
  
            case types.exit:
                chat.push(`${item.id} ||${types.exit}`);
                break;
  
            default: 
                return true;
        }
        return true;
    });
    chat.push(`${firstMessage > 1 ? lastIndex + 1 : chat.length + 1} ||${types.exit}`);
    // chat should start from 1 id;
    if (firstMessage > 1) {
        const firstString = chat[0].split(' ');
        firstString.shift();
        chat[0] = '1 ' + firstString.join(' ');
    }
    //console.log(chat);
    return  chat.join('\n');
}

export const convertToList = (chat, isForChatPopup = false) => {
   let allMessages = chat.map(item => {
       if (item.children.length > 0) {
           return [item, item.children];
       } else {
           return item;
       }
   }).flat(2);

   const filteredMessages = isForChatPopup ? allMessages : moveSpecialToTheEnd(allMessages);
   const chatString = filteredMessages.map(item => {
        if (item === newLineChar) return;
        if (item.children.length > 0) {
        const nextIds = item.children.map((item) => `${chatIndex(item)}`).join(',');
        return `${chatIndex(item)} ${chatMessage(item)} [${nextIds}]`
    } else {
        if (item.type === types.exit || item.type === types.collection) {
            return `${chatIndex(item)} ${chatMessage(item)}`
        }

        const nextElement = allMessages.find((m )=> m.id === item.nextId+1);
        return `${chatIndex(item)} ${chatMessage(item)} -> ${chatIndex(nextElement)}`
    }
   }).join('\n');

   _imageCounter = 0;

   return chatString;
}

const moveSpecialToTheEnd = (array) => {
  const imageWithAnswers = (line) =>
    line.type === types.image && line.children.length;
  return array
    .filter((line) => line.type === types.text || imageWithAnswers(line))
    .concat(
      newLineChar,
      newLineChar,
      array.filter(
        (line) => line.type !== types.text && !imageWithAnswers(line)
      )
    );
};

export const getWrongSpecialLines = (stateList) => {
  const specialLineIsChild = (line) => line.isChild && line.type !== types.text;
  const specialLineWithChild = (line) =>
    line.type !== types.text && line.children.length;
  return stateList.filter(
    (line) => specialLineIsChild(line) || specialLineWithChild(line)
  );
};

const chatMessage = (item) => {
    switch(item.type) {
        case types.cam:
        case types.map:
        case types.collection:
        case types.exit:
            return `||${item.type}`
        case types.image:
            return `||${item.type}${_imageCounter++}`
        default:
            const message = item.message.split('->').join('- >').split('[').join('{').split(']').join('}');
            return `${message}`
    }
}

const chatIndex = (item) => {
    if (!item) return DIALOGUE_IDS_FOR_SPECIAL_ACTIONS.EXIT;
    switch(item.type) {
        case types.cam:
            return DIALOGUE_IDS_FOR_SPECIAL_ACTIONS.CAM;
        case types.map:
            return DIALOGUE_IDS_FOR_SPECIAL_ACTIONS.MAP;
        case types.collection:
            return DIALOGUE_IDS_FOR_SPECIAL_ACTIONS.COLLECTION;
        case types.exit:
            return DIALOGUE_IDS_FOR_SPECIAL_ACTIONS.EXIT;
        default:
            return item.id;
    }
}

export const parseUploadedChat = (stateList, firstMessage) => {
    let imageCount = 0;
    let cutList = stateList.filter(item => item.id > firstMessage - 1);
    cutList.map(item => {
        item.message = item.message.replace(/(\r\n|\n|\r)/gm, "");
        return true;
    });
    let chat = [];

    let list = cutList.filter( item => !(/^ *$/.test(item.message)) || item.type !== types.text);

    list.map(item => {
        switch(item.type) {
            case types.question:
            case types.answer:
            case types.text:
                if (item.children.length === 0 && !item.message.includes(types.exit)) {
                    chat.push(`${item.id} ${item.message} -> ${item.nextId + 1}`);
                } else if (item.message.includes(types.exit)) {
                    chat.push(`${item.id} ||${types.exit}`)
                } else {
                    let nextChildren = item.childrenId.map(id => id);
                    chat.push(`${item.id} ${item.message} [${nextChildren}]`);
                    item.children.map(child => {
                        chat.push(`${child.id} ${child.message} -> ${child.nextId + 1}`);
                        return true;
                    });
                }
                break;

            case types.cam:
            case types.collection:
            case types.map:
                chat.push(`${item.id} ||${item.type} -> ${item.nextId + 1}`);
                break;

            case types.image:
                chat.push(`${item.id} ||${types.image}${imageCount} -> ${item.nextId + 1}`);
                imageCount++;
                break;

            case types.exit:
                chat.push(`${item.id} ||${types.exit}`);
                break;

            default:
                break;
        }
        
        return true;
    });
    chat.push(`${chat.length + 1} ||${types.exit}`);
    // chat should start from 1 id;
    if (firstMessage > 1) {
        const firstString = chat[0].split(' ');
        firstString.shift();
        chat[0] = '1 ' + firstString.join(' ');
    }

    console.log(chat);

    return chat.join('\n');
}

export const convertToArray = (items) => {
    return items.map(i => {
        if (i.children.length > 0) {
            return [i, i.children];
        } else {
            return i;
        }
    }).flat(2);
}

export const insertElements = (item, items, beforeItems) => { 
    let elements = convertToArray(items);
    let beforeElements = convertToArray(beforeItems);

    const isCurrentElement = (element) => element.id == item.id

    let selectedId = item.id;
    let currentSelectedIndex = elements.findIndex(isCurrentElement) + beforeItems[0].id;
    let previousIndex = beforeElements.findIndex(isCurrentElement) + beforeItems[0].id;
    let currentIndex = currentSelectedIndex > previousIndex ? currentSelectedIndex + item.children.length : currentSelectedIndex;

    const isMovedBack = (id) => (id < previousIndex && id >= currentIndex);
    const isMovedForward = (id) => (id <= currentIndex && id > previousIndex);
    
    const isNeedToBeUpdatedId = (id) => currentIndex < previousIndex ? isMovedBack(id) : isMovedForward(id);
    const isNeedToBeUpdatedNextId = (id) => isNeedToBeUpdatedId(id) || ((isNeedToBeUpdatedId(id + 1) && elements.length > id));

    const updatedId = (id, s) => {
        if (isNeedToBeUpdatedId(id)) {
            return id + s;
        }
        return id;
    }

    const updatedLine = (line) => {
        if (line.id === selectedId) {
            return updatedSelectedItem(line);
        }

        let shift = currentIndex < previousIndex ? 1 + item.children.length : -(1 + item.children.length);
        line.id = updatedId(line.id, shift);
        line.nextId = isNeedToBeUpdatedNextId(line.nextId) ? line.nextId + shift : line.nextId;
        line.children = line.children.length > 0 ? line.children.map(c => {
           let item = updatedLine(c, shift)
           if (item.nextId + 1 <= line.id + line.children.length) {
               item.nextId = line.id + line.children.length;
           }
           return item;
        }) : [];

        // some weird action if line doesn't have next id
        if (!line.nextId && line.children.length == 0) {
            line.nextId = line.id;
        }
        
        return line;
    }

    const updatedSelectedItem = (e) => {
        e.id = currentSelectedIndex;
        let shift = currentIndex < previousIndex ? 1 + e.children.length : -(1 + e.children.length);
        e.nextId = updatedId(e.nextId + 1, shift) - 1;
        e.children = e.children.map (c => {
            // doesn't work for case if currentIndex > previousIndex
            c.id = currentSelectedIndex - previousIndex + c.id;
            if (c.nextId <= c.id) {
                c.nextId = c.nextId + currentSelectedIndex - previousIndex;
            }

            return c;
        })
        return e;
    }

    let updatedElements = items.map(e => {
        let line = updatedLine(e);
        return line;
    })
    return updatedElements;
}

export const insertElement = (item, items) => { 
  let selectedId = item.id;
  let elements = convertToArray(items);
  
  const isNeedToBeUpdatedId = (id) => (id >= selectedId);
  const updatedId = (id, shift) => {
      if (isNeedToBeUpdatedId(id)) {
          return id + shift;
      }
      return id;
  }

  const updatedLine = (line) => {
      let shift = 1;
      line.id = updatedId(line.id, shift);
      if((line.nextId + 1 >= selectedId && elements.length > line.nextId) || line.nextId >= selectedId) {
        line.nextId += shift;
      }
      line.children = line.children.length > 0 ? line.children.map(c => {
        let item = updatedLine(c, shift);
        if (item.nextId + 1 <= line.id + line.children.length) {
          item.nextId = line.id + line.children.length;
        }

        return item;
     }) : [];
      // some weird action if line doesn't have next id
      if (!line.nextId && line.children.length == 0) {
          line.nextId = line.id;
      }
      
      return line;
  }

  let updatedElements = items.map(e => {
      let line = updatedLine(e);
      return line;
  })
  return updatedElements;
}

export const deleteElement = (item, items, parent) => {
  let selectedId = item.id;
  let elements = convertToArray(items);
  const isNeedToBeUpdatedId = (id) => (id > selectedId);
  const updatedId = (id, shift) => {
    if (isNeedToBeUpdatedId(id)) {
      return id - shift;
    }
    return id;
  }

  const updatedLine = (line) => {
    let shift = 1 + item.children.length;
    line.id = updatedId(line.id, shift);
    if((line.nextId + 1 > selectedId && elements.length >= line.nextId) || line.nextId > selectedId) {
      line.nextId -= shift;
    }
    line.children = line.children.length > 0 ? line.children.map(c => {
      let item = updatedLine(c, shift);
      if (item.nextId + 1 <= line.id + line.children.length) {
        item.nextId = line.id + line.children.length;
      }
      return item
    }) : [];
    
    if (parent && parent.children.length === 0) {
      parent.nextId = parent.id;
    }

    return line;
  }

  let updatedElements = items.map(e => {
    let line = updatedLine(e);
    return line;
  });

  return updatedElements;
}

export const checkOnMaxChildren = (answer) => {
  const maxChildrenCount = 5;
  return answer.children && answer.children.length >= maxChildrenCount;
}
