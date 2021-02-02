import React from 'react';
import { types } from './constants/types';
import { Dropdown } from 'react-bootstrap';

export const MenuLineChats = ({ index, changeType, item }) => (
  <Dropdown.Menu>
    <Dropdown.Item 
      href="#/action-1"
      onClick={() => changeType(index, item, types.text)}>
      Text
    </Dropdown.Item>
    <Dropdown.Item 
      href="#/action-2"
      onClick={() => changeType(index, item, types.image)}>
      Image
    </Dropdown.Item>
    <Dropdown.Item 
      href="#/action-3"
      onClick={() => changeType(index, item, types.map)}>
      Map
    </Dropdown.Item>
    <Dropdown.Item 
      href="#/action-4"
      onClick={() => changeType(index, item, types.cam)}>
      Cam
    </Dropdown.Item>
    <Dropdown.Item 
      href="#/action-5"
      onClick={() => changeType(index, item, types.collection)}>
      Collection
    </Dropdown.Item>
    <Dropdown.Item 
      href="#/action-6"
      onClick={() => changeType(index, item, types.exit)}>
      Exit
    </Dropdown.Item>
  </Dropdown.Menu>
)