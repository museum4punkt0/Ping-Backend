import React from 'react';
import MapIcon from '@material-ui/icons/Map';
import CameraIcon from '@material-ui/icons/Camera';
import CollectionsIcon from '@material-ui/icons/Collections';
import DragIndicatorIcon from '@material-ui/icons/DragIndicator';
import QuestionAnswer from '@material-ui/icons/QuestionAnswer';
import AddIcon from '@material-ui/icons/Add';
import { Dropdown } from 'react-bootstrap';
import { MenuLineChats } from './MenuLineChats';
import NextItems from './NextItems';
import PlayButton from './PlayButton';
import { types } from './constants/types';
import { MenuAnswer } from './MenuAnswer';

const renderIcon = (item) => {
  switch(item.type) {
    case types.map:
      return <MapIcon />;
    case types.cam:
      return <CameraIcon />;
    case types.collection:
      return <CollectionsIcon />;
    default:
      return;
  }
}

export const ItemRowSpecial = ({ 
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
            {renderIcon(item)}
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
    {item.type !== 'Collection' && (
      <>
        <div className="contentWrapper" />
          <PlayButton item={item} />
        <div className="nextIdWrapper">
          <NextItems item={item} />
        </div>
      </> 
    )}
 
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