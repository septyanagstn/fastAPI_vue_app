<template>
    <div class="container bg-white p-5 border border-secondary rounded shadow d-flex flex-column align-items-center justify-content-center"
        style="max-width: 400px; margin: 40px auto 0 auto;">
        <h2 class="mb-5 text-center" style="font-weight: bold;">Login</h2>
        <form @submit.prevent="login()">
            <div class="form-group">
                <label for="email" class="form-label" style="font-weight: bold; font-size: large;">Email</label>
                <input type="email" v-model="email" class="form-control border" name="email"
                    placeholder="example@gmail.com" required>
            </div>
            <div class="form-group" style="position: relative;">
                <label for="password" class="form-label" style="font-weight: bold; font-size: large;">Password</label>
                <input :type="showPassword ? 'text' : 'password'" class="form-control border" name="password"
                    placeholder="Enter your password" required v-model="password" style="padding-right: 40px;">
                <button type="button" id="togglePassword" @click="togglePassword"
                    style="position: absolute; right: 10px; top: 38px; border: none; background: none; cursor: pointer; padding: 0;"
                    tabindex="-1">
                    <i :class="showPassword ? 'ti-eye' : 'ti-eye'"></i>
                </button>
            </div>
            <p class="text-secondary mb-2">It must be a combination of minimum letters, numbers, and symbols.</p>
            <div class="w-100 mt-5 d-flex justify-content-center">
                <button type="submit" class="text-white w-100 p-2 rounded border-secondary bg-dark cursor-pointer"
                    style="font-weight: bold;">Login</button>
            </div>
            <div class="text-center mt-3 mb-5">
                <p>Don't have an account? <span><router-link to="/register">SignUp</router-link></span></p>
            </div>
        </form>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "Login",
    data() {
        return {
            email: "",
            password: "",
            showPassword: false,
            errors: [],
        };
    },
    methods: {
        togglePassword() {
            this.showPassword = !this.showPassword;
        },
        resetForm() {
            this.email = '',
            this.password = ''
        }, 
        async login() {
            try {
                const response = await axios.post('http://localhost:8000/login', {
                    email: this.email,
                    password: this.password,
                });

                const data = response.data;

                // console.log(data.access_token)

                // Simpan token dan user info
                localStorage.setItem("access_token", data.access_token);
                localStorage.setItem("user", JSON.stringify(data.user));

                // Arahkan ke dashboard
                try {
                    this.$router.push("/warta/dashboard")
                    this.resetForm()
                } catch (error) {
                    console.error("Redirect error:", error);
                }

                alert("Login berhasil. Selamat datang, " + data.user.username);
            } catch (error) {
                if (error.response) {
                    alert("Login gagal: " + error.response.data.detail);
                } else {
                    alert("Terjadi kesalahan: " + error.message);
                }
            }
        }

    }
}
</script>