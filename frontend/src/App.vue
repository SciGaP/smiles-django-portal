<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>

export default {
  name: 'App'
};
</script>

<style scoped>
#app {
  height: 100vh;
  width: 100vw;
  overflow-x: hidden; /* Hide horizontal scrollbar */
  overflow-y: auto; /* Add vertical scrollbar if necessary */
}
</style>