import React from "react";
import PlayArrowIcon from "@material-ui/icons/PlayArrow";
import FastRewindIcon from "@material-ui/icons/FastRewind";
import { connect } from "react-redux";
import { parseChatFrom, checkChatSpecialLines } from "../actions/builder";
import { handleVisibleChat } from "../actions/chats";
class PlayButton extends React.Component {
  render() {
    const { item, checkChatSpecialLines } = this.props;
    if (item.children.length > 0) {
      return (
        <FastRewindIcon
          onClick={() => checkChatSpecialLines(item)}
          className="playButton"
          style={{ transform: "rotate(180deg)" }}
        />
      );
    } else {
      return (
        <PlayArrowIcon
          onClick={() => checkChatSpecialLines(item)}
          className="playButton"
        />
      );
    }
  }
}

const mapStateToProps = (state) => {
  return {
    builder: state.builder,
    wrongChatLinesIds: state.builder.wrongChatLinesIds,
  };
};

export default connect(mapStateToProps, {
  parseChatFrom,
  handleVisibleChat,
  checkChatSpecialLines,
})(PlayButton);
