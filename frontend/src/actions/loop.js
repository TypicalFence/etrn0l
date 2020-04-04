import { push } from "connected-react-router";

export const FETCH_LOOP = "SHOW_LOOP";
export const SHOW_LOOP = "SHOW_LOOP";
export const OPEN_TAGS = "OPEN_TAGS";
export const CLOSE_TAGS = "CLOSE_TAGS";
export const SHOW_404 = "CLOSE_TAGS";


export const showLoop = (data) => {
    const { loop, next, prev } = data;

    let prevLoop = null;
    let nextLoop = null;

    if (prev !== null) {
        prevLoop = prev;
    }

    if (next !== null) {
        nextLoop = next;
    }

    return {
        type: SHOW_LOOP,
        loop,
        next: nextLoop,
        prev: prevLoop,
    };
};

export const show404 = () => ({
    type: SHOW_404,
});


export const fetchLoop = id => (dispatch) => {
    fetch(`/api/v1/loops/${id}`)
        .then(resp => resp.json())
        .then((resp) => {
            if (resp.code === 200) {
                dispatch(showLoop(resp.data));
            } else {
                dispatch(show404());
            }
        });
};

export const gotToLoop = id => (dispatch) => {
    dispatch(push(`/${id}`));
    dispatch(fetchLoop(id));
};

export const goToRandomLoop = () => async (dispatch) => {
    const response = await fetch("/api/v1/random").then(resp => resp.json);

    if (response.code === 200) {
        const id = response.data.number;

        dispatch(gotToLoop(id));
    } else {
        dispatch(show404());
    }
};
