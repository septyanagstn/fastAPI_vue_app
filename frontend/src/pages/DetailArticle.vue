<template>

    <loader v-if="is_loading" />

    <div v-else class="col-md-10 mx-auto d-block">
        <!-- Title -->
        <h1 class="text-center"><strong>{{ article.title }}</strong></h1>
        <!-- Post Date -->
        <p>Kompas.com - {{ formatDate(article.post_date) }}</p>
        <!-- Author -->
        <h6>Tim Redaksi - {{ article.author }}</h6>
        <div class="mt-4">
            <!-- Thumbnail -->
            <div class="mb-3">
                <img :src="article.thumbnail" alt="thumbnail" class="img-thumbnail">
            </div>
            <!-- Content -->
            <div>
                <p v-for="content in splittedContent" class="text-justify">{{ content }}</p>
            </div>
        </div>`
    </div>
</template>
<script>
import axios from 'axios';
import loader from '@/components/Loader.vue'; 

export default {
    components: {
        loader,
    },
    name: "ArticleDetail",
    data() {
        return {
            is_loading: true,
            article_id: this.$route.params.id,
            article: [],
            // content: [],
            errors: []
        }
    },
    computed: {
        splittedContent() {
            return (this.article.content || "").split("|");
        }
    },
    methods: {
        async getArticleDetail() {
            try {
                this.is_loading = true;
                const response = await axios.get(`http://localhost:8000/articles/detail/${this.article_id}`);
                this.article = response.data;
            } catch (e) {
                this.errors.push(e);
                console.error(e);
            } finally {
                this.is_loading = false;
            }
        },
        formatDate(dateStr) {
            const options = { year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" };
            return new Date(dateStr).toLocaleDateString("id-ID", options);
        },
    },
    mounted() {
        this.getArticleDetail();
    },
}
</script>