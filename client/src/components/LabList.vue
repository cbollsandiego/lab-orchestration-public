<template>
    <div class="full-page">
        <div class="container">
        <router-link :to="{ name: 'Lab Create' }" class="route-link">
            <button class="create-lab-button">
                <a class="nav-link">New Lab</a>
            </button>
        </router-link>
        <table class="table table-striped table-bordered">
            <thead>
                <tr>
                    <th>Lab Title</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="lab in labs">
                    <td>
                        <router-link :to="{name: 'Lab Create', params: {labName: lab.title}}" class="route-link">
                            {{ lab.title }}
                        </router-link>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    </div>
</template>

<script>
import axios from 'axios';
export default {
    data() {
        return {
            labs: []
        }
    },
    created() {
        this.getLabs()
    },
    methods: {
        getLabs() {
            const path = `http://localhost:5001/lablist`;
            const accessToken = localStorage.getItem('token');
            axios.get(path, {headers: {'Authorization': accessToken}})
                .then((res) => {
                    this.labs = res.data;
                })
                .catch((error) => {
                    console.log(error)
                    this.$router.push({ name: 'Login'})
                })
        }
    }
}
</script>

<style>
.full-page {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #f2f2f2;
    padding: 20px;
  }

.create-lab-button {
    background-color: #4caf50;
    color: #fff;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 5px;
  }
</style>