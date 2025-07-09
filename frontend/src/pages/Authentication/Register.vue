<template>
    <div class="container bg-white p-3 border border-secondary rounded shadow d-flex flex-column align-items-center justify-content-center"
        style="max-width: 400px; margin: 40px auto 0 auto;">
        <h2 class="mb-3 text-center" style="font-weight: bold;">SignUp</h2>
        <form @submit.prevent="register()">
            <div class="form-group">
                <label for="username" class="form-label" style="font-weight: bold; font-size: large;">Username</label>
                <input type="username" v-model="username" class="form-control border" name="username"
                    placeholder="Enter your username" required>
            </div>
            <div class="form-group">
                <label for="fullname" class="form-label" style="font-weight: bold; font-size: large;">Fullname</label>
                <input type="fullname" v-model="fullname" class="form-control border" name="fullname"
                    placeholder="Enter your fullname" required>
            </div>
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
            <div class="form-group" style="position: relative;">
                <label for="confirm_password" class="form-label" style="font-weight: bold; font-size: large;">Confirm
                    Password</label>
                <input :type="showConfirmPassword ? 'text' : 'password'" class="form-control border"
                    name="confirm_password" placeholder="Re-enter your password" required v-model="confirm_password"
                    style="padding-right: 40px;">
                <button type="button" id="toggleConfirmPassword" @click="toggleConfirmPassword"
                    style="position: absolute; right: 10px; top: 38px; border: none; background: none; cursor: pointer; padding: 0;"
                    tabindex="-1">
                    <i :class="showConfirmPassword ? 'ti-eye' : 'ti-eye'"></i>
                </button>
            </div>
            <div class="w-100 mt-3 d-flex justify-content-center">
                <button type="submit" class="text-white w-100 p-2 rounded border-secondary bg-dark cursor-pointer"
                    style="font-weight: bold;">SignUp</button>
            </div>
            <div class="text-center mt-3 mb-5">
                <p>Already have an account? <span><router-link to="/login">Login</router-link></span></p>
            </div>
        </form>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "Register",

    data() {
        return {
            username: "",
            fullname: "",
            email: "",
            password: "",
            confirm_password: "",
            showPassword: false,
            showConfirmPassword: false,
            errors: [],
        };
    },
    methods:
    {
        togglePassword() {
            this.showPassword = !this.showPassword;
        },
        toggleConfirmPassword() {
            this.showConfirmPassword = !this.showConfirmPassword;
        },

        async register() {
            try {
                if (this.password != this.confirm_password) {
                    alert("Password and confirmation do not match.");
                    return;
                }

                const response = await axios.post('http://localhost:8000/register', {
                    username: this.username,
                    full_name: this.fullname,
                    email: this.email,
                    password: this.password
                });

                this.$router.push("/");
                
                const data = response.data

                alert("Selamat akun berhasil didaftarkan. Silahkan login")
            } catch (error) {
                if (error.response) {
                    alert("SignUp gagal: " + error.response.data.detail);
                } else {
                    alert("Terjadi kesalahan: " + error.message);
                }
            }
        }
    }
}
</script>