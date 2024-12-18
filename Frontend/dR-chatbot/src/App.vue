<template>
  <div id="app">
    <img class="main-logo" alt="dReveal logo" src="./assets/logo-dreveal.png">
    <ChatView />
  </div>
</template>

<script>
import ChatView from './components/ChatView.vue';

export default {
  name: 'App',
  components: {
    ChatView,
  },
};
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  margin: 20px;
}

.main-logo {
  display: block;
  margin: 0 auto;
  width: 20vw;
}
  
.error {
    color: red;
    font-weight: bold;
}
</style>
