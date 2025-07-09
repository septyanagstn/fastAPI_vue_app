<template>
  <card>
    <div class="mb-4 d-flex justify-content-between align-items-center">
      <div>
        <h4 class="card-title mb-0">Daftar Berita</h4>
        <p class="card-category mb-0 text-muted">Temukan berita terbaru</p>
      </div>
      <input type="text" class="col-6 form-control border rounded" v-model="query" name="search"
        placeholder="Search..." />
    </div>
    <div v-for="(article, index) in articles" :key="index"
      class="d-flex bg-light text-dark rounded overflow-hidden mb-3 shadow" style="height: 150px;">
      <router-link :to="{ name: 'article detail', params: { id: article._id } }"
        class="d-flex w-100 text-decoration-none text-dark">
        <!-- Gambar -->
        <div class="col-md-3">
          <img :src="article.thumbnail" alt="thumbnail" class="h-100 w-100 object-fit-cover" />
        </div>

        <!-- Konten -->
        <div class="p-3 d-flex flex-column justify-content-center flex-grow-1 hover">
          <h5 class="mb-2">{{ article.title }}</h5>
          <div class="d-flex align-items-center text-secondary small">
            <span class="me-2">{{ article.author }}</span>-<span class="ms-2">{{ formatDate(article.post_date) }}</span>
          </div>
        </div>
      </router-link>
    </div>
    <div class="clearfix btn-group col-md-2 offset-md-5">
      <button type="button" class="text-dark btn btn-sm btn-outline-secondary" @click="changePage(page - 1)"
        :disabled="page === 1"> <span class="ti-angle-double-left"></span> </button>

      <button v-for="n in paginatedPages" :key="n" class="text-dark btn btn-sm btn-outline-secondary"
        :class="{ 'active': page === n }" @click="changePage(n)">
        {{ n }}
      </button>

      <button type="button" class="text-dark btn btn-sm btn-outline-secondary" @click="changePage(page + 1)"
        :disabled="page === totalPages"> <span class="ti-angle-double-right"></span> </button>
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
      totalItems: 0,
      errors: [],
      page: 1,
      perPage: 10,
      pages: [],
      query: ''
    };
  },
  watch: {
    articles() {
      this.setPages();
    },
    query: {
      handler: 'getFilteredArticles',
      immediate: false
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.totalItems / this.perPage);
    },
    paginatedPages() {
      const total = this.totalPages;
      const current = this.page;
      const maxPagesToShow = 5;
      let start = Math.max(1, current - Math.floor(maxPagesToShow / 2));
      let end = start + maxPagesToShow - 1;

      if (end > total) {
        end = total;
        start = Math.max(1, end - maxPagesToShow + 1);
      }

      const pages = [];
      for (let i = start; i <= end; i++) {
        pages.push(i);
      }
      return pages;
    }
  },
  methods: {
    async getArticles() {
      const skip = (this.page - 1) * this.perPage;
      try {
        const response = await axios.get("http://localhost:8000/articles/", {
          params: { skip, limit: this.perPage }
        });
        this.articles = response.data.items;
        this.totalItems = response.data.total;
      } catch (e) {
        this.errors.push(e);
        console.error(e);
      }
    },
    async getFilteredArticles() {
      if (this.query.trim() === '') {
        return this.getArticles();
      }

      const skip = (this.page - 1) * this.perPage;

      try {
        const response = await axios.get(`http://localhost:8000/articles/search/${this.query}`, {
          params: { skip, limit: this.perPage }
        });
        this.articles = response.data.items;
        this.totalItems = response.data.total;
      } catch (e) {
        this.errors.push(e);
        console.error(e);
      }
    },
    formatDate(dateStr) {
      const options = { year: "numeric", month: "2-digit", day: "2-digit" };
      return new Date(dateStr).toLocaleDateString("id-ID", options);
    },
    setPages() {
      let numberOfPages = Math.ceil(this.articles.length / this.perPage);
      for (let index = 1; index <= numberOfPages; index++) {
        this.pages.push(index);
      }
    },
    async changePage(newPage) {
      this.page = newPage;
      if (this.query.trim() === '') {
        await this.getArticles();
      } else {
        await this.getFilteredArticles();
      }
    }
  },
  mounted() {
    this.getArticles();
  },
};
</script>
