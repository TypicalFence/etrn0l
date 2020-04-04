import "./index.scss";
import { renderApp } from "./app";
import configureStore, { history } from "./store";
import "../vendor/ruffle/web/js-src/ruffle-object";

//polyfill(["static-content"]);

const store = configureStore();
renderApp(store, history);
