import React from "react";
import "../styles/builderStyle.css";
import { connect } from "react-redux";
import {
  addItem,
  sortList,
  saveToClipboard,
  resetAll,
  uploadChat,
  changeAlertState,
  changeWrongLinesState
} from "../actions/builder";
import Nestable from "react-nestable";
import ItemRow from "../components/ItemRow";
import Alert from "@material-ui/lab/Alert";
import Chat from "./Chat";
import ModalConfirmWindow from "../components/ModalConfirmWindow";
import { types } from "../components/constants/types";
import { convertToArray, getWrongSpecialLines } from '../services/parse';
import Snackbar from '@material-ui/core/Snackbar';

const snackOpt = {
  vertical: 'top', 
  horizontal: 'center',
  hideDuration: 5000
}

class Builder extends React.Component {
  uploadChat = React.createRef();
  interval = 0;
  isStopScrollUp = true;
  isStopScrollDown = true;

  componentDidMount() {
    window.onbeforeunload = () => true;
    document.addEventListener("mousedown", this.handleMousedown);
  }

  componentWillUnmount() {
    document.removeEventListener("mousedown", this.handleMousedown);
  }

  state = {
    isVisibleWarning: false,
    isVisibleSuccess: false,
    isMaxChildren: false,
    isModalShow: false,
    isWrongType: false,
    emptyLineIds: '',
    wrongFileIds: ''
  };

  handleAlertWarning = () =>
    this.setState({ isVisibleWarning: !this.state.isVisibleWarning });

  handleAlertSuccess = () =>
    this.setState({ isVisibleSuccess: !this.state.isVisibleSuccess });

  handleAlertMaxChildren = () => this.setState({ isMaxChildren: true });

  handleFileWrong = (boolean = true) => this.setState({ isWrongType: boolean })

  handleWrongSpecialLines = () => {
    this.props.changeWrongLinesState();
    this.setState({ wrongFileIds: "" });
  }

  changeWindowState = () =>
    this.setState({ isModalShow: !this.state.isModalShow });

  resetAllProgress = () => {
    this.props.resetAll();
    this.changeWindowState();
  };

  handleMousedown = (e) => {
    if (e.which !== 1) {
      return;
    }
    const draggableItem = e.target.closest(".itemWrapper");

    if (draggableItem) {
      document.addEventListener("mousemove", this.handleMousemove);
      document.addEventListener("mouseup", this.stopScrolling);
    }
  };

  handleMousemove = (e) => {
    const screenHeight = window.innerHeight;
    const step = 300;
    if (e.clientY < 180) {
      this.isStopScrollUp = false;
      this.interval = setInterval(() => {
        if (!this.isStopScrollUp) {
          window.scrollBy({ top: -step, behavior: "smooth" });
        }
      }, 0);
    }
    if (e.clientY >= screenHeight) {
      this.isStopScrollDown = false;
      this.interval = setInterval(() => {
        if (!this.isStopScrollDown) {
          window.scrollBy({ top: step, behavior: "smooth" });
        }
      }, 0);
    }
    if (e.clientY > 180 && e.clientY < screenHeight) {
      this.isStopScrollUp = true;
      this.isStopScrollDown = true;
    }
    document.addEventListener("mouseup", this.stopScrolling);
  };

  stopScrolling = () => {
    this.isStopScrollUp = true;
    this.isStopScrollDown = true;
    clearInterval(this.interval);
    document.removeEventListener("mousemove", this.handleMousemove);
    document.removeEventListener("mouseup", this.stopScrolling);
  };

  get renderAlert() {
    const {
      isVisibleWarning,
      isVisibleSuccess,
      isMaxChildren,
      isWrongType,
      emptyLineIds,
      wrongFileIds,
    } = this.state;
    const {
      isIncorrectFile,
      errorMessage,
      changeAlertState,
      wrongChatLinesIds,
    } = this.props;
    if (isVisibleWarning) {
      return (
        <Snackbar 
          anchorOrigin={{ vertical: snackOpt.vertical, horizontal: snackOpt.horizontal }} 
          open={isVisibleWarning} 
          autoHideDuration={snackOpt.hideDuration} 
          onClose={this.handleAlertWarning}
        >
          <Alert onClose={this.handleAlertWarning} severity="warning">
             All ids was changed!
          </Alert>
        </Snackbar>
      );
    } else if (isVisibleSuccess) {
      return (
        <Snackbar 
          anchorOrigin={{ vertical: snackOpt.vertical, horizontal: snackOpt.horizontal }} 
          autoHideDuration={snackOpt.hideDuration} 
          open={isVisibleSuccess} 
          onClose={this.handleAlertSuccess}
        >
          <Alert onClose={this.handleAlertSuccess} severity="success">
            Chat was saved!
          </Alert>
        </Snackbar>
      );
    } else if (isMaxChildren) {
      return (
        <Alert
         severity="error"
         className="alert"
         onClose={() => this.setState({ isMaxChildren: false })}
         >
          You can't add more elements!
        </Alert>
      );
    } else if (isIncorrectFile) {
      return (
        <Alert 
          severity="error" 
          className="alert" 
          onClose={changeAlertState}
        >
          <p>File is invalid!</p>
          {errorMessage}
        </Alert>
      )
    } else if (isWrongType) {
      return (
        <Alert 
          severity="error" 
          className="alert" 
          onClose={() => this.handleFileWrong(false)}
        >
          <p>You are trying to load the wrong file format</p>
        </Alert>
      )
    } else if (emptyLineIds) {
      return (
        <Alert 
          severity="error" 
          className="alert" 
          onClose={() => this.setState({ emptyLineIds: '' })}
        >
          <p>Fill in or delete empty line(s): {emptyLineIds}</p>
        </Alert>
      )
    } else if (wrongFileIds || wrongChatLinesIds) {
      return (
        <Alert
          severity="error"
          className="alert"
          onClose={this.handleWrongSpecialLines}
        >
          <p>Special line(s): {wrongFileIds || wrongChatLinesIds} can't be answer(s) or can't have answer(s)</p>
        </Alert>
      );
    } else {
      return null;
    }
  }

  renderItem = ({ item, index }) => (
    <ItemRow
      item = { item }
      index = { index }
      onMaxChildren = { this.handleAlertMaxChildren }
      handleFileWrong = {this.handleFileWrong}
    />
  );

  isFileTxt = (file) => /(\.txt)$/.test(file);

  readChatFromFile = (e) => {
    e.preventDefault();
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = async (e) => {
      const text = e.target.result;
      this.props.uploadChat(text);
    };
    if (file) {
      this.isFileTxt(file.name)
        ? reader.readAsText(file)
        : this.handleFileWrong(true);
    }
  };

  addLine = () => {
    const { builder: { focusedItem, listOfBlocks }, addItem } = this.props;
    const oneListOfBlocks = convertToArray(listOfBlocks);
    const item = oneListOfBlocks.find(item => item.id === focusedItem?.id)
    if(!focusedItem || item?.type !== types.text){
      return addItem();
    }
    if (item.isChild) {
      const parent = listOfBlocks
        .filter(el => el.children.find(child => child.id === item.id))[0];
      parent.children.length <= 4 ? addItem(focusedItem.id, item, parent) : addItem();
    } else {
      addItem(item.id, item);
    };
  };

  onSaveClick = () => {
    const {
      builder: { listOfBlocks },
      saveToClipboard,
    } = this.props;
    const oneList = convertToArray(listOfBlocks);
    const oneListOfTextBlocks = oneList.filter(
      (item) => item.type === types.text
    );
    const emptyLineIds = oneListOfTextBlocks
      .filter((item) => !item.message.trim())
      .map((line) => line.id);
    const wrongLinesList = getWrongSpecialLines(oneList).map(
      (line) => line.id
    );

    if (emptyLineIds.length) {
      return this.setState({ emptyLineIds: emptyLineIds.join(",") });
    }
    if (wrongLinesList.length) {
      return this.setState({ wrongFileIds: wrongLinesList.join(",") });
    }
    this.handleAlertSuccess();
    saveToClipboard();
  };
 
  get renderHeader() {
    const { builder: { listOfBlocks } } = this.props;
    
    return (
      <div className="header">
        <div className="header-content">
          <div className="title-wrapper">
            <img src={require("../images/logo.jpg")} className='title-wrapper__logo' alt="title-logo"/>
            <h1 className="title-wrapper__title">Chat Builder</h1>
          </div>
          <div className="buttonWrapper">
            <button className="addButton" onClick={this.addLine}>
              Add New Line
            </button>
            <input
              type="file"
              id="uploadChat"
              ref={this.uploadChat}
              onChange={(e) => this.readChatFromFile(e)}
              className="uploadButton"
            />
            <button
              className="uploadChatButton"
              onClick={() => this.uploadChat.current.click()}
            >
              Upload chat
            </button>
            <button onClick={this.changeWindowState} className="resetButton">
              Reset
            </button>
            <ModalConfirmWindow
              show={this.state.isModalShow}
              confirm={this.resetAllProgress}
              onHide={this.changeWindowState}
            />
            <button
              disabled={listOfBlocks.length === 0}
              onClick={this.onSaveClick}
              className="saveButton"
            >
              Save
            </button>
          </div>
        </div>
      </div>
    );
  }

  render() {
    const { listOfBlocks } = this.props.builder;
    return (
      <div className="builderWrapper">
        {this.renderAlert}
        {this.renderHeader}
        <Nestable
          maxDepth={2}
          items={listOfBlocks}
          renderItem={this.renderItem}
          onChange={(items, item) => {
            if (this.props.builder.isCustomId) {
              this.handleAlertWarning();
            }
            this.props.sortList(items, item);
          }}
          confirmChange={(dragItem, destinationParent) => {
            if (destinationParent) {
              dragItem.isChild = true;
              if (destinationParent.children.length > 4) {
                return false;
              }
              return true;
            } else {
              dragItem.isChild = false;
              return true;
            }
          }}
          className="nestableWrapper"
        />
        <Chat />
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  return {
    builder: state.builder,
    isError: state.builder.isError,
    isIncorrectFile: state.builder.isIncorrectFile,
    errorMessage: state.builder.errorMessage,
    wrongChatLinesIds: state.builder.wrongChatLinesIds
  };
};

export default connect(mapStateToProps, {
  addItem,
  sortList,
  saveToClipboard,
  resetAll,
  uploadChat,
  changeAlertState,
  changeWrongLinesState
})(Builder);
