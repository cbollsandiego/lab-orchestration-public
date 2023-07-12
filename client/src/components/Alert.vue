<template>
    <div v-if="message !== ''">
      <div v-if="isSuccess" class="alert alert-success" role="alert">{{ this.message }}</div>
      <div v-if="!isSuccess" class="alert alert-danger" role="alert">{{ this.message }}</div>
      <br/>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      message: {type: String}, 
      isSuccess: {type: Boolean}
    }
  };
  </script> 