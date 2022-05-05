<template>
  <div class="activate">
    <div class="category-body">
      <div class="category-in">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "category-item",
    data() {
      return {

      }
    },
    components: {},
    mounted() {},
    methods: {}

  }
</script>

<style lang="less" scoped>
  .activate {
    margin-top: 15px;
  }

  .category-in {
    margin-left: 250px;
  }
</style>