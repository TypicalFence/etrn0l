import React from "react";
import PropTypes from "prop-types";
import RuffleObject from "../../../vendor/ruffle/web/js-src/ruffle-object";
import { register_element } from "../../../vendor/ruffle/web/js-src/register-element";

register_element("ruffle-object", RuffleObject);

const FlashLoop = ({ loop }) => {
    if (loop.file_url) {
        return <ruffle-object data={loop.file_url} />;
    }

    return <h1>OH NO!</h1>;
};

FlashLoop.propTypes = {
    loop: PropTypes.object.isRequired,
};

export default FlashLoop;
