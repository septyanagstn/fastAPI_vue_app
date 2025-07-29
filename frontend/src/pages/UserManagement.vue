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

        <loader v-if="is_loading" />

        <table v-else class="table">
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
          <Pagination :currentPage="page" :totalPages="totalPages" @change="changePage" />
        </div>
      </card>
    </div>

    <!-- Modals -->
    <AddUserModal v-if="modals.add" :form="form" @close="closeAddModal" @submit="handleAddUser" />
    <EditUserModal v-if="modals.edit" :form="form" @close="closeEditModal" @submit="handleUpdateUser" />
    <DeleteUserModal v-if="modals.delete" :user="selectedUser" @close="closeDeleteModal" @confirm="handleDeleteUser" />

  </div>
</template>

<script>
import axios from "axios";
import Pagination from "@/components/Pagination.vue";
import AddUserModal from "@/components/User/AddUser.vue";
import EditUserModal from "@/components/User/EditUser.vue";
import DeleteUserModal from "@/components/User/DeleteUser.vue";
import loader from "@/components/Loader.vue";

export default {
  components: {
    Pagination,
    AddUserModal,
    EditUserModal,
    DeleteUserModal,
    loader,
  },
  data() {
    return {
      is_loading: true,
      user_id: "",
      users: [],
      selectedUser: null,
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
        this.is_loading = true;
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
      } finally {
        this.is_loading = false;
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
      const user = this.users.find(u => u._id === id);
      if (user) {
        this.selectedUser = user;
        this.user_id = id;
        this.modals.delete = true;
      }
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
        const response = await axios.post("http://localhost:8000/users/", {
          username: this.form.username,
          full_name: this.form.full_name,
          email: this.form.email,
          password: this.form.password,
        });
        const data = response.data;

        alert(data.message);
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
        const data = response.data;

        alert(data.message);
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
    async handleAddUser() {
      await this.addUsers();
      this.resetForm();
      this.getUsers();
      this.closeAddModal();
    },
    async handleUpdateUser() {
      await this.updateUsers();
      this.resetForm();
      this.getUsers();
      this.closeEditModal();
    },
    async handleDeleteUser() {
      await this.deleteUsers();
      this.getUsers();
      this.closeDeleteModal();
    },
  },
  mounted() {
    this.getUsers();
  },
};
</script>
