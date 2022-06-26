<template>
            <div id="tree" ref="tree"></div>
        </template>

<script>

import FamilyTree from '@balkangraph/familytree.js';

export default {

  name: 'tree',
  data() {
    return {
      nodes: [
        {
          id: 1, pids: [2], name: 'Manou', gender: 'female', img: 'https://cdn.balkan.app/shared/2.jpg',
        },
        {
          id: 7, pids: [6], name: 'Inconnu', gender: 'male', img: 'https://cdn.balkan.app/shared/m30/5.jpg',
        },
        {
          id: 2, pids: [1], name: 'Papounet', gender: 'male', img: 'https://cdn.balkan.app/shared/m30/5.jpg',
        },
        {
          id: 6, pids: [7], name: 'Facteur', gender: 'male', img: 'https://cdn.balkan.app/shared/m30/5.jpg',
        },
        {
          id: 3, mid: 7, fid: 6, pids: [4], name: 'Cécile', gender: 'female', img: 'https://cdn.balkan.app/shared/m10/2.jpg',
        },
        {
          id: 4, mid: 1, fid: 2, pids: [3], name: 'Claire', gender: 'female', img: 'https://cdn.balkan.app/shared/m10/1.jpg',
        },
        {
          id: 5, mid: 1, fid: 2, name: 'Sophie', gender: 'female', img: 'https://cdn.balkan.app/shared/w10/3.jpg',
        },
        {
          id: 8, mid: 3, fid: 4, name: 'Paul', gender: 'female', img: 'https://cdn.balkan.app/shared/w10/3.jpg',
        },
        {
          id: 9, mid: 3, fid: 4, name: 'Paul', gender: 'female', img: 'https://cdn.balkan.app/shared/w10/3.jpg',
        },
      ],
    };
  },

  methods: {
    mytree(domEl, x) {
      this.family = new FamilyTree(domEl, {
        nodes: x,
        nodeBinding: {
          field_0: 'name',
          img_0: 'img',
        },
      });
    },
  },

  mounted() {
    this.mytree(this.$refs.tree, this.nodes);
  },
};
</script>

        <style scoped>
        </style>
