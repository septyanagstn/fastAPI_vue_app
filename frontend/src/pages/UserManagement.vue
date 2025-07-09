<template>
  <div class="row">
    <div class="col-12">
      <card>
        <div class="mb-4 d-flex justify-content-between align-items-center">
          <div>
            <h4 class="card-title mb-0">Kelola User</h4>
            <!-- <p class="card-category mb-0 text-muted">Temukan user </p> -->
          </div>
          <input type="text" class="col-6 form-control border rounded" v-model="query" name="search"
            placeholder="Search..." />
        </div>
        <div class="mb-2 d-flex justify-content-end">
          <button type="button" name="add" class="btn btn-success btn-xs" @click="openAddModal()">
            Add User <span class="ti-plus"></span>
          </button>
        </div>
        <table class="table">
          <thead class="table-secondary">
            <tr>
              <th>#</th>
              <th>Username</th>
              <th>Email</th>
              <th>Full Name</th>
              <th>Password</th>
              <th>Edit</th>
              <th>Delete</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in users" :key="index">
              <td>{{ user.index }}</td>
              <td>{{ shortenText(user.username) }}</td>
              <td>{{ user.email }}</td>
              <td>{{ shortenText(user.full_name) }}</td>
              <td>{{ hideText(user.password) }}</td>
              <td>
                <button type="button" class="btn btn-primary btn-xs" @click="openEditModal(user._id)">
                  Edit
                </button>
              </td>
              <td>
                <button type="button" class="btn btn-danger btn-xs" @click="openDeleteModal(user._id)">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
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
    </div>

    <!-- Modal Add -->
    <div v-if="modals.add" class="modal fade show d-block" style="background-color: rgba(0, 0, 0, 0.5); z-index: 1050">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title">Tambah User</h4>
          </div>
          <div class="modal-body">
            <form>
              <div class="form-group">
                <label for="username" class="form-label" style="font-weight: bold; font-size: large">Username</label>
                <input type="text" v-model="form.username" class="form-control border" name="username"
                  placeholder="Add a username" required />
              </div>
              <div class="form-group">
                <label for="email" class="form-label" style="font-weight: bold; font-size: large">Email</label>
                <input type="email" v-model="form.email" class="form-control border" name="email"
                  placeholder="Add a email" required />
              </div>
              <div class="form-group">
                <label for="fullname" class="form-label" style="font-weight: bold; font-size: large">Fullname</label>
                <input type="text" v-model="form.full_name" class="form-control border" name="fullname"
                  placeholder="Add a fullname" required></input>
              </div>
              <div class="form-group">
                <label for="password" class="form-label" style="font-weight: bold; font-size: large">Password</label>
                <input type="password" v-model="form.password" class="form-control border" name="password"
                  placeholder="Add a password" required />
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeAddModal()">
              Close
            </button>
            <button class="btn btn-success" @click="addUsers(), closeAddModal(), resetForm()">Submit</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Edit -->
    <div v-if="modals.edit" class="modal fade show d-block" style="background-color: rgba(0, 0, 0, 0.5); z-index: 1050">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="modal-title">Update User</h4>
          </div>
          <div class="modal-body">
            <form>
              <div class="form-group">
                <label for="username" class="form-label" style="font-weight: bold; font-size: large">Username</label>
                <input type="text" v-model="form.username" class="form-control border" name="username"
                  placeholder="Add a username" required />
              </div>
              <div class="form-group">
                <label for="email" class="form-label" style="font-weight: bold; font-size: large">Email</label>
                <input type="email" v-model="form.email" class="form-control border" name="email"
                  placeholder="Add a email" required />
              </div>
              <div class="form-group">
                <label for="fullname" class="form-label" style="font-weight: bold; font-size: large">Fullname</label>
                <input type="text" v-model="form.full_name" class="form-control border" name="fullname"
                  placeholder="Add a fullname" required></input>
              </div>
              <div class="form-group">
                <label for="password" class="form-label" style="font-weight: bold; font-size: large">Password</label>
                <input type="password" v-model="form.password" class="form-control border" name="password"
                  placeholder="Add a password" required />
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeEditModal()">
              Close
            </button>
            <button class="btn btn-success" @click="updateUsers(), closeEditModal(), resetForm()">Submit</button>
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
            <h4 class="modal-title">Hapus User</h4>
          </div>
          <div class="modal-body">
            <p>Yakin ingin menghapus User?</p>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" @click="closeDeleteModal()">
              Batal
            </button>
            <button class="btn btn-danger" @click="deleteUsers(), closeDeleteModal()">Hapus</button>
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
      user_id: "",
      users: [],
      totalItems: 0,
      page: 1,
      perPage: 10,
      pages: [],
      form: {
        username: "",
        email: "",
        full_name: "",
        password: "",
      },
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
    users() {
      this.setPages();
    },
    query: {
      handler: 'getFilteredUsers',
      immediate: false
    }
  },
  computed: {
    // displayedUsers() {
    //   return this.paginate(this.users);
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
    async getUsers() {
      const skip = (this.page - 1) * this.perPage;
      try {
        const response = await axios.get("http://localhost:8000/users/", {
          params: { skip, limit: this.perPage }
        });
        this.users = response.data.items.map((user, idx) => ({
          ...user,
          index: (this.page - 1) * this.perPage + idx + 1
        }));
        this.totalItems = response.data.total;
      } catch (e) {
        this.errors.push(e);
        console.error(e);
      }
    },
    async getFilteredUsers() {
      if (this.query.trim() === '') {
        return this.getUsers();
      }

      const skip = (this.page - 1) * this.perPage;

      try {
        const response = await axios.get(`http://localhost:8000/users/search/${this.query}`, {
          params: { skip, limit: this.perPage }
        });
        this.users = response.data.items.map((user, idx) => ({
          ...user,
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
    hideText(text) {
      if (text) return "...";
    },
    setPages() {
      let numberOfPages = Math.ceil(this.users.length / this.perPage);
      for (let index = 1; index <= numberOfPages; index++) {
        this.pages.push(index);
      }
    },
    async changePage(newPage) {
      this.page = newPage;
      if (this.query.trim() === '') {
        await this.getUsers();
      } else {
        await this.getFilteredUsers();
      }
    },
    openAddModal() {
      this.modals.add = true
    },
    async openEditModal(id) {
      try {
        const response = await axios.get(`http://localhost:8000/users/${id}`)
        const data = response.data

        this.form.username = data.username
        this.form.email = data.email
        this.form.full_name = data.full_name
        this.form.password = data.password

        this.modals.edit = true
        this.user_id = id
      } catch (e) {
        this.errors.push(e);
        console.error(e);
      }
    },
    openDeleteModal(id) {
      this.modals.delete = true
      this.user_id = id
    },
    closeAddModal() {
      this.modals.add = false
    },
    closeEditModal() {
      this.modals.edit = false
      this.user_id = ''
    },
    closeDeleteModal() {
      this.modals.delete = false
      this.user_id = ''
    },
    resetForm() {
      this.form.username = '',
        this.form.email = '',
        this.form.full_name = '',
        this.form.password = ''
    },
    async addUsers() {
      try {
        const response = await axios.post("http://localhost:8000/users", {
          username: this.form.username,
          full_name: this.form.full_name,
          email: this.form.email,
          password: this.form.password,
        });
        const data = response.data

        alert(data.message)
        this.getUsers()
      } catch (e) {
        this.errors.push(e);
        console.error(e);
      }
    },
    async updateUsers() {
      try {
        const response = await axios.put(`http://localhost:8000/users/${this.user_id}`, {
          username: this.form.username,
          email: this.form.email,
          full_name: this.form.full_name,
          password: this.form.password
        });
        const data = response.data

        alert(data.message)
        this.getUsers()
      } catch (e) {
        this.errors.push(e);
        console.error(e);
      }
    },
    async deleteUsers() {
      try {
        const response = await axios.delete(`http://localhost:8000/users/${this.user_id}`)
        const data = response.data

        alert(data.message)
        this.getUsers()
      } catch (e) {
        this.errors.push(e);
        console.error(e);
      }
    },
  },
  mounted() {
    this.getUsers();
  },
};
</script>
