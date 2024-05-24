<template>
    <div class="container" style="text-align: center; align-items: center; margin-top: 50px; width: 350px;">
        <div>
            <h1>Register as a Creator</h1>
        </div><br><br>
        <form @submit.prevent="registercreator">
            <div class="mb-3">
                <label for="exampleInputPassword1" class="form-label">UserName</label>
                <input v-model="UserName" type="text" class="form-control" id="exampleInputPassword1" name="username">
            </div>
            <div class="mb-3">
                <label for="exampleInputPassword1" class="form-label">Password</label>
                <input v-model="Password" type="password" class="form-control" id="exampleInputPassword1"
                    name="password">
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
</template>


<script>
export default {
    methods: {
        registercreator() {
            if (!this.Password || !this.UserName) {
                console.log("Error")
            } else {
                fetch('http://127.0.0.1:5000/registercreator', {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer " + localStorage.getItem('user'),
                        "UserAuth": localStorage.getItem('auth')
                    },
                    body: JSON.stringify({
                        UserName: this.UserName,
                        Password: this.Password,
                    })
                })
                    .then(resp => resp.json())
                    .then(() => {
                        localStorage.setItem('auth', "Creator");
                        this.$router.push('/creatordashboard').then(() => {
                            window.location.reload();
                        })

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