import React from 'react';
import { connect } from 'react-redux';
import {
  changeType,
  changeTextInput,
  saveImage,
  deleteItem,
  addItem,
  setNewNextId
} from '../actions/builder';
import { types } from './constants/types';
import ItemRowTextLine from './ItemRowTextLine';
import { ItemRowImage } from './ItemRowImage';
import {ItemRowExit} from './ItemRowExit';
import { ItemRowSpecial } from './ItemRowSpecial';

class ItemRow extends React.Component {

  componentDidMount() {
    document.addEventListener('click', this.handleClickOutside);
  }

  componentWillUnmount() {
    document.removeEventListener('click', this.handleClickOutside);
  }

  handleClickOutside = (event) => {
    const { index } = this.props;

    if (event.target.closest(`.typeWrapper${index}`)) return;
    this.setState({
      isVisible: false,
    });
  };

  isFileImg = (file) => /(\.png|\.jpe?g)$/.test(file);

  handleImageChange = (e, index, item) => {
    const { handleFileWrong } = this.props;
    let reader = new FileReader();
    let file = e.target.files[0];

    reader.onloadend = () => {
      this.props.saveImage(file, index, item);
    };
    if (file) {
      this.isFileImg(file.name.toLowerCase())
        ? reader.readAsDataURL(file)
        : handleFileWrong();
    }
  };

  get countOfElements() {
    const { builder: { listOfBlocks } } = this.props;
    const countOfChildren = listOfBlocks.filter(block => block.children.length).length;
    return countOfChildren + listOfBlocks.length;
  }

  renderContent = (item, index, listOfBlocks, onMaxChildren) => {
    switch (item.type) {
      case types.question:
      case types.answer:
      case types.text:
        return <ItemRowTextLine
          key={item.id}
          item={item}
          index={index}
          listOfBlocks={listOfBlocks}
          onMaxChildren = {onMaxChildren}
          itemsCount = {this.countOfElements}
        />

      case types.collection:
      case types.cam:
      case types.map:
        return <ItemRowSpecial
          key={item.id}
          item={item}
          index={index}
          changeType={this.props.changeType}
          deleteItem={this.props.deleteItem}
          itemsCount = {this.countOfElements}
        />

      case types.image:
        return <ItemRowImage
          key={item.id}
          item={item}
          index={index}
          handleImageChange={this.handleImageChange}
          changeType={this.props.changeType}
          deleteItem={this.props.deleteItem}
          itemsCount = {this.countOfElements}
        />

      case types.exit:
        return <ItemRowExit
          key={item.id}
          item={item}
          index={index}
          changeType={this.props.changeType}
          deleteItem={this.props.deleteItem}
          itemsCount = {this.countOfElements}
        />
      default:
        return;
    }
  }

  render() {
    const { item, index, builder: { listOfBlocks }, onMaxChildren } = this.props;
    return(
      <div className={`itemWrapper ${item.id}`} key={item.id} id={`itemWrapper ${item.id}`} >
        {this.renderContent(item, index, listOfBlocks, onMaxChildren)}
      </div>
    )
  }
}

const mapStateToProps = (state) => {
    return {
      builder: state.builder
    }
  }

export default connect(
  mapStateToProps, {
    changeType,
    changeTextInput,
    saveImage,
    deleteItem,
    addItem,
    setNewNextId,
  })(ItemRow);
