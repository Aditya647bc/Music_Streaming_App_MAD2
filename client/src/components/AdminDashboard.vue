<template>
  <div>
  <div style="display: flex; margin-left: 370px;">
    <div>
      <div class="card" style="width: 150px; margin-right: 20px;">
        <div class="card-body">
          <h5>General Users </h5>
          <h3>{{ alldata[0].user_count }}</h3>
        </div>
      </div>
    </div><br>
    <div>
      <div class="card" style="width: 150px; margin-right: 20px;">
        <div class="card-body">
          <h5>Creator</h5>
          <h3>{{ alldata[0].creator_count }} </h3>
        </div>
      </div>
    </div><br>
    <div>
      <div class="card" style="width: 170px; margin-right: 20px;">
        <div class="card-body">
          <h5>Songs</h5>
          <h3>{{ alldata[0].song_count }} <router-link class="btn btn-primary mx-2" to="/flagsong" role="button">Flag Song</router-link></h3>
        </div>
      </div>
    </div><br>
    <div>
      <div class="card" style="width: 150px; margin-right: 20px;">
        <div class="card-body">
          <h5>Albums</h5>
          <h3>{{ alldata[0].album_count }} </h3>
        </div>
      </div>
    </div><br>
    <div>
      <div class="card" style="width: 150px;">
        <div class="card-body">
          <h5>Genres</h5>
          <h3>{{ alldata[0].genre_count }}</h3>
        </div>
      </div>
    </div>
  </div>

    <div style="display: flex; margin-left: 220px;">
      <div>
        <img :src="`data:image/png;base64,${alldata[0].graph_html}`" alt="Graph" style="width: 80%;" />
      </div>
      <div>
        <img :src="`data:image/png;base64,${alldata[0].pie_chart_html}`" alt="Pie Chart" style="width: 80%;" />
      </div>
    </div>

  </div>
</template>


<script>
export default {
  data() {
    return {
      UserStatus: localStorage.getItem('auth'),
      alldata: [],
    }
  },
  methods: {
    getadmindashboard() {
      fetch('http://127.0.0.1:5000/admindashboard', {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + localStorage.getItem('user'),
          "UserAuth": localStorage.getItem('auth')
        }
      })
        .then(resp => resp.json())
        .then(data => {
          this.alldata.push(data),
            console.log(data)
        })
        .catch(error => {
          console.log(error)
        })
    },
  },
  created() {
    this.getadmindashboard();
  }
}
</script>

<style scoped></style>