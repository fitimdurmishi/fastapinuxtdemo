<template>
  <!-- <Tutorial/> -->
  <div id="app">
    <treeselect v-model="value" :multiple="true" :options="options" />
  </div>
</template>

<script>
// import the component
import Treeselect from '@riophae/vue-treeselect'
// import the styles
import '@riophae/vue-treeselect/dist/vue-treeselect.css'

export default {
  name: 'IndexPage',
  components: {
    Treeselect,
  },
  data: () => ({
    value: [],
    options: [ {
      id: 'fruits',
      label: 'Fruits',
      children: [ {
        id: 'apple',
        label: 'Apple 🍎',
        isNew: true,
      }, {
        id: 'grapes',
        label: 'Grapes 🍇',
      }, {
        id: 'pear',
        label: 'Pear 🍐',
      }, {
        id: 'strawberry',
        label: 'Strawberry 🍓',
      }, {
        id: 'watermelon',
        label: 'Watermelon 🍉',
      } ],
    }, {
      id: 'vegetables',
      label: 'Vegetables',
      children: [ {
        id: 'corn',
        label: 'Corn 🌽',
      }, {
        id: 'carrot',
        label: 'Carrot 🥕',
      }, {
        id: 'eggplant',
        label: 'Eggplant 🍆',
      }, {
        id: 'tomato',
        label: 'Tomato 🍅',
      } ],
    } ],
  }),
}
</script>
