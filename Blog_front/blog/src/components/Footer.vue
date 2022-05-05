<template>
  <div class="footer">
    <div>
      <span>@ 2022 Owr</span>
    </div>
    <span>
      Open sourced to Github
      <a href="https://github.com/Owr-fri/BLOG"> Owr-fri</a>
    </span>

  </div>
</template>
<script>
  export default {
    name: 'Footer',
  }
</script>

<style scoped>
  .footer {
    border-top: 1px solid #e8ecf1;
    font-size: 12px;
    text-align: center;
    padding: 20px 0;
    font-weight: 200;
    color: #505560;
  }

  .footer a {
    display: inline;
    text-decoration: underline;
  }
</style>