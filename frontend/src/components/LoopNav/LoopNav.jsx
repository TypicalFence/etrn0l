import React from "react";
import PropTypes from "prop-types";
import { connect } from "react-redux";
import { gotToLoop, goToRandomLoop } from "../../actions/loop";

const LoopNav = ({
    next,
    previous,
    changeToLoop,
    changeToRandomLoop,
}) => {
    let nextLink = null;
    let previousLink = null;
    const nextClick = () => changeToLoop(next);
    const previousClick = () => changeToLoop(previous);

    if (next !== null) {
        nextLink = <span role="button" onClick={nextClick}>next</span>;
    }

    if (previous !== null) {
        previousLink = <span role="button" onClick={previousClick}>previous</span>;
    }

    return (
        <div className="loop-nav">
            {previousLink}
            <span role="button" onClick={() => changeToRandomLoop()}>random</span>
            {nextLink}
        </div>
    );
};

LoopNav.propTypes = {
    next: PropTypes.number,
    previous: PropTypes.number,
    changeToLoop: PropTypes.func.isRequired,
    changeToRandomLoop: PropTypes.func.isRequired,
};

LoopNav.defaultProps = {
    next: null,
    previous: null,
};

const mapDispatchToProps = dispatch => ({
    changeToLoop: id => dispatch(gotToLoop(id)),
    changeToRandomLoop: () => dispatch(goToRandomLoop()),
});

export default connect(null, mapDispatchToProps)(LoopNav);
