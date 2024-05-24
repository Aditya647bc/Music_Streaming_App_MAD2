<template>
  <div id="app">
    <BaseNav/>
    <router-view></router-view>
  </div>
</template>

<script>
import BaseNav from './components/BaseNav.vue'
export default {
  name: 'App',
  components: {
    BaseNav
  }
}
</script>

<style>

</style>
