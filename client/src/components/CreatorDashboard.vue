<template>
    <div class="my-4">
        <div style="display: flex; margin-left: 420px;">
            <div>
                <div class="card" style="width: 200px; margin-right: 20px;">
                    <div class="card-body">
                        <h5>Total Songs</h5>
                        <h3>{{ totalsongs }}</h3>
                    </div>
                </div>
            </div><br>
            <div>
                <div class="card" style="width: 200px; margin-right: 20px;">
                    <div class="card-body">
                        <h5>Average Ratings</h5>
                        <h3>{{ averageratings }} </h3>
                    </div>
                </div>
            </div><br>
            <div>
                <div class="card" style="width: 200px; margin-right: 20px;">
                    <div class="card-body">
                        <h5>Total Albums</h5>
                        <h3>{{ totalalbums }}</h3>
                    </div>
                </div>
            </div><br>
        </div><br>

        <div style="display: flex;">
            <div class="container" style="text-align: center; align-items: center; width: 350px;">
                <div>
                    <h3>Create Album</h3>
                </div><br><br>
                <form  @submit.prevent="createalbum">
                    <div class="mb-3">
                        <label for="exampleInputPassword1" class="form-label">Name</label>
                        <input type="text" class="form-control" id="exampleInputPassword1" v-model="albumname">
                    </div>
                    <div class="mb-3">
                        <label for="exampleInputPassword1" class="form-label">Aritst</label>
                        <input type="text" class="form-control" id="exampleInputPassword1" v-model="artist">
                    </div>
                    <div class="mb-3">
                        <label for="exampleInputPassword1" class="form-label">Genre</label>
                        <input type="text" class="form-control" id="exampleInputPassword1" v-model="genre">
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                </form>
            </div>

            <div class="container" style="width: 850px;">
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th scope="col">SNo</th>
                            <th scope="col">Album ID</th>
                            <th scope="col">Album Name</th>
                            <th scope="col">Artist</th>
                            <th scope="col">Genre</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(album, index) in allalbums[0] " :key="album.Album_id">
                            <th scope="row">{{ index+1 }}</th>
                            <td>{{ album.Album_id }} </td>
                            <td>{{ album.Name }}</td>
                            <td>{{ album.Artist }}</td>
                            <td>{{ album.Genre }}</td>
                            <td>
                                <router-link :to="{name:'updatealbum', params:{Album_id:album.Album_id}}" class="btn btn-primary btn-sm mx-1"
                                    style="text-decoration: none; margin-right: 20px;">update</router-link>
                                <button v-on:click="deletealbum(album.Album_id)" class="btn btn-primary btn-sm mx-1"
                                    style="text-decoration: none; margin-right: 20px;">delete</button>
                                <router-link :to="{name:'addsong', params:{Album_id:album.Album_id}}" type="button"
                                    class="btn btn-primary btn-sm mx-1">Add song</router-link>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CreatorDashboard',

    data() {
        return {
            allalbums: [],
            totalsongs: 0,
            averageratings: 0,
            totalalbums: 0,
            token: localStorage.getItem('user'),
            User: localStorage.getItem('auth')
        }
    },
    methods: {
        getcreatordashboard() {
            fetch('http://127.0.0.1:5000/creatordashboard', {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + localStorage.getItem('user'),
                    "UserAuth" : localStorage.getItem('auth')
                }
            })
                .then(resp => resp.json())
                .then(data => {
                    this.allalbums.push(data.allalbums),
                    this.totalsongs=data.totalsongs,
                    this.averageratings=data.averageratings,
                    this.totalalbums=data.totalalbums,
                    console.log(data)
                })
                .catch(error => {
                    console.log(error)
                })
                
        },
        createalbum(){
            if(!this.albumname || !this.artist || !this.genre){
                this.error = "Please fill all the fields"
            }else{
                fetch('http://127.0.0.1:5000/createalbum',{
                method:"POST",
                headers:{
                    "Content-Type":"application/json",
                    "Authorization": "Bearer " + localStorage.getItem('user'),
                    "UserAuth" : localStorage.getItem('auth')
                },
                body: JSON.stringify({Name:this.albumname,Artist: this.artist, Genre: this.genre})
                })
                .then(resp => resp.json())
                .then(() =>{
                    window.location.reload();
                
                })
                .catch(error => {
                    console.log(error)
                })
            } 
        },
        deletealbum(Album_id){
        fetch(`http://127.0.0.1:5000/deletealbum/${Album_id}`,{
            method:"DELETE",
            headers:{
                "Content-Type":"application/json",
                "Authorization": "Bearer " + localStorage.getItem('user'),
                "UserAuth" : localStorage.getItem('auth')
            },
        })
          .then(() =>{
                    window.location.reload();
                })
            .catch(error => {
                console.log(error);
            });
      },
    },
    created() {
        this.getcreatordashboard()
    }
}
</script>