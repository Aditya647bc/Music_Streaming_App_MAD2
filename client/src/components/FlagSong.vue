<template>
    <div class="col-9 my-4" style="text-align: center; margin-left: 170px;">
        <h2>All Songs</h2>
        <br>
        <table class="table table-light">
            <thead>
                <tr>
                    <th scope="col">Genre</th>
                    <th scope="col">Song ID</th>
                    <th scope="col">Song Name</th>
                    <th scope="col">Artist</th>
                    <th scope="col">Rating</th>
                    <th scope="col">Duration</th>
                </tr>
            </thead>
            <tbody  v-for="genre in allsongs[0]  " :key="genre">
                <tr>
                    <td class="table-primary"><strong>{{ genre.genre }}</strong></td>
                </tr>
                <tr v-for="song in genre.songs " :key="song.Song_id">
                    <td></td>
                    <td>{{ song.Song_id }} </td>
                    <td>{{ song.Name }}</td>
                    <td>{{ song.Artist }}</td>
                    <td>{{ song.Rating }}</td>
                    <td>
                        <button v-on:click="deletesong(song.Song_id)" class="btn btn-primary btn-sm mx-1"
                            style="text-decoration: none; margin-right: 20px;">delete</button>
                        <button type="button" class="btn btn-primary btn-sm" data-bs-toggle="modal"
                            :data-bs-target="'#exampleModal' + song.Song_id">
                            View Lyrics
                        </button>

                        <div class="modal fade" :id="'exampleModal' + song.Song_id" tabindex="-1"
                            aria-labelledby="exampleModalLabel" aria-hidden="true">
                            <div class="modal-dialog modal-dialog-centered">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h1 class="modal-title fs-5" id="exampleModalLabel">{{ song.Name }}</h1>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal"
                                            aria-label="Close"></button>
                                    </div>
                                    <div class="modal-body">
                                        {{ song.Lyrics }}
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary"
                                            data-bs-dismiss="modal">Close</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
export default {
    data() {
        return {
            allsongs: [],
            selectedFile: null,
            token: localStorage.getItem('user'),
            User: localStorage.getItem('auth'),
        }
    },
    methods: {
        getallsongsbygenre() {
            fetch('http://127.0.0.1:5000/admindashboard/FlagSong', {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + localStorage.getItem('user'),
                    "UserAuth": localStorage.getItem('auth')
                }
            })
                .then(resp => resp.json())
                .then(data => {
                    this.allsongs.push(data),
                        console.log(data)
                })
                .catch(error => {
                    console.log(error)
                })
        },
        deletesong(Song_id) {
            fetch(`http://127.0.0.1:5000/deletesong/${Song_id}`, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + localStorage.getItem('user'),
                    "UserAuth": localStorage.getItem('auth')
                },
            })
                .then(() => {
                    window.location.reload();
                })
                .catch(error => {
                    console.log(error);
                });
        },
    },
    created() {
        this.getallsongsbygenre()
    },
}
</script>

<style></style>
