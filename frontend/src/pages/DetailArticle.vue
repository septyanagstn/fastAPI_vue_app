<template>
    <div>
        <!-- Title -->
        <h1></h1>
        <!-- Post Date -->
        <p></p>
        <!-- Author -->
        <p></p>
        <div>
            <!-- Thumbnail -->
            <div>

            </div>
            <!-- Content -->
            <div>

            </div>
        </div>`
    </div>
</template>
<script>
import axios from 'axios';

export default{
    name: "ArticleDetail",
    data() {
        return {
            article_id: this.$route.params.id,
            article: [],
            errors: []
        }
    },
    methods: {
        async getArticleDetail() {
        try {
            const response = await axios.get(`http://localhost:8000/articles/detail/${this.article_id}`);
            this.article = response.data;
            console.log(response.data)
        } catch (e) {
            this.errors.push(e);
            console.error(e);
        }
        },
        formatDate(dateStr) {
        const options = { year: "numeric", month: "2-digit", day: "2-digit" };
        return new Date(dateStr).toLocaleDateString("id-ID", options);
        },
    },
    mounted() {
        this.getArticleDetail();
    },
}
</script>