import React from 'react';
import ExitToApp from '@material-ui/icons/ExitToApp';
import DragIndicatorIcon from '@material-ui/icons/DragIndicator';
import QuestionAnswer from '@material-ui/icons/QuestionAnswer';
import AddIcon from '@material-ui/icons/Add';
import { Dropdown } from 'react-bootstrap';
import { MenuLineChats } from './MenuLineChats';
import { MenuAnswer } from './MenuAnswer';

export const ItemRowExit = ({ 
  item, 
  index, 
  changeType, 
  deleteItem,
  itemsCount
}) => (
  <>
    <div className="infoWrapper">
      <DragIndicatorIcon style={{cursor: 'grab', fontSize: 32, width: '30px'}} />
      <div className="idWrapper">
        <div className="linesId">
          {item.id}
        </div>
        <Dropdown>
          <Dropdown.Toggle variant="primary" id="dropdown-basic">
            <ExitToApp />
          </Dropdown.Toggle>
          <MenuLineChats changeType={changeType} index={index} item={item} />
        </Dropdown>
        <Dropdown>
          <Dropdown.Toggle variant="primary" id="dropdown-basic" disabled={item.children.length || itemsCount <= 1}>
            <QuestionAnswer />
          </Dropdown.Toggle>
          <MenuAnswer changeType={changeType} index={index} item={item} />
        </Dropdown>
      </div>
    </div>
    <div className="contentWrapper" />
    <AddIcon 
       onClick={() => {
        deleteItem(item);
        // let nestableLines = document.getElementsByClassName(`nestable-item-${item.id}`);
        // nestableLines[0].classList.add('deleteNestableItem');
        // setTimeout( () => deleteItem(item.id), 200)
      }}
      className="deleteIcon"
    />
  </>
)