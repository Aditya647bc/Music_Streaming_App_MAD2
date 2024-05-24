<!-- Home.vue -->
<template>
  <div class="container" style="text-align: center; align-items: center; margin-top: 50px;">
    <div>
      <router-link class="btn btn-warning" to="/adminlogin" role="button">Admin Login</router-link>
    </div> <br><br> <br>
    <div>
      <router-link class="btn btn-primary mx-2" to="/login" role="button">User Login</router-link>
      <router-link class="btn btn-primary mx-2" to="/signup" role="button">User Signup</router-link>
    </div>
  </div>
</template>

<script>
export default {
  // Component logic
};
</script>