<template>
  <div class="row">
    <div class="col-12">
      <card>
        <div class="mb-4 d-flex justify-content-between align-items-center">
          <div>
            <h4 class="card-title mb-0">Kelola Berita</h4>
            <p class="card-category mb-0 text-muted">Temukan berita terbaru</p>
          </div>
          <input type="text" class="col-6 form-control border rounded" v-model="query" name="search"
            placeholder="Search..." />
        </div>
        <div class="mb-2 d-flex justify-content-end">
          <button type="button" name="add" class="btn btn-success btn-xs" @click="openAddModal()">
            Add Berita <span class="ti-plus"></span>
          </button>
        </div>
        <table class="table">
          <thead class="table-secondary">
            <tr>
              <th>#</th>
              <th>Title</th>
              <th>Author</th>
              <th>Post Date</th>
              <th>Content</th>
              <th>Thumbnail</th>
              <th>Edit</th>
              <th>Delete</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(article, index) in articles" :key="index">
              <td>{{ article.index }}</td>
              <td>{{ shortenText(article.title) }}</td>
              <td>{{ article.author }}</td>
              <td>{{ formatDate(article.post_date) }}</td>
              <td>{{ shortenText(article.content) }}</td>
              <td>{{ shortenText(article.thumbnail) }}</td>
              <td>
                <button type="button" class="btn btn-primary btn-xs" @click="openEditModal(article._id)">
                  Edit
                </button>
              </td>
              <td>
                <button type="button" class="btn btn-danger btn-xs" @click="openDeleteModal(article._id)">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="clearfix btn-group col-md-2 offset-md-5">
          <button type="button" class="text-dark btn btn-sm btn-outline-secondary" @click="changePage(page - 1)"
            :disabled="page === 1"> &laquo; </button>

          <button v-for="n in paginatedPages" :key="n" class="text-dark btn btn-sm btn-outline-secondary"
            :class="{ 'active': page === n }" @click="changePage(n)">
            {{ n }}
          </button>

          <button type="button" class="text-dark btn btn-sm btn-outline-secondary" @click="changePage(page + 1)"
            :disabled="page === totalPages"> &raquo; </button>
        </div>
      </card>
    </div>

    <!-- Modal Add -->
    <div v-if="modals.add" class="modal fade show d-block" style="background-color: rgba(0, 0, 0, 0.5); z-index: 1050">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title">Tambah Berita</h4>
          </div>
          <div class="modal-body">
            <form>
              <div class="form-group">
                <label for="title" class="form-label" style="font-weight: bold; font-size: large">Title</label>
                <input type="text" v-model="form.title" class="form-control border" name="title"
                  placeholder="Add a title" required />
              </div>
              <div class="form-group">
                <label for="author" class="form-label" style="font-weight: bold; font-size: large">Author</label>
                <input type="text" v-model="form.author" class="form-control border" name="author"
                  placeholder="Add a author" required />
              </div>
              <div class="form-group">
                <label for="content" class="form-label" style="font-weight: bold; font-size: large">Content</label>
                <textarea type="" v-model="form.content" class="form-control border" name="content"
                  placeholder="Add a content" required></textarea>
              </div>
              <div class="form-group">
                <label for="thumbnail" class="form-label" style="font-weight: bold; font-size: large">Thumbnail</label>
                <input type="url" v-model="form.thumbnail" class="form-control border" name="thumbnail"
                  placeholder="Add a thumbnail url" required />
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeAddModal()">
              Close
            </button>
            <button class="btn btn-success" @click="addArticle(), closeAddModal(), resetForm()">Submit</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Edit -->
    <div v-if="modals.edit" class="modal fade show d-block" style="background-color: rgba(0, 0, 0, 0.5); z-index: 1050">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title">Update Berita</h4>
          </div>
          <div class="modal-body">
            <form>
              <div class="form-group">
                <label for="title" class="form-label" style="font-weight: bold; font-size: large">Title</label>
                <input type="text" v-model="form.title" class="form-control border" name="title"
                  placeholder="Update a title" required />
              </div>
              <div class="form-group">
                <label for="author" class="form-label" style="font-weight: bold; font-size: large">Author</label>
                <input type="text" v-model="form.author" class="form-control border" name="author"
                  placeholder="Update a author" required />
              </div>
              <div class="form-group">
                <label for="content" class="form-label" style="font-weight: bold; font-size: large">Content</label>
                <textarea type="" v-model="form.content" class="form-control border" name="content"
                  placeholder="Update a content" required></textarea>
              </div>
              <div class="form-group">
                <label for="thumbnail" class="form-label" style="font-weight: bold; font-size: large">Thumbnail</label>
                <input type="url" v-model="form.thumbnail" class="form-control border" name="thumbnail"
                  placeholder="Update a thumbnail url" required />
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeEditModal()">
              Close
            </button>
            <button class="btn btn-success" @click="updateArticle(), closeEditModal(), resetForm()">Submit</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Delete -->
    <div v-if="modals.delete" class="modal fade show d-block"
      style="background-color: rgba(0, 0, 0, 0.5); z-index: 1050">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title">Hapus Berita</h4>
          </div>
          <div class="modal-body">
            <p>Yakin ingin menghapus berita?</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeDeleteModal()">
              Batal
            </button>
            <button class="btn btn-danger" @click="deleteArticle(), closeDeleteModal()">Hapus</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      article_id: "",
      articles: [],
      totalItems: 0,
      page: 1,
      perPage: 10,
      pages: [],
      form: {
        title: "",
        author: "",
        post_date: "",
        content: "",
        thumbnail: "",
      },
      selectedArticle: null,
      errors: [],
      modals: {
        add: false,
        edit: false,
        delete: false,
      },
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
    // displayedArticles() {
    //   return this.paginate(this.articles);
    // }
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
        this.articles = response.data.items.map((article, idx) => ({
          ...article,
          index: (this.page - 1) * this.perPage + idx + 1
        }));
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
        this.articles = response.data.items.map((article, idx) => ({
          ...article,
          index: (this.page - 1) * this.perPage + idx + 1
        }));
        this.totalItems = response.data.total;
      } catch (e) {
        this.errors.push(e);
        console.error(e);
      }
    },
    formatDate(dateStr) {
      const options = {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
      };
      return new Date(dateStr).toLocaleDateString("id-ID", options);
    },
    shortenText(text, maxLength = 20) {
      if (!text) return "";
      return text.length > maxLength ? text.slice(0, maxLength) + "..." : text;
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
    },
    openAddModal() {
      this.modals.add = true
    },
    async openEditModal(id) {
      try {
        const response = await axios.get(`http://localhost:8000/articles/detail/${id}`)
        const data = response.data

        this.form.title = data.title
        this.form.author = data.author
        this.form.post_date = data.post_date
        this.form.content = data.content
        this.form.thumbnail = data.thumbnail

        this.modals.edit = true
        this.article_id = id
      } catch (e) {
        this.errors.push(e);
        console.error(e);
      }
    },
    openDeleteModal(id) {
      this.modals.delete = true
      this.article_id = id
    },
    closeAddModal() {
      this.modals.add = false
    },
    closeEditModal() {
      this.modals.edit = false
      this.article_id = ''
    },
    closeDeleteModal() {
      this.modals.delete = false
      this.article_id = ''
    },
    resetForm() {
      this.form.title = '',
        this.form.author = '',
        this.form.post_date = '',
        this.form.content = '',
        this.form.thumbnail = ''
    },
    async addArticle() {
      try {
        const response = await axios.post("http://localhost:8000/articles", {
          title: this.form.title,
          author: this.form.author,
          post_date: new Date(),
          content: this.form.content,
          thumbnail: this.form.thumbnail
        });
        const data = response.data

        alert(data.message)
        this.getArticles()
      } catch (e) {
        this.errors.push(e);
        console.error(e);
      }
    },
    async updateArticle() {
      try {
        const response = await axios.put(`http://localhost:8000/articles/${this.article_id}`, {
          title: this.form.title,
          author: this.form.author,
          post_date: new Date(),
          content: this.form.content,
          thumbnail: this.form.thumbnail
        });
        const data = response.data

        alert(data.message)
        this.getArticles()
      } catch (e) {
        this.errors.push(e);
        console.error(e);
      }
    },
    async deleteArticle() {
      try {
        const response = await axios.delete(`http://localhost:8000/articles/${this.article_id}`)
        const data = response.data

        alert(data.message)
        this.getArticles()
      } catch (e) {
        this.errors.push(e);
        console.error(e);
      }
    },
  },
  mounted() {
    this.getArticles();
  },
};
</script>
