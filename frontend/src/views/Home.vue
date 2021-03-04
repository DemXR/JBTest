<template>
    <div class="exercises">
        <exercise v-if="currentExercise" :exercise="currentExercise" />
        <exercise-loading v-if="isLoading" />
        <exercise-not-found v-if="!isLoading && exerciseCount === 0" />
        <pagination
            v-if="exerciseCount > 0"
            :count="exerciseCount"
            :currentPage="currentPage"
        />
    </div>
</template>

<script>
import Exercise from "@/components/Exercise/Exercise.vue";
import ExerciseLoading from "@/components/Exercise/ExerciseLoading.vue";
import ExerciseNotFound from "@/components/Exercise/ExerciseNotFound.vue";
import Pagination from "@/components/Pagination.vue";
import store from "../../src/store/";

export default {
    name: "Home",

    data() {
        return {
            exerciseCount: 0
        };
    },

    components: {
        Pagination,
        Exercise,
        ExerciseLoading,
        ExerciseNotFound
    },

    computed: {
        isLoading() {
            return this.$store.getters.getLoading;
        },
        exerciseList() {
            return this.$store.getters.getExerciseList;
        },
        currentPage() {
            return this.$store.getters.getCurrentPage;
        },
        currentExercise() {
            return this.exerciseList[this.currentPage - 1];
        }
    },

    mounted() {
        store.dispatch("loadExercises").then(() => {
            store.dispatch("checkReviewResult");
        });
    },

    watch: {
        exerciseList(exercises) {
            if (Array.isArray(exercises)) {
                this.exerciseCount = exercises.length;
            } else {
                this.exerciseCount = 0;
            }

            if (this.exerciseCount < this.currentPage) {
                this.currentPage = this.exerciseCount;
            }
        }
    }
};
</script>
