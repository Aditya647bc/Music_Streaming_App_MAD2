<template>
  <div>
    <div  v-if="allsongs.length > 0 && this.$route.params.what === 'allsongs'">
      <div class="text-center"> <h2>All Songs</h2></div>
      <div class="d-flex flex-wrap mx-4 my-4">
      <div v-for="song in allsongs[0]" :key="song.Song_id">
        <div class="card border-primary mb-3 mx-2" style="max-width: 21rem;">
          <div class="card-header">{{ song.Genre }} <span style="position: absolute; right: 5%;">{{ song.Rating }}
              <img src="../assets/star.png" alt="" width="15"></span>
          </div>
          <div class="card-body text-center">
            <p class="card-title"><strong>{{ song.Name }} </strong></p>
            <p class="card-title">{{ song.Artist }} </p>
            <p class="card-text">

              <audio controls>
                <source :src="get_url_for(song.Song_path)" type="audio/mp3">
              </audio>
            </p>
            <div class="d-flex" style="position: relative; left: 17%;">
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
                      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                      {{ song.Lyrics }}
                    </div>
                    <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                  </div>
                </div>
              </div>
              &nbsp;
              <button type="button" class="btn btn-primary btn-sm" data-bs-toggle="modal"
                :data-bs-target="'#saveModal' + song.Song_id">
                +save
              </button>

              <div class="modal fade" :id="'saveModal' + song.Song_id" tabindex="-1" aria-labelledby="exampleModalLabel"
                aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h1 class="modal-title fs-5" id="exampleModalLabel">Playlists</h1>
                      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                      <form @submit.prevent="createplaylist(song.Song_id)">
                        <div class="mb-3">
                          <label class="form-label"><strong>Palylist Name</strong></label>
                          <input type="text" class="form-control" name="name" id="playlistname" v-model="playlistname"
                            aria-describedby="emailHelp">
                        </div>
                        <div>
                          <div v-for="playlist in allplaylist[0]" :key="playlist.Playlist_id">
                            <td> <input type="radio" class="form-check-input" :value="playlist.playlist.Name"
                                v-model="playlistname2" name="playlist"> {{
                                  playlist.playlist.Name }}</td>
                          </div>
                        </div>
                        <br>
                        <button type="submit" class="btn btn-primary">save</button>
                      </form>
                    </div>
                    <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                  </div>
                </div>
              </div>

              <div class="dropdown">
                <button class="btn btn-secondary dropdown-toggle btn-sm mx-1" role="button" data-bs-toggle="dropdown"
                  aria-expanded="false">
                  Rate
                </button>

                <ul class="dropdown-menu">
                  <li><button class="dropdown-item" @click="rate(1, song.Song_id)">1</button></li>
                  <li><button class="dropdown-item" @click="rate(2, song.Song_id)">2</button></li>
                  <li><button class="dropdown-item" @click="rate(3, song.Song_id)">3</button></li>
                  <li><button class="dropdown-item" @click="rate(4, song.Song_id)">4</button></li>
                  <li><button class="dropdown-item" @click="rate(5, song.Song_id)">5</button></li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    </div>


    <div v-if="allplaylist.length > 0 && allplaylist[0].songs && this.$route.params.what === 'playlist'">
      <div class="text-center">
        <h2> {{ allplaylist[0].playlist.Name }}</h2> <button v-on:click="deleteplaylist()" type="button"
          class="btn btn-danger btn-sm">
          Delete
        </button>
      </div>
      <div class="d-flex flex-wrap mx-4 my-4">
        <div v-for="song in allplaylist[0]['songs']" :key="song.Song_id">
          <div class="card border-primary mb-3 mx-2" style="max-width: 21rem;">
            <div class="card-header">{{ song.Genre }} <span style="position: absolute; right: 5%;">{{ song.Rating }}
                <img src="../assets/star.png" alt="" width="15"></span>
            </div>
            <div class="card-body text-center">
              <p class="card-title"><strong>{{ song.Name }} </strong></p>
              <p class="card-title">{{ song.Artist }} </p>
              <p class="card-text">

                <audio controls>
                  <source :src="get_url_for(song.Song_path)" type="audio/mp3">
                </audio>
              </p>
              <div class="d-flex" style="position: relative; left: 17%;">
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
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                      </div>
                      <div class="modal-body">
                        {{ song.Lyrics }}
                      </div>
                      <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                      </div>
                    </div>
                  </div>
                </div>
                &nbsp;
                <button v-on:click="removesong(song.Song_id)" type="button" class="btn btn-primary btn-sm">
                  remove
                </button>

                <div class="dropdown">
                  <button class="btn btn-secondary dropdown-toggle btn-sm mx-1" role="button" data-bs-toggle="dropdown"
                    aria-expanded="false">
                    Rate
                  </button>

                  <ul class="dropdown-menu">
                    <li><button class="dropdown-item" @click="rate(1, song.Song_id)">1</button></li>
                    <li><button class="dropdown-item" @click="rate(2, song.Song_id)">2</button></li>
                    <li><button class="dropdown-item" @click="rate(3, song.Song_id)">3</button></li>
                    <li><button class="dropdown-item" @click="rate(4, song.Song_id)">4</button></li>
                    <li><button class="dropdown-item" @click="rate(5, song.Song_id)">5</button></li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>


    <div v-if="allalbums.length > 0 && this.$route.params.what === 'allalbums'">
      <div class="text-center"> <h2>All Albums</h2></div>
      <div class="d-flex flex-wrap mx-4 my-4">
        <div v-for="album in allalbums[0]" :key="album.Album_id">
          <div class="card border-primary mb-3 mx-2" style="width: 14rem;">
            <div class="card-header">{{ album.Genre }}</div>
            <div class="card-body">
              <h5 class="card-title">{{ album.Name }}</h5>
              <p class="card-text">{{ album.Artist }}</p>
              <router-link :to="{ name: 'albumsong', params: {Name:album.Name, ID: album.Album_id } }"
           type="button" class="btn btn-primary btn-sm" title="user's login">All Songs</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>


<script>
export default {
  name: 'UserDashboard',

  data() {
    return {
      UserStatus: localStorage.getItem('auth'),
      allsongs: [],
      allalbums: [],
      allplaylist: []
    }
  },
  methods: {
    get_url_for(Song_path) {
      return require(`@/assets/${Song_path}`);
    },
    getallsongs() {
      fetch('http://127.0.0.1:5000/allsongs', {
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
            console.log(data.slice(0, 3))
        })
        .catch(error => {
          console.log(error)
        })
    },
    getallplaylist() {
      if (this.$route.params.ID === 'all') {
        fetch('http://127.0.0.1:5000/playlistsongs', {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem('user'),
            "UserAuth": localStorage.getItem('auth')
          }
        })
          .then(resp => resp.json())
          .then(data => {
            this.allplaylist.push(data),
              console.log(data[0])
          })
          .catch(error => {
            console.log(error)
          })
      } else {
        fetch('http://127.0.0.1:5000/playlistsongs/' + this.$route.params.ID, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem('user'),
            "UserAuth": localStorage.getItem('auth')
          }
        })
          .then(resp => resp.json())
          .then(data => {
            this.allplaylist.push(data),
              console.log(data[0])
          })
          .catch(error => {
            console.log(error)
          })
      }
    },
    rate(rating, Song_id) {
      fetch(`http://127.0.0.1:5000/ratesong/${Song_id}/${rating}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + localStorage.getItem('user'),
          "UserAuth": localStorage.getItem('auth')
        }
      })
        .then(resp => resp.json())
        .then(data => {
          console.log(data)
          window.location.reload();

        })
        .catch(error => {
          console.log(error)
        })

    },
    getallalbums() {
      fetch('http://127.0.0.1:5000/allalbums/all', {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + localStorage.getItem('user'),
          "UserAuth": localStorage.getItem('auth')
        }
      })
        .then(resp => resp.json())
        .then(data => {
          this.allalbums.push(data),
            console.log(data)
        })
        .catch(error => {
          console.log(error)
        })
    },
    removesong(Song_id) {
      fetch(`http://127.0.0.1:5000/removesong/${Song_id}/` + this.$route.params.ID, {
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
    deleteplaylist() {
      fetch(`http://127.0.0.1:5000/deleteplaylist/` + this.$route.params.ID, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + localStorage.getItem('user'),
          "UserAuth": localStorage.getItem('auth')
        },
      })
        .then(resp => resp.json())
        .then(() => {
          this.$router.push('/userdashboard')

        }).catch(error => {
          console.error("Error:", error);
        });
    },

    createplaylist(Song_id) {
      let P_Name = null
      if (this.playlistname) {
        P_Name = this.playlistname
      } else if (this.playlistname2) {
        P_Name = this.playlistname2
      }
      fetch('http://127.0.0.1:5000/createplaylist', {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + localStorage.getItem('user'),
          "UserAuth": localStorage.getItem('auth')
        },
        body: JSON.stringify({ Name: P_Name, Songs_list: [Song_id] })
      })
        .then(resp => resp.json())
        .then(data => {
          this.$router.push('/viewall/playlist/' + data.ID).then(() => {
            window.location.reload();
          })
        })
        .catch(error => {
          console.log(error)
        })

    },

  },

  created() {
    this.getallplaylist();
    this.getallsongs();
    this.getallalbums()
  }
}
</script>

<style scoped></style>