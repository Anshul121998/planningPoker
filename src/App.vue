<template>
  <v-app>
    <v-app-bar app dark class="deep-purple darken-3" dense>
      <div class="d-flex align-center">
        <v-img alt="logo" class="shrink mr-2" contain :src="require('@/assets/logo.png')" transition="scale-transition" width="26" />
        <h2 class="mr-2">Planning Poker</h2>
      </div>
      <v-spacer></v-spacer>
      <v-btn href="#" target="_blank" text>
        <span class="mr-2">Feedback</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
      <template v-slot:extension>
        <v-tabs>
          <v-tab to="/joinroom">Join Room</v-tab>
          <v-tab to="/createroom">Create Room</v-tab>
          <v-tab to="/about">About</v-tab>
        </v-tabs>
      </template>
    </v-app-bar>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'App'
}
</script>
