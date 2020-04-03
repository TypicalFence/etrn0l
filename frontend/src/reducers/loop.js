import { SHOW_LOOP, SHOW_404 } from "../actions/loop";

const defaultState = {
    current: null,
    next: null,
    previous: null,
    notFound: false,
};

const loopReducer = (state = defaultState, action) => {
    switch (action.type) {
        case SHOW_LOOP: {
            return Object.assign({}, state, {
                notFound: false,
                current: action.loop,
                next: action.next,
                previous: action.prev,
            });
        }

        case SHOW_404: {
            return Object.assign({}, state, {
                notFound: true,
                current: null,
                next: null,
                previous: null,
            });
        }

        default: {
            return state;
        }
    }
};

export default loopReducer;
