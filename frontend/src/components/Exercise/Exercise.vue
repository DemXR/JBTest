<template>
    <div
        class="exercise-container"
        v-loading="reviewStatus === 'evaluation'"
        element-loading-background="rgba(0, 0, 0, 0.8)"
        element-loading-text="На проверке..."
    >
        <div class="exercise-container__header">
            <h1 class="exercise-title">
                {{ exercise.title }}
                <i class="el-icon-success green" title="Верно" v-if="reviewStatus === 'correct'"></i>
                <i class="el-icon-error red" title="Неверно" v-if="reviewStatus === 'wrong'"></i>
            </h1>
            <h3 class="exercise-body">{{ exercise.body }}</h3>
        </div>
        <div class="exercise-code">
            <exercise-code
                ref="codeEditor"
                :exerciseId="exercise.id"
                :code="exerciseCode"
            />
        </div>
        <div class="exercise-container__footer" v-if="reviewStatus != 'correct'">
            <exercise-footer
                :review="exercise.review"
                @sendToReview="sendForReview"
            />
        </div>
    </div>
</template>

<script>
import { defineComponent } from "vue";
import ExerciseCode from "./ExerciseCode.vue";
import ExerciseFooter from "./ExerciseFooter.vue";
import store from "../../store/index";

export default defineComponent({
    name: "Exercise",

    components: {
        ExerciseCode,
        ExerciseFooter
    },

    methods: {
        sendForReview() {
            const replyText = this.$refs.codeEditor.getReplyText();
            store.dispatch("sendForReview", {
                exerciseId: this.exercise.id,
                replyText: replyText
            });
        }
    },

    computed: {
        reviewStatus() {
            try {
                return this.exercise.review.reply.status.slug;
            } catch {
                return "";
            }
        },

        exerciseCode() {
            try {
                return this.exercise.review.reply.reply_text;
            } catch {
                return "";
            }
        }
    },

    props: {
        exercise: {
            type: Object
        }
    }
});
</script>
