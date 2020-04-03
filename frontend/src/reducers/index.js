import { combineReducers } from "redux";
import { connectRouter } from "connected-react-router";
import loopReducer from "./loop";

const createRootReducer = history => combineReducers({
    router: connectRouter(history),
    loop: loopReducer,
});

export default createRootReducer;
