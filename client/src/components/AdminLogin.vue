<template>
  <div class="container" style="text-align: center; align-items: center; margin-top: 50px; width: 350px;">
      <h1>Admin Login</h1>
      <form @submit.prevent="adminlogin">
          <div class="mb-3">
              <label for="exampleInputPassword1" class="form-label">UserName</label>
              <input type="text" class="form-control" id="exampleInputPassword1" v-model="UserName">
          </div>
          <div class="mb-3">
              <label for="exampleInputPassword1" class="form-label">Password</label>
              <input type="password" class="form-control" id="exampleInputPassword1" v-model="Password">
          </div>

          <button type="submit" class="btn btn-primary">Submit</button>
      </form>
  </div>
</template>




<script>
export default {
    methods: {
        adminlogin() {
            if (!this.Password || !this.UserName) {
                console.log("Error")
            } else {
                fetch('http://127.0.0.1:5000/adminlogin', {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        UserName: this.UserName,
                        Password: this.Password,
                    })
                })
                    .then(resp => resp.json())
                    .then(data => {
                        if (data === 401) {
                            this.msg.push("Please login with correct username and password.")
                            console.log(data)
                        }
                        else {
                            localStorage.setItem('user', data.token);
                            localStorage.setItem('auth', data.User);
                            localStorage.setItem('username', data.UserName);
                            this.$router.push('/admindashboard').then(() => {
                                window.location.reload();
                            })
                        }
                    },
                    )
                    .catch(error => {
                        console.log(error)
                    })

            }
        },
    }
}
</script>
