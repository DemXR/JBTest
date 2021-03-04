import { createStore } from "vuex";

// Возвращает URL до API
function getApiUrl() {
    return "http://" + window.location.hostname + ":8000/api/";
}

// Возвращает cookie value по его name
function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(";");
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == " ") c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

export default createStore({
    state: {
        exercises: {
            // Информация по упражнениям
            timerId: 0, // Идентификатор таймера для периодической проверки результата ревью
            checkReviewInterval: 3, // Интервал для периодической проверки результата ревью
            loadingExerceises: false, // Признак процесса загрузки упражнений
            currentPage: 1, // Текущая страница (для пагинации)
            list: [] // Перечень упражнений
        }
    },

    mutations: {
        // Записывает список упражнений в state
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

        // Сохраняет результаты ревью для упражнения
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

        // Устанавливает признак загрузки упражнений
        setExercisesLoad(state, loading) {
            state.exercises.loadingExerceises = loading;
        },

        // Устанавливает текущую страницу (для пагинации)
        setCurrentPage(state, pageNumber) {
            state.exercises.currentPage = pageNumber;
        }
    },

    actions: {
        // Загрузка списка упражнений
        loadExercises({ commit }) {
            commit("setExercisesLoad", true);
            const url = getApiUrl() + "exercise/";
            fetch(url, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                },
                credentials: "include"
            })
                .then(response => {
                    response.json().then(data => {
                        commit("setExercisesList", data);
                    });
                })
                .catch(error => {
                    console.log(error);
                })
                .finally(() => {
                    commit("setExercisesLoad", false);
                });
        },

        // Отправка результата на review
        sendForReview({ commit }, { exerciseId, replyText }) {
            const url = getApiUrl() + "exercise/" + exerciseId + "/review/";
            fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": readCookie("csrftoken")
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

        // Запрос результата для упражнений, которые находятся на ревью
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
                const url =
                    getApiUrl() +
                    "exercise/" +
                    exercise.id +
                    "/review/" +
                    exercise.review.id +
                    "/";
                fetch(url, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json"
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
        }
    },

    getters: {
        // Возвращает список упражнений
        getExerciseList: state => {
            return state.exercises.list;
        },
        // Возвращает текущую страницу пагинации
        getCurrentPage: state => {
            return state.exercises.currentPage;
        },
        // Возвращает признак загрузки приложения
        getLoading: state => {
            return state.exercises.loadingExerceises;
        }
    }
});
