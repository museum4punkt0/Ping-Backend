import React from 'react';
import ImageIcon from '@material-ui/icons/Image';
import DragIndicatorIcon from '@material-ui/icons/DragIndicator';
import QuestionAnswer from '@material-ui/icons/QuestionAnswer';
import AddIcon from '@material-ui/icons/Add';
import { Dropdown } from 'react-bootstrap';
import { MenuLineChats } from './MenuLineChats';
import NextItems from './NextItems';
import PlayButton from './PlayButton';
import { MenuAnswer } from './MenuAnswer';

export const ItemRowImage = ({ 
  item, 
  index, 
  handleImageChange, 
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
            <ImageIcon />
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
    <div className="imageWrapper">
      <input 
        className="fileInput"
        type="file" 
        id={`files${index}`}
        onChange={(e) => handleImageChange(e,index, item)}
      />
      <button 
        className="uploadImage"
        onClick={ () => {
          document.getElementById(`files${index}`).click()
        }}>
        Choose file
      </button>
      <label>
        {item.image.name ? item.image.name : "No file chosen"}
      </label>
    </div>
    <PlayButton item={item} />
    <div className="nextIdWrapper">
      <NextItems item={item} />
    </div>
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