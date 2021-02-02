import React from 'react';
import { Dropdown } from 'react-bootstrap';
import { setNewNextId } from '../actions/builder';
import { connect } from 'react-redux';

class NextItems extends React.Component {

  get countOfElements() {
    const { builder: { listOfBlocks } } = this.props;
    const countOfChildren = listOfBlocks.filter(block => block.children.length).length;
    return countOfChildren + listOfBlocks.length;
  }

  render() {
    const {item} = this.props;

    if (item.children.length === 0) {
      return <Dropdown>
        <Dropdown.Toggle 
          variant="primary" 
          id="dropdown-basic"
          disabled = {this.countOfElements <= 1 }
          style= {{cursor: this.countOfElements <= 1 ? 'auto' : 'pointer'}}
        >
          {item.nextId + 1}
        </Dropdown.Toggle>
        <Dropdown.Menu
          style={{
            maxHeight: '200px',
            overflow: 'auto'
          }}>
          {this.props.builder.listOfBlocks.filter( i => i.id !== item.id).map( filterItem => (
           <Dropdown.Item
             className="dropdownItem"
             key = {item.id}
             onClick={() => this.props.setNewNextId(filterItem.id, item)}
           >
             {filterItem.id} - {filterItem.message}
           </Dropdown.Item>
          ))}
        </Dropdown.Menu>
      </Dropdown>
    } else {
      return item.children.map(child => (
        <div
          key={child.id}
          className="linesId"
          style={{ marginLeft: '8px'}}>
          {child.id}
        </div>
      ))
    }
  }
}

const mapStateToProps = (state) => {
  return {
    builder: state.builder
  }
}


export default connect(mapStateToProps, { setNewNextId})(NextItems);
