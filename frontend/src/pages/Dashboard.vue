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
    <div v-for="(article, index) in displayedArticles" :key="index"
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
      <button type="button" class="text-dark btn btn-sm btn-outline-secondary" v-if="page != 1" @click="page--">
        << </button>
          <button type="button" class="text-dark btn btn-sm btn-outline-secondary"
            v-for="pageNumber in pages.slice(page - 1, page + 5)" @click="page = pageNumber"> {{ pageNumber }} </button>
          <button type="button" class="text-dark btn btn-sm btn-outline-secondary" @click="page++"
            v-if="page < pages.length"> >>
          </button>
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
  // watch: {
  //   query: {
  //     handler: 'getFilteredArticles',
  //     debounce: 200
  //   }
  // },
  computed: {
    displayedArticles() {
      return this.paginate(this.articles);
    }
  },
  methods: {
    async getArticles() {
      try {
        const response = await axios.get("http://localhost:8000/articles");
        this.articles = response.data.sort((a, b) => new Date(b.post_date) - new Date(a.post_date));
      } catch (e) {
        this.errors.push(e);
        console.error(e);
      }
    },
    async getFilteredArticles() {
      if (this.query.trim() === '') {
        return this.getArticles();
      }
      try {
        const response = await axios.get(`http://localhost:8000/articles/search/${this.query}`);
        const sorted = response.data.sort((a, b) => new Date(b.post_date) - new Date(a.post_date));
        this.articles = sorted;
        this.page = 1;
        this.pages = [];
        this.setPages();
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
    paginate(articles) {
      let page = this.page;
      let perPage = this.perPage;
      let from = (page * perPage) - perPage;
      let to = (page * perPage);
      return articles.slice(from, to);
    },
  },
  mounted() {
    this.getArticles();
  },
};
</script>
