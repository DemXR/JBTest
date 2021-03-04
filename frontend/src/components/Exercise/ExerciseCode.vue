<template>
    <div class="code_mirror_wrapper">
        <textarea ref="codeMirrorEditor" />
    </div>
</template>

<script>
import { defineComponent } from "vue";
import store from "../../store/index";
import CodeMirror from "codemirror";
import "codemirror/lib/codemirror.css";
import "codemirror/theme/material-palenight.css";
import "codemirror/mode/python/python";

export default defineComponent({
    name: "ExerciseCode",

    data() {
        return {
            replyText: "",
            codeMirror: {
                type: CodeMirror
            }
        };
    },

    methods: {
        getReplyText() {
            return this.replyText;
        },
        createCodeMirrorInstance() {
            const divCodeEditor = this.$refs.codeMirrorEditor;
            const codeMirror = CodeMirror.fromTextArea(divCodeEditor, {
                mode: {
                    name: "python",
                    version: 3,
                    singleLineStringErrors: false
                },
                lineNumbers: true,
                indentUnit: 4,
                theme: "material-palenight"
            });
            codeMirror.setValue(this.code);
            codeMirror.on("change", code => {
                this.replyText = code.getValue();
                store.commit("setExercisesReview", {
                    exerciseId: this.exerciseId,
                    review: {
                        id: undefined,
                        reply: {
                            reply_text: this.replyText
                        }
                    }
                });
            });
            this.replyText = codeMirror.getValue();
            this.codeMirror = codeMirror;
        }
    },

    mounted() {
        this.createCodeMirrorInstance();
    },

    props: {
        exerciseId: {
            type: Number
        },

        code: {
            type: String,
            default: ""
        }
    },

    watch: {
        exerciseId() {
            this.codeMirror.toTextArea();
            this.createCodeMirrorInstance();
        }
    }
});
</script>
