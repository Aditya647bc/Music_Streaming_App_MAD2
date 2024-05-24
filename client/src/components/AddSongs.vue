<template>
    <div style="display: flex;">
        <div class="container" style="text-align: center; align-items: center; width: 350px;">
            <h2>Add Song</h2>
            <form @submit.prevent="createsong">
                <div class="mb-3">
                    <label for="songname" class="form-label">Song Name</label>
                    <input type="text" class="form-control" v-model="songname" id="songname">
                </div>
                <div class="mb-3">
                    <label for="lyrics" class="form-label">Lyrics</label>
                    <textarea type="text" class="form-control" v-model="lyrics" id="lyrics"></textarea>
                </div>
                <div class="mb-3">
                    <label for="artist" class="form-label">Artist</label>
                    <input type="text" class="form-control" v-model="artist" id="artist">
                </div>
                <div class="mb-3">
                    <label for="venuecapacity" class="form-label">Genre</label>
                    <input type="text" class="form-control" v-model="genre" id="genre">
                </div>
                <div class="mb-3">
                    <label for="song" class="form-label">Select an MP3 File</label>
                    <input type="file" @change="onFileChange" accept=".mp3" required class="form-control">
                </div>
                <br>
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
        </div>

        <div class="container" style="width: 850px;">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">SNo</th>
                        <th scope="col">Song Name</th>
                        <th scope="col">Genre</th>
                        <th scope="col">Artist</th>
                        <th scope="col">Rating</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(song, index) in  allsongs[0]  " :key="song.Song_id">
                        <th scope="row">{{ index + 1 }}</th>
                        <td>{{ song.Name }} </td>
                        <td>{{ song.Genre }}</td>
                        <td>{{ song.Artist }}</td>
                        <td>{{ song.Rating }}</td>
                        <td>
                            <router-link :to="{ name: 'updatesong', params: { Song_id: song.Song_id } }"
                                class="btn btn-primary btn-sm mx-1"
                                style="text-decoration: none; margin-right: 20px;">update</router-link>
                            <button v-on:click="deletesong(song.Song_id)" class="btn btn-primary btn-sm mx-1"
                                style="text-decoration: none; margin-right: 20px;">delete</button>

                            <button type="button" class="btn btn-primary btn-sm" data-bs-toggle="modal"
                            :data-bs-target="'#exampleModal' + song.Song_id">
                                View Lyrics
                            </button>

                            <div class="modal fade" :id="'exampleModal' + song.Song_id" tabindex="-1" aria-labelledby="exampleModalLabel"
                                aria-hidden="true">
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
    </div>
</template>

<script>
export default {
    name: 'AddSong',

    data() {
        return {
            allsongs: [],
            selectedFile: null,
            token: localStorage.getItem('user'),
            User: localStorage.getItem('auth'),
        }
    },
    methods: {
        getallsongs() {
            fetch('http://127.0.0.1:5000/songs/' + this.$route.params.Album_id, {
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
        onFileChange(e) {
            this.selectedFile = e.target.files[0];
        },
        createsong() {
            if (!this.songname || !this.lyrics || !this.genre || !this.artist || !this.selectedFile) {
                this.error = "Please fill all the fields";
                return;
            }

            let formData = new FormData();
            formData.append('Name', this.songname);
            formData.append('Lyrics', this.lyrics);
            formData.append('Genre', this.genre);
            formData.append('Artist', this.artist);
            formData.append('Song_file', this.selectedFile);

            fetch('http://127.0.0.1:5000/createsong/' + this.$route.params.Album_id, {
                method: "POST",
                headers: {
                    "Authorization": "Bearer " + localStorage.getItem('user'),
                    "UserAuth": localStorage.getItem('auth')
                },
                body: formData
            })
                .then(resp => resp.json())
                .then(() => {
                    window.location.reload();

                }).catch(error => {
                    console.error("Error:", error);
                });
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
        this.getallsongs()
    },
}
</script>

<style scoped></style>
