<template>
  <NavBar :key="$route.fullPath"></NavBar>
  <RouterView />
</template>

<script setup>
import { RouterView } from 'vue-router'
import NavBar from './components/NavBar.vue'
</script>