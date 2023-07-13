<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">
                <img src="../assets/usd-logo-primary-thumb.png" alt="" width="72" height="42" class="d-inline-block align-text-top">
            </a>
          <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div class="navbar-nav">
              <a class="nav-link active" aria-current="page" href="#">My Courses</a>
              <a class="nav-link" href="#">Courses</a>
              <a class="nav-link" href="#">Users</a>
              <!--<router-link :to="{name: 'Create Lab'}">
                <a class="nav-link">Labs</a>
              </router-link> -->
            </div>
          </div>
          <button class="btn btn-outline-success" type="submit">Login</button>
        </div>
      </nav>
</template>

<script>
import { useLink } from 'vue-router';

export default {
    
}
</script>

<style>
    a {
        text-decoration: none;
    }
</style>