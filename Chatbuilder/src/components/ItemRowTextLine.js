import React from 'react';
import DragIndicatorIcon from '@material-ui/icons/DragIndicator';
import ChatBubbleIcon from '@material-ui/icons/ChatBubble';
import QuestionAnswer from '@material-ui/icons/QuestionAnswer';
import AddIcon from '@material-ui/icons/Add';
import { Dropdown, FormControl } from 'react-bootstrap';
import { MenuLineChats } from './MenuLineChats';
import NextItems from './NextItems';
import PlayButton from './PlayButton';
import { connect } from 'react-redux';
import {
  changeType,
  changeTextInput,
  deleteItem,
  addItem,
  setFocusedLine
} from '../actions/builder';
import { MenuAnswer } from './MenuAnswer';
import { convertToArray } from '../services/parse';
import { types } from './constants/types';

const color = {
  green: '#99ff99',
  lightGreen: '#ccffcc'
}
class ItemRowTextLine extends React.Component {
  componentDidUpdate(prevProps) {
    const { addedElement } = this.props;
    const { addedElement: prevAdded } = prevProps;

    if (addedElement && addedElement !== prevAdded) {
      document.getElementById(`inputField ${addedElement.id}`).focus();
      const allLines = document.getElementsByClassName('itemWrapper');
      for (let i = 0; i < allLines.length; i ++) {
        allLines[i].style.background = '#ffffff';
      }
      this.setHighlightLines(addedElement.id);
    }
  }

  get isFirefox() {
    return navigator.userAgent.search(/Firefox/) > 0;
  };

  setCursorToEnd = ({ target:textarea }) =>
    textarea.selectionStart = textarea.selectionEnd = textarea.value.length;

  removeDraggable = (event, item) => {
    const { setFocusedLine } = this.props;
    this.setHighlightLines(item.id);
    setFocusedLine(item);
    if (this.isFirefox) {
      this.setCursorToEnd(event);
      const draggChild = event.target.closest(".itemWrapper");
      draggChild.parentNode.removeAttribute("draggable");
    }
  };

  setDraggable = (event) => {
    const allLines = document.getElementsByClassName('itemWrapper');
      for (let i = 0; i < allLines.length; i ++) {
        allLines[i].style.background = '#ffffff';
      }
    if (this.isFirefox) {
      const draggChild = event.target.closest(".itemWrapper");
      draggChild.parentNode.setAttribute("draggable", "true");
    }
  };

  setHighlightLines = (id) => {
    const { listOfBlocks } = this.props;
    const oneListOfBlocks = convertToArray(listOfBlocks);
    const item = oneListOfBlocks.find((item) => item.id === id);
    this.setHtmlColor(item, color.green);
    const nextElem = oneListOfBlocks.find((el) => el.id === item.nextId + 1);
    const prevElems = oneListOfBlocks.filter((el) => item.id === el.nextId + 1);
    if (item.children.length) {
      item.children.map((child) => this.setHtmlColor(child, color.lightGreen));
    }
    if (nextElem) {
      this.setHtmlColor(nextElem, color.lightGreen);
    }
    if (prevElems.length && !item.isChild) {
      prevElems.map((el) => {
        if (el.type !== types.exit && el.type !== types.collection) {
          return this.setHtmlColor(el, color.lightGreen);
        }
      });
    }
  };

  setHtmlColor = (item, color) => {
    const htmlItem = document.getElementById(`itemWrapper ${item.id}`);
    htmlItem.style.background = color;
  };

  addNewItem(item) {
    const { listOfBlocks, addItem, onMaxChildren } = this.props;
    if (item.isChild) {
      const parent = listOfBlocks
        .filter(el => el.children.find(child => child.id === item.id))[0];
      parent.children.length > 4 ? onMaxChildren() : addItem(item.id, item, parent);
    } else {
      addItem(item.id, item);
    };
  };
  
  deleteLine = (item) => {
    const { setFocusedLine, deleteItem } = this.props;
    setFocusedLine(null);
    deleteItem(item);
  };

  render() {
    const {
      item,
      index,
      changeTextInput,
      changeType,
      deleteItem,
      itemsCount
    } = this.props;
    return (
      <>
        <div className="infoWrapper">
          <DragIndicatorIcon style={{cursor: 'grab', fontSize: 32, width: '30px'}} />
          <div className="idWrapper">
            <div className="linesId">
              {item.id}
            </div>
            <Dropdown>
              <Dropdown.Toggle variant="primary" id="dropdown-basic">
                <ChatBubbleIcon />
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
        <div className="contentWrapper" style={{ width: 'calc(1280px-160px)'}}>
          <FormControl
            id={`inputField ${item.id}`}
            as="textarea"
            rows="2"
            value={item.message}
            type="text"
            className="itemRowTextarea"
            onFocus = {(e) => this.removeDraggable(e, item)}
            onBlur = {this.setDraggable}
            onChange={(e) => changeTextInput(e.target.value, index, item)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.ctrlKey) {
                e.preventDefault();
                this.addNewItem(item)
              } else if (e.key === 'Enter' && e.ctrlKey) {
                return changeTextInput(e.target.value + '\n', index, item)
              }
            }}
          />
        </div>
        <PlayButton item={item} />
        <div className="nextIdWrapper">
          <NextItems item={item} />
        </div>
        <AddIcon
          onClick={() => {
            this.deleteLine(item)
          }}
          className="deleteIcon"
        />
      </>
    )
  }
}

const mapStateToProps = (state) => {
  return {
    focusId: state.builder.focusId,
    addedElement: state.builder.addedElement
  }
}

export default connect(
mapStateToProps, {
  changeType,
  changeTextInput,
  deleteItem,
  addItem,
  setFocusedLine
})(ItemRowTextLine);
