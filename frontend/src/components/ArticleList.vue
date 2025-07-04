<template>
  <div class="container">
    <div
      v-for="(article, index) in articles"
      :key="index"
      class="d-flex bg-dark text-white rounded overflow-hidden mb-3 shadow"
      style="height: 150px;"
    >
      <!-- Gambar -->
      <div style="flex: 0 0 150px;">
        <img
          :src="article.thumbnail"
          alt="Thumbnail"
          class="h-100 w-100 object-fit-cover"
        />
      </div>

      <!-- Konten -->
      <div class="p-3 d-flex flex-column justify-content-center" style="flex: 1;">
        <h5 class="mb-2" style="font-weight: bold;">{{ article.title }}</h5>
        <div class="d-flex align-items-center text-secondary small">
          <span class="me-2">{{ article.author }}</span>
          •
          <span class="ms-2">{{ formatDate(article.post_date) }}</span>
        </div>
      </div>
    </div>
  </div>
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
        const response = await axios.get("http://localhost:8000");
        this.articles = response.data;
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
