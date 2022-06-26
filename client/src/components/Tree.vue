<template>
  <div class="container">
    <VueFamilyTree
      :tree="treeData"
      @card-click="cardClick"
    />
  </div>
</template>

<script>
import axios from 'axios';
import VueFamilyTree from 'vue-family-tree';

export default {
  components: {
    VueFamilyTree,
  },
  data() {
    return {
      treeData: {},
    };
  },
  methods: {
    getTree() {
      const path = 'http://localhost:5000/tree';
      axios.get(path)
        .then((res) => {
          this.treeData = res.data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getTree();
  },
};
</script>
