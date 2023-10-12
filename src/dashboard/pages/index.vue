<template>
  <div v-if="isAuthenticated">
    
  </div>
  <div v-else class="p-5">
    <p> You are not authenticated on the system, please login first.</p>
  </div>
</template>

<script>
  import { mapGetters } from 'vuex'

  export default {
    layout: 'Navigation',
    computed: {
      ...mapGetters(['isAuthenticated'])
    },
  }
</script>