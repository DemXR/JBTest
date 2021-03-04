<template>
    <div class="exercise-container__actions">
        <el-button type="success" @click="sendToReview()"
            >Отправить на проверку</el-button
        >
    </div>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
    name: "ExerciseFooter",

    methods: {
        sendToReview() {
            this.$emit("sendToReview");
        }
    },

    computed: {
        enableSendButton() {
            return !this.status || this.status.slug === "wrong";
        }
    },

    props: {
        review: {
            type: Object
        }
    }
});
</script>
