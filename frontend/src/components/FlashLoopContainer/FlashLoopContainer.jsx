import React from "react";
import PropTypes from "prop-types";
import { withRouter } from "react-router";
import { connect } from "react-redux";
import FlashLoop from "../FlashLoop/FlashLoop";
import { fetchLoop } from "../../actions/loop";
import NotFound from "../NotFound";

class FlashLoopContainer extends React.Component {
    componentDidMount() {
        const { match, fetchLoopData } = this.props;
        fetchLoopData(match.params.id);
    }

    render() {
        const { loop } = this.props;

        if (loop === null) {
            return <NotFound />;
        }

        return <FlashLoop loop={loop} />;
    }
}

FlashLoopContainer.propTypes = {
    fetchLoopData: PropTypes.func.isRequired,
    loop: PropTypes.object,
    match: PropTypes.object.isRequired,
};

FlashLoopContainer.defaultProps = {
    loop: null,
};

const mapStateToProps = state => ({
    loop: state.loop.current,
});

const mapDispatchToProps = dispatch => ({
    fetchLoopData: id => dispatch(fetchLoop(id)),
});

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(FlashLoopContainer));
