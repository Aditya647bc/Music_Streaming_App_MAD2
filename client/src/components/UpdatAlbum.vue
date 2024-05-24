<template>
    <div class="my-4">
            <div class="container" style="text-align: center; align-items: center; width: 350px;">
                <div>
                    <h3>Update Album</h3>
                </div><br><br>
                <form  @submit.prevent="updatealbum">
                    <div class="mb-3">
                        <label for="exampleInputPassword1" class="form-label">Name</label>
                        <input type="text" class="form-control" id="exampleInputPassword1" v-model="Name">
                    </div>
                    <div class="mb-3">
                        <label for="exampleInputPassword1" class="form-label">Aritst</label>
                        <input type="text" class="form-control" id="exampleInputPassword1" v-model="Artist">
                    </div>
                    <div class="mb-3">
                        <label for="exampleInputPassword1" class="form-label">Genre</label>
                        <input type="text" class="form-control" id="exampleInputPassword1" v-model="Genre">
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>
    </div>
</template>

<script>
export default {
    name: 'UpdateAlbum',

    data() {
        return {
            Name:'',
            Artist:'',
            Genre:''
        }
    },
    methods: {
        getalbum() {
            fetch('http://127.0.0.1:5000/album/'+ this.$route.params.Album_id, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + localStorage.getItem('user'),
                    "UserAuth" : localStorage.getItem('auth')
                }
            })
                .then(resp => resp.json())
                .then(data => {
                    this.Name = data.Name,
                    this.Genre=data.Genre,
                    this.Artist=data.Artist
                    console.log(data)
                })
                .catch(error => {
                    console.log(error)
                })
        },
        updatealbum(){
            if(!this.Name || !this.Artist || !this.Genre){
                this.error = "Please fill all the fields"
            }else{
                fetch('http://127.0.0.1:5000/updatealbum/'+this.$route.params.Album_id,{
                method:"PUT",
                headers:{
                    "Content-Type":"application/json",
                    "Authorization": "Bearer " + localStorage.getItem('user'),
                    "UserAuth" : localStorage.getItem('auth')
                },
                body: JSON.stringify({Name:this.Name,Artist: this.Artist, Genre: this.Genre})
                })
                .then(resp => resp.json())
                .then(() =>{
                    this.$router.push('/creatordashboard')
                
                })
                .catch(error => {
                    console.log(error)
                })
            }
        }
    },
    created() {
        this.getalbum()
    }
}
</script>