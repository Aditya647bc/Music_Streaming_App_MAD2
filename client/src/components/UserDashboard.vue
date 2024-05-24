<template>
  <div style="display: flex;">
    <div class="col-9 mx-4">
      <h4>Songs <router-link :to="{ name: 'viewall', params: { what: 'allsongs', ID: 'all' } }"
          style="position: relative; left: 83%;" type="button" class="btn btn-primary btn-sm" title="user's login">view
          all</router-link> </h4>
      <div class="d-flex flex-wrap mx-4 my-4" v-if="allsongs.length > 0">
        <div v-for="song in allsongs[0].slice(0, 3)" :key="song.Song_id">
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

                <div class="modal fade" :id="'saveModal' + song.Song_id" tabindex="-1"
                  aria-labelledby="exampleModalLabel" aria-hidden="true">
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
                              <td> <input type="radio" class="form-check-input" :value="playlist.playlist.Name" v-model="playlistname2"
                                  name="playlist"> {{
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

      <h4>Albums <router-link :to="{ name: 'viewall', params: { what: 'allalbums', ID: 'all' } }"
          style="position: relative; left: 83%;" type="button" class="btn btn-primary btn-sm" title="user's login">view
          all</router-link></h4>
      <div v-if="allalbums.length" class="d-flex flex-wrap mx-4 my-4">
        <div v-for="album in allalbums[0].slice(0,5)" :key="album.Album_id">
          <div class="card border-primary mb-3 mx-2" style="width: 12.2rem;">
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

    <div class="col-2">
      <h4 class="text-center">Your Playlists</h4>
      <div class="my-4" v-for="playlist in allplaylist[0]" :key="playlist.Playlist_id">
        <div class="card border-primary mb-3 mx-2" style="max-width: 15rem;">
          <div class="card-header">{{ playlist['playlist'].Name }} <router-link
              :to="{ name: 'viewall', params: { what: 'playlist', ID: playlist['playlist'].Playlist_id } }"
              style="position: relative; left: 5em;" type="button" class="btn btn-primary btn-sm">Go</router-link>
          </div>
          <div class="card-body">
            <p class="card-text" v-for="song in playlist['songs'].slice(0, 4)" :key="song.Song_id">
              <router-link :to="{ name: 'song', params: { Song_id: song.Song_id } }" class="link"
                style="text-decoration: none; margin-right: 20px;">{{ song.Name }}</router-link>
            </p>
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
      allplaylist: [],
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
            console.log(data[0].Song_list[0])
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
        this.$router.push('/viewall/playlist/'+ data.ID).then(() => {
                                window.location.reload();
                            })
      })
      .catch(error => {
        console.log(error)
      })

    },



  },
  created() {
    this.getallsongs();
    this.getallalbums();
    this.getallplaylist();
  }
}
</script>

<style scoped></style>