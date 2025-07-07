<template>
  <card title="Daftar Berita">
    <!-- <div>
      <input type="text" class="rounded form-control border" name="search" placeholder="Search..." />
      <i class="ti-search"></i>
    </div> -->
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
    };
  },
  watch: {
    articles() {
      this.setPages();
    }
  },
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
