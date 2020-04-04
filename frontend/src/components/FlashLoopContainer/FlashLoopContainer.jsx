import React from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router";
import { connect } from "react-redux";
import { fetchLoop } from "../../actions/loop";
import FlashLoop from "../FlashLoop";
import LoopNav from "../LoopNav";
import NotFound from "../NotFound";

class FlashLoopContainer extends React.Component {
    componentDidMount() {
        const { match, fetchLoopData } = this.props;
        fetchLoopData(match.params.id);
    }

    render() {
        const { loop, next, prev } = this.props;

        if (loop === null) {
            return <NotFound />;
        }

        return (
            <div className="loop-container">
                <FlashLoop loop={loop} />
                <LoopNav next={next} previous={prev} />
            </div>
        );
    }
}

FlashLoopContainer.propTypes = {
    fetchLoopData: PropTypes.func.isRequired,
    loop: PropTypes.object,
    next: PropTypes.number,
    prev: PropTypes.number,
    match: PropTypes.object.isRequired,
};

FlashLoopContainer.defaultProps = {
    loop: null,
    next: null,
    prev: null,
};

const mapStateToProps = state => ({
    loop: state.loop.current,
    next: state.loop.next,
    prev: state.loop.previous,
});

const mapDispatchToProps = dispatch => ({
    fetchLoopData: id => dispatch(fetchLoop(id)),
});

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(FlashLoopContainer));
