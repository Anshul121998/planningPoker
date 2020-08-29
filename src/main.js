import Vue from 'vue'
import '@mdi/font/css/materialdesignicons.css'
import vuetify from '@/plugins/vuetify'
import App from './App.vue'
import router from './router'

Vue.config.productionTip = false

new Vue({
  router,
  vuetify,
  icons: {
    iconfont: 'mdi' // default - only for display purposes
  },
  render: h => h(App)
}).$mount('#app')
