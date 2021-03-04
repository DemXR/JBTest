import { createStore } from "vuex";

function getApiUrl() {
    return "http://" + window.location.hostname + ":8000/api/"
}

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

export default createStore({
    state: {
        exercises: {
            timerId: 0,
            checkReviewInterval: 3,
            loadingExerceises: false,
            currentPage: 1,
            list: []
        }
    },
    mutations: {
        setExercisesList(state, exercises) {
            state.exercises.list = [];
            exercises.forEach(item => {
                const exercise = {
                    id: item.id,
                    title: item.title,
                    body: item.body,
                    loading: false,
                    review: item.review
                };
                state.exercises.list.push(exercise);
            });
        },

        setExercisesReview(state, { exerciseId, review }) {
            state.exercises.list.map(item => {
                if (item.id === exerciseId) {
                    item.review = {
                        id: review.id,
                        reply: review.reply
                    };
                }
                return item;
            });
        },

        setExercisesLoad(state, loading) {
            state.exercises.loadingExerceises = loading;
        },

        setCurrentPage(state, pageNumber) {
            state.exercises.currentPage = pageNumber;
        }
    },
    actions: {
        loadExercises({ commit }) {
            commit("setExercisesLoad", true);
            const url = getApiUrl() + "exercise/";
            fetch(url, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
                credentials: "include"
            })
                .then(response => {
                    response.json().then(data => {
                        commit("setExercisesList", data);
                    });
                })
                .catch((error) => {
                    console.log(error)
                })
                .finally(() => {
                    commit("setExercisesLoad", false);
                });
        },

        sendForReview({ commit }, { exerciseId, replyText }) {
            const url = getApiUrl() + "exercise/" + exerciseId + "/review/";
            fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": readCookie("csrftoken"),
                },
                credentials: "include",
                body: JSON.stringify({
                    reply: replyText
                })
            })
                .then(response => {
                    response.json().then(data => {
                        commit("setExercisesReview", {
                            exerciseId: exerciseId,
                            review: data
                        });
                    });
                })
                .catch(error => {
                    console.log(error);
                });
        },

        checkReviewResult({ state, commit, dispatch }) {
            const onReview = state.exercises.list.filter(exercise => {
                if (
                    exercise.review &&
                    exercise.review.reply &&
                    exercise.review.reply.status &&
                    exercise.review.reply.status.slug &&
                    exercise.review.reply.status.slug === "evaluation"
                ) {
                    return exercise;
                }
            });
            onReview.forEach(exercise => {
                const url = getApiUrl() + "exercise/" +
                    exercise.id +
                    "/review/" +
                    exercise.review.id +
                    "/";
                fetch(url, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    credentials: "include"
                })
                    .then(response => {
                        response.json().then(data => {
                            commit("setExercisesReview", {
                                exerciseId: exercise.id,
                                review: data
                            });
                        });
                    })
                    .catch(() => {});
            });

            state.exercises.timerId = setTimeout(
                () => dispatch("checkReviewResult"),
                state.exercises.checkReviewInterval * 1000
            );   
        },

    },

    getters: {
        getExerciseList: state => {
            return state.exercises.list;
        },
        getCurrentPage: state => {
            return state.exercises.currentPage;
        },
        getLoading: state => {
            return state.exercises.loadingExerceises;
        }
    }
});
