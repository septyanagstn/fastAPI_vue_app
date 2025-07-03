<template>
    <div class="container">
        <h2>Login</h2>
        <form @submit.prevent="login">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="username" class="form-control">
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" class="form-control">
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    methods: {
        async login() {
            try {
                const response = await axios.post('http://localhost:8000/login')
            } catch (error) {
                console.error(error);
            }
        }
    }
};
</script>