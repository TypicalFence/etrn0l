import React from "react";
import PropTypes from "prop-types";

const FlashLoop = ({ loop }) => <h1>{loop.number}</h1>;

FlashLoop.propTypes = {
    loop: PropTypes.object.isRequired,
};

export default FlashLoop;
