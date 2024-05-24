<template>
  <div class="my-6">
    <div class="container" style="text-align: center; align-items: center; width: 550px;">
      <div>
        <h3>Update Song</h3>
      </div><br><br>
      <form @submit.prevent="updatesong">
        <div class="mb-3">
          <label for="songname" class="form-label">Song Name</label>
          <input type="text" class="form-control" v-model="Name" id="songname">
        </div>
        <div class="mb-3">
          <label for="lyrics" class="form-label">Lyrics</label>
          <textarea type="text" class="form-control" v-model="Lyrics" id="lyrics"></textarea>
        </div>
        <div class="mb-3">
          <label for="artist" class="form-label">Artist</label>
          <input type="text" class="form-control" v-model="Artist" id="artist">
        </div>
        <div class="mb-3">
          <label for="venuecapacity" class="form-label">Genre</label>
          <input type="text" class="form-control" v-model="Genre" id="genre">
        </div>
        <div class="mb-3">
          <label for="song" class="form-label">Select an MP3 File</label>
          <input type="file" @change="onFileChange" accept=".mp3" class="form-control">
        </div>
        <br>
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
      Name: '',
      Artist: '',
      Genre: '',
      Lyrics: '',
      Album_id: 0,
      selectedFile: null,
    }
  },
  methods: {
    getsong() {
      fetch('http://127.0.0.1:5000/song/' + this.$route.params.Song_id, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + localStorage.getItem('user'),
          "UserAuth": localStorage.getItem('auth')
        }
      })
        .then(resp => resp.json())
        .then(data => {
          this.Name = data.Name,
            this.Genre = data.Genre,
            this.Artist = data.Artist,
            this.Lyrics = data.Lyrics,
            this.Album_id = data.Album_id
          console.log(data)
        })
        .catch(error => {
          console.log(error)
        })
    },
    onFileChange(e) {
      this.selectedFile = e.target.files[0];
    },
    updatesong() {
      if (!this.Name || !this.Lyrics || !this.Genre || !this.Artist) {
        this.error = "Please fill all the fields";
        return;
      }

      let formData = new FormData();
      formData.append('Name', this.Name);
      formData.append('Lyrics', this.Lyrics);
      formData.append('Genre', this.Genre);
      formData.append('Artist', this.Artist);
      formData.append('Song_file', this.selectedFile);

      fetch('http://127.0.0.1:5000/updatesong/' + this.$route.params.Song_id, {
        method: "PUT",
        headers: {
          "Authorization": "Bearer " + localStorage.getItem('user'),
          "UserAuth": localStorage.getItem('auth')
        },
        body: formData
      })
        .then(resp => resp.json())
        .then(() => {
          this.$router.push('/addsong/' + this.Album_id)

        }).catch(error => {
          console.error("Error:", error);
        });
    },
  },
  created() {
    this.getsong()
  }
}
</script>