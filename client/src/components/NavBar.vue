<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">
                <img src="../assets/usd-logo-primary-thumb.png" alt="" width="72" height="42" class="d-inline-block align-text-top">
            </a>
          <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div class="navbar-nav">
              <router-link :to="{name: 'My Courses'}" class="route-link">
                <a class="nav-link active">My Courses</a>
              </router-link>
              <router-link :to="{name: 'Course List'}" class="route-link">
                <a class="nav-link">Courses</a>
              </router-link>
              <router-link :to="{name: 'User List'}" class="route-link">
                <a class="nav-link">Users</a>
              </router-link>
              <a class="nav-link">Labs</a>
            </div>
          </div>
          <router-link :to="{name: 'Login'}">
            <button v-if="!loggedIn" class="btn btn-outline-success" type="submit">Login</button>
          </router-link>
          <button v-if="loggedIn" class="btn btn-outline-danger" type="submit" @click="logout">Logout</button>
        </div>
      </nav>
</template>

<script>
import { useLink } from 'vue-router';

export default {
    data() {
        return {
            loggedIn: false
        }
    },
    mounted() {
        if(localStorage.getItem('token')) {
            this.loggedIn = true
        }
    },
    methods: {
        logout(){
            if(this.loggedIn) {
                localStorage.removeItem('token')
                this.loggedIn = false
                this.$router.push({name: 'Login'})
            }
        }
    },
    
}
</script>

<style>
    .route-link {
        text-decoration: none;
    }
</style>