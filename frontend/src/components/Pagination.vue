<template>
    <div class="exercise-pagination">
        <el-pagination
            background
            layout="prev, pager, next"
            :total="count"
            :current-page="currentPage"
            :page-size="1"
            @current-change="handleCurrentPage"
        >
        </el-pagination>
    </div>
</template>

<script>
import { defineComponent } from "vue";
import store from "../../src/store/";

export default defineComponent({
    name: "Pagination",

    methods: {
        handleCurrentPage(value) {
            store.commit("setCurrentPage", value);
        }
    },

    props: {
        count: {
            type: Number,
            default: 10
        },
        currentPage: {
            type: Number,
            default: 1
        }
    }
});
</script>
