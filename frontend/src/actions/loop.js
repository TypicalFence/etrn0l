export const FETCH_STATUS = "FETCH_LOOP";
export const FETCH_RANDOM_LOOP = "SHOW_LOOP";
export const SHOW_LOOP = "SHOW_LOOP";
export const OPEN_TAGS = "OPEN_TAGS";
export const CLOSE_TAGS = "CLOSE_TAGS";
export const SHOW_404 = "CLOSE_TAGS";


export const showLoop = (data) => {
    const { loop, next, prev } = data;

    let prevLoop = null;
    let nextLoop = null;

    if (prev !== null) {
        prevLoop = prev.number;
    }

    if (next !== null) {
        nextLoop = next.number;
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
