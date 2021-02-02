
export const getLocalization = (object, lang, key = 'title') => {
    let result = null;
    let array = object || [];
    if(typeof object === 'object') array = Array.from(object);
    const localization = array.find(item => item.language === lang)
    if(localization) return localization[key];
    if(array[0]) result = array[0][key];
    return result;
};

export const calculateMessageDelay = (message = '', minimumDelay, divider = 4) => {
    // calculate delay to show the next messages (reading delay)
    const wordCount = message.split(' ').length;
    const messageDelay = (wordCount / divider * 1000) < minimumDelay ? minimumDelay : (wordCount / divider * 1000);
    return messageDelay;
}

export const updateArrayItem = (array, item, key = 'sync_id') => {
    const result = [...array];
    const index = result.findIndex(i => i[key] === item[key]);
    if(index !== -1) result[index] = {...result[index], ...item};
    return result;
  };

export const deletingMain = (list, removedItem) => {
    return list.map((item, index) => {
        let updateChildren = [];
        if (item.id > removedItem.id) {
            if (item.children.length > 0) {
                updateChildren = item.children.map(child =>  {
                    return {
                        ...child,
                        id: child.id - removedItem.children.length - 1,
                        nextId: child.nextId - removedItem.children.length - 1,
                    }
                });
            }
            return {
                ...item,
                id: item.id - removedItem.children.length - 1,
                nextId: !item.isCustomNextId ? item.nextId - removedItem.children.length - 1 : item.nextId > removedItem.id ? item.nextId - removedItem.children.length - 1 : item.nextId,
                children: updateChildren,
            };
        } else if (item.id < removedItem.id) {
            if (item.children.length > 0) {
                updateChildren = item.children.map(child =>  {
                    return {
                        ...child,
                        nextId: child.isCustomNextId && child.nextId >= removedItem.id ? child.nextId - 1 : child.nextId,
                    }
                });
            }
            return {
                ...item,
                id: item.id,
                nextId: !item.isCustomNextId ? item.nextId : item.nextId >= removedItem.id ? item.nextId - 1 : item.nextId,
                children: updateChildren,
            };
        }
        return item;
    });
}

export const deletingChildren = (list, removedItem, parentIndex) => {
     const updateChildren = list[parentIndex].children.map(child => {
        if (child.id > removedItem) {
            return {
                ...child,
                id: child.id - 1,
                nextId: child.nextId - 1,
            };
        }
        return {
            ...child,
            nextId: child.nextId - 1,
        };
    });

    list[parentIndex].children = updateChildren;

   return list.map((item, index) => {
       if (index > parentIndex) {
            let updateChildren = [];
            if (item.children.length > 0) {
                updateChildren = item.children.map(child =>  {
                    return {
                        ...child,
                        id: child.id - 1,
                        nextId: child.nextId - 1,
                    }
                });
            }
            return {
                ...item,
                id: item.id - 1,
                nextId: !item.isCustomNextId ? item.nextId - 1 : item.nextId > list[parentIndex].id ? item.nextId - 1 : item.nextId,
                children: updateChildren,
            };
       }
       return item;
   });
}

export const addingMain = (list, newElementId, index, actionId) => {
    return list.map((item, id) => {
        let updateChildrenList = [];
        if (item.id >= newElementId && index !== undefined && id !== index + 1) {
            if (item.children.length > 0) {
                updateChildrenList = item.children.map(child =>  {
                    return {
                        ...child,
                        id: child.id + 1,
                        nextId: child.nextId + 1,
                    }
                });
            }
            return {
                ...item,
                id: item.id + 1,
                nextId: !item.isCustomNextId ? item.nextId + 1 : item.nextId > actionId ? item.nextId + 1 : item.nextId,
                children: updateChildrenList,
            };
        } else if (item.id < newElementId) {
            console.log(actionId);
            if (item.children.length > 0) {
                updateChildrenList = item.children.map(child =>  {
                    return {
                        ...child,
                        nextId: child.isCustomNextId && child.nextId >= newElementId - 1 ? child.nextId + 1 : child.nextId,
                    }
                });
            }
            return {
                ...item,
                nextId: !item.isCustomNextId ? item.nextId : item.nextId >= actionId ? item.nextId + 1 : item.nextId,
                children: updateChildrenList,
            };
        }
        return item;
    });
}

export const addingChildren = (list, parentBlock, newElementId, index, actionId) => {
    const parentIndex = list.map(i => i.id).indexOf(parentBlock.id);

    const updatedChildrenList = parentBlock.children.map((child, childIndex) => {
        if (child.id >= newElementId && index !== undefined && childIndex !== index + 1) {
            return {
                ...child,
                id: child.id + 1,
                nextId: child.isCustomId ? child.nextId + 1 : parentBlock.id + parentBlock.children.length,
            };
        }
        return {
            ...child,
            nextId: child.isCustomId ? child.nextId + 1 : parentBlock.id + parentBlock.children.length,
        };
    });
    list[parentIndex].children = updatedChildrenList;

    return list.map((item, id) => {
        if (item.id > parentBlock.id) {
            return {
                ...item,
                id: item.id + 1,
                nextId: !item.isCustomNextId ? item.nextId + 1 : item.nextId > actionId ? item.nextId + 1 : item.nextId,
            };
        } else if (item.id < parentBlock.id) {
            return {
                ...item,
                nextId: !item.isCustomNextId ? item.nextId : item.nextId > actionId ? item.nextId + 1 : item.nextId,
            };
        }
        return item;
    });
}