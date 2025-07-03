<template>
    <form @submit.prevent="login">
        <button type="submit" class="btn btn-primary">Login</button>
    </form>
</template>

<script>
import axios from 'axios';

export default {
    name: 'Index',
    methods: {
        index() {
            axios.get('http://localhost:8000/dashboard')
                .then(response => {
                    console.log(response.data);
                })
                .catch(error => {
                    console.error(error);
                });
        }
    }
};
</script>