import React from "react";
import { types } from "./constants/types";
import { Dropdown } from "react-bootstrap";

export const MenuAnswer = ({ index, changeType, item }) => (
  <Dropdown.Menu>
    {item.isChild && (
      <Dropdown.Item
        href="#/action-7"
        onClick={() => changeType(index, item, types.question)}
      >
        Question
      </Dropdown.Item>
    )}
    {!item.isChild && (
      <Dropdown.Item
        href="#/action-8"
        onClick={() => changeType(index, item, types.answer)}
      >
        Answer
      </Dropdown.Item>
    )}
  </Dropdown.Menu>
);
