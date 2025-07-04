<template>
  <card title="Daftar Berita">
    <div
      v-for="(article, index) in articles"
      :key="index"
      class="d-flex bg-light text-dark rounded overflow-hidden mb-3 shadow"
      style="height: 150px;"
    >
      <router-link
        :to="{ name: 'article-detail', params: { id: article._id }}"
        class="d-flex w-100 text-decoration-none text-dark"
      >
        <!-- Gambar -->
        <div style="width: 150px; flex-shrink: 0;">
          <img
            :src="article.thumbnail"
            alt="thumbnail"
            class="h-100 w-100 object-fit-cover"
            style="object-fit: cover;"
          />
        </div>

        <!-- Konten -->
        <div class="p-3 d-flex flex-column justify-content-center flex-grow-1">
          <h5 class="mb-2 fw-bold">{{ article.title }}</h5>
          <div class="d-flex align-items-center text-secondary small">
            <span class="me-2">{{ article.author }}</span>-<span class="ms-2">{{ formatDate(article.post_date) }}</span>
          </div>
        </div>
      </router-link>
    </div>
  </card>
</template>

<script>
import axios from "axios";

export default {
  name: "ArticleList",
  data() {
    return {
      articles: [],
      errors: [],
    };
  },
  methods: {
    async getArticles() {
      try {
        const response = await axios.get("http://localhost:8000/articles");
        this.articles = response.data;
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
    this.getArticles();
  },
};
</script>
