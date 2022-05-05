<template>
  <div class="activate">
    <div class="tags-body">
      <div class="tags-in">
        <router-view></router-view>
      </div>
    </div>

  </div>
</template>

<script>
  export default {
    name: 'label-item',
    data() {
      return {}
    },
    components: {

    },
  }
</script>

<style lang="less" scoped>
  .activate {
    margin-top: 15px;
  }

  .tags-in {
    margin-left: 240px;
  }
</style>