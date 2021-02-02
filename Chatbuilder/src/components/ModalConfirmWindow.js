import React from "react";
import { Modal, Button } from "react-bootstrap";

export default ({show, confirm, onHide}) => (
  <Modal show={show} size="lg">
    <Modal.Header closeButton onClick={onHide}>
      <Modal.Title>
        <h5>
          Do you really want to reset the chat builder and delete every unsaved
          progress?
        </h5>
      </Modal.Title>
    </Modal.Header>
    <Modal.Footer>
      <Button variant="danger" onClick={confirm}>
        Yes
      </Button>
      <Button variant="primary" onClick={onHide}>
        Cancel
      </Button>
    </Modal.Footer>
  </Modal>
);

