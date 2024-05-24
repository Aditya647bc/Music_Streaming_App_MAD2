<template>
  <div>
    <div  v-if="songs_g != null" class="container" style=" align-items: center; margin-top: 50px; width: 450px;">
      <div class="card border-primary mb-3 mx-2" style="max-width: 21rem;">
        <div class="card-header">{{ songs_g[0].Genre }} <span style="position: absolute; right: 5%;">{{ songs_g[0].Rating }}
            <img src="../assets/star.png" alt="" width="15"></span>
        </div>
        <div class="card-body text-center">
          <p class="card-title"><strong>{{ songs_g[0].Name }} </strong></p>
          <p class="card-title">{{ songs_g[0].Artist }} </p>
          <p class="card-text">

            <audio controls>
              <source :src="get_url_for(songs_g[0].Song_path)" type="audio/mp3">
            </audio>
          </p>
          <div class="d-flex" style="position: relative; left: 17%;">
            <button type="button" class="btn btn-primary btn-sm" data-bs-toggle="modal"
              :data-bs-target="'#exampleModal' + songs_g[0].Song_id">
              View Lyrics
            </button>
            <div class="modal fade" :id="'exampleModal' + songs_g[0].Song_id" tabindex="-1"
              aria-labelledby="exampleModalLabel" aria-hidden="true">
              <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                  <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">{{ songs_g[0].Name }}</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                  </div>
                  <div class="modal-body">
                    {{ songs_g[0].Lyrics }}
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                  </div>
                </div>
              </div>
            </div>
            &nbsp;
            <button type="button" class="btn btn-primary btn-sm" data-bs-toggle="modal"
              :data-bs-target="'#saveModal' + songs_g[0].Song_id">
              +save
            </button>

            <div class="modal fade" :id="'saveModal' + songs_g[0].Song_id" tabindex="-1" aria-labelledby="exampleModalLabel"
              aria-hidden="true">
              <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                  <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Playlists</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                  </div>
                  <div class="modal-body">
                    <form @submit.prevent="createplaylist(songs_g[0].Song_id)">
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
                <li><button class="dropdown-item" @click="rate(1, songs_g[0].Song_id)">1</button></li>
                <li><button class="dropdown-item" @click="rate(2, songs_g[0].Song_id)">2</button></li>
                <li><button class="dropdown-item" @click="rate(3, songs_g[0].Song_id)">3</button></li>
                <li><button class="dropdown-item" @click="rate(4, songs_g[0].Song_id)">4</button></li>
                <li><button class="dropdown-item" @click="rate(5, songs_g[0].Song_id)">5</button></li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div  v-if="songs_n != null" class="container" style=" align-items: center; margin-top: 50px; width: 450px;">
      <div class="card border-primary mb-3 mx-2" style="max-width: 21rem;">
        <div class="card-header">{{ songs_n[0].Genre }} <span style="position: absolute; right: 5%;">{{ songs_n[0].Rating }}
            <img src="../assets/star.png" alt="" width="15"></span>
        </div>
        <div class="card-body text-center">
          <p class="card-title"><strong>{{ songs_n[0].Name }} </strong></p>
          <p class="card-title">{{ songs_n[0].Artist }} </p>
          <p class="card-text">

            <audio controls>
              <source :src="get_url_for(songs_n[0].Song_path)" type="audio/mp3">
            </audio>
          </p>
          <div class="d-flex" style="position: relative; left: 17%;">
            <button type="button" class="btn btn-primary btn-sm" data-bs-toggle="modal"
              :data-bs-target="'#exampleModal' + songs_n[0].Song_id">
              View Lyrics
            </button>
            <div class="modal fade" :id="'exampleModal' + songs_n[0].Song_id" tabindex="-1"
              aria-labelledby="exampleModalLabel" aria-hidden="true">
              <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                  <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">{{ songs_n[0].Name }}</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                  </div>
                  <div class="modal-body">
                    {{ songs_n[0].Lyrics }}
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                  </div>
                </div>
              </div>
            </div>
            &nbsp;
            <button type="button" class="btn btn-primary btn-sm" data-bs-toggle="modal"
              :data-bs-target="'#saveModal' + songs_n[0].Song_id">
              +save
            </button>

            <div class="modal fade" :id="'saveModal' + songs_n[0].Song_id" tabindex="-1" aria-labelledby="exampleModalLabel"
              aria-hidden="true">
              <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                  <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Playlists</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                  </div>
                  <div class="modal-body">
                    <form @submit.prevent="createplaylist(songs_n[0].Song_id)">
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
                <li><button class="dropdown-item" @click="rate(1, songs_n[0].Song_id)">1</button></li>
                <li><button class="dropdown-item" @click="rate(2, songs_n[0].Song_id)">2</button></li>
                <li><button class="dropdown-item" @click="rate(3, songs_n[0].Song_id)">3</button></li>
                <li><button class="dropdown-item" @click="rate(4, songs_n[0].Song_id)">4</button></li>
                <li><button class="dropdown-item" @click="rate(5, songs_n[0].Song_id)">5</button></li>
              </ul>
            </div>
          </div>
        </div>
      </div>
  </div>
    <div  v-if="album_n != null" class="container" style=" align-items: center; margin-top: 50px; width: 450px;">
      <div class="card border-primary mb-3 mx-2" style="width: 12.2rem;">
            <div class="card-header">{{ album_n[0].Genre }}</div>
            <div class="card-body">
              <h5 class="card-title">{{ album_n[0].Name }}</h5>
              <p class="card-text">{{ album_n[0].Artist }}</p>
              <router-link :to="{ name: 'albumsong', params: {Name:album_n[0].Name, ID: album_n[0].Album_id } }"
           type="button" class="btn btn-primary btn-sm" title="user's login">All Songs</router-link>
            </div>
          </div>
    </div>
      <div v-if="album_g != null" class="container" style=" align-items: center; margin-top: 50px; width: 450px;">
        <div class="card border-primary mb-3 mx-2" style="width: 12.2rem;">
            <div class="card-header">{{ album_g[0].Genre }}</div>
            <div class="card-body">
              <h5 class="card-title">{{ album_g[0].Name }}</h5>
              <p class="card-text">{{ album_g[0].Artist }}</p>
              <router-link :to="{ name: 'albumsong', params: {Name:album_g[0].Name, ID: album_g[0].Album_id } }"
           type="button" class="btn btn-primary btn-sm" title="user's login">All Songs</router-link>
            </div>
          </div>
    </div>
  </div>
</template>


<script>
export default {
  data() {
    return {
      UserStatus: localStorage.getItem('auth'),
      songs_g : null,
      songs_n : null,
      album_g : null,
      album_n : null,
      allplaylist: []
    }
  },
  methods: {
    get_url_for(Song_path) {
      return require(`@/assets/${Song_path}`);
    },
    getsearchresult() {
      fetch('http://127.0.0.1:5000/search', {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + localStorage.getItem('user'),
          "UserAuth": localStorage.getItem('auth')
        },
        body: JSON.stringify({
                        SearchField: this.$route.params.What
                    })
      })
        .then(resp => resp.json())
        .then(data => {
          if (data[0].length > 0){this.songs_g = data[0]}
          if (data[1].length > 0){this.songs_n = data[1]}
          if (data[2].length > 0){this.album_g = data[2]}
          if (data[3].length > 0){this.album_n = data[3]}
          
          
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
            console.log(data[0])
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
    this.getsearchresult();
  }
}
</script>

<style scoped></style>