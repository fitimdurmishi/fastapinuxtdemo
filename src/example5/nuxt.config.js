export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'example5',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
      { name: 'format-detection', content: 'telephone=no' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    '~/plugins/bootstrap-vue.js'
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    '@nuxtjs/axios',
    'bootstrap-vue/nuxt',
  ],

  axios: {
    // extra config e.g
    baseURL: process.env.API_URL,
  },

  proxy: {
    '/api/': 'http://127.0.0.1:8000'  // we do this beacuse of CORS
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
  }
}
