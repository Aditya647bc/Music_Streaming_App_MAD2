<template>
  <div>
    <nav class="navbar" style="background-color: #e3f2fd;">
      <div class="container-fluid">
        <router-link v-if="UserStatus === 'Admin'" class="navbar-brand" to='/admindashboard'>Navbar</router-link>
        <router-link v-else class="navbar-brand" to='/userdashboard'>Navbar</router-link>
        <form  @submit.prevent="searchSA" v-if="UserStatus" class="d-flex" role="search">
          <input style="width: 300px;" name="search" class="form-control me-2" type="search"
            placeholder="Search by song name and genres" aria-label="Search" v-model="search">
          <button class="btn btn-outline-primary" type="submit">Search</button>
        </form>
        <div class="flex">
          <router-link v-if="UserStatus === 'User'" class="btn btn-outline-primary mx-2" to='/registercreator'
            role="button">Register Creator</router-link>
          <router-link v-if="UserStatus === 'Creator'" class="btn btn-outline-primary mx-2" to='/creatordashboard'
            role="button">Creator Dashboard</router-link>

          <button v-if="UserStatus" class="btn btn-outline-primary" @click="logoutuser(token)"
            role="button">Logout</button>
        </div>
      </div>
    </nav><br><br>
  </div>
</template>
<script>

export default {
  data() {
    return {
      token: localStorage.getItem('token'),
      UserStatus: localStorage.getItem('auth')
    };
  },
  methods: {
    logoutuser(token) {
      fetch('http://127.0.0.1:5000/logout', {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + token
        },
      })
        .then(resp => resp.json())
        .then(data => {
          console.log(data)
          this.$router.push('/').then(() => {
            window.location.reload();
            localStorage.clear()

          });
        })
    },
    searchSA(){
      this.$router.push('/search/'+this.search)
      },
  },
}

</script>

<style></style>
