<template>
  <div class="search-content">
    <el-page-header @back="goBack" :content="'搜索：'+this.$route.query.key">
    </el-page-header>
    <div v-if="isLoading">
      <div class="loading" v-loading="true"></div>
    </div>
    <div v-else class="search">
      <ul class="posts-ul" v-if="posts.length != 0">
        <li v-for="(item, index) in posts" :key="index" class="post-item">
          <div class="post-title">
            <a :href="'/post/' + item.id" class="post-link">
              <span>
                {{ item.title }}
              </span>
            </a>
          </div>
          <div class="post-meta">
            <span class="post-time">
              <span class="iconfont">&#xe8b4;</span>
              <span>发布于 </span>
              <time>{{ item.publishTime }}</time>
            </span>
            <span class="post-meta-separate"></span>
            <span class="post-cate">
              <span class="iconfont">&#xe7b8;</span>
              <span>分类于 </span>
              <a
                href="javascript:void(0)"
                @click="toCategory(item.categoryId, item.categoryName)"
                >{{ item.categoryName }}</a
              >
            </span>
          </div>
          <div class="post-main">
            <div class="post-content">
              {{ item.summary }}
              <a :href="'/post/' + item.id" class="read-desc">阅读全文</a>
            </div>
          </div>
          <div class="post-desc">
            <span class="post-author"> posted@{{ item.author }} </span>
            &nbsp;&nbsp;&nbsp;
            <span class="iconfont">&#xe645;</span>
            <span class="post-read"> 阅读({{ item.read_counts }}) </span>
            &nbsp;
            <span class="iconfont">&#xe6ad;</span>
            <span class="post-comment"> 评论({{ item.comment_counts }}) </span>
            &nbsp;
            <span class="iconfont">&#xe600;</span>
            <span class="post-like"> 点赞({{ item.like_counts }}) </span>
          </div>
          <div class="separate"></div>
        </li>
      </ul>
      <div v-else>
        <el-empty description="未查询到此博客"></el-empty>
      </div>
    </div>
    <div class="clear"></div>
    <el-pagination
      small
      :hide-on-single-page="isHide"
      @current-change="handleCurrentChange"
      :page-size="pageSize"
      :current-page="currentPage"
      layout="prev, pager, next"
      :total="total"
    >
    </el-pagination>
    <div class="clear"></div>
  </div>
</template>

<script>
export default {
  name: "search-list",
  data() {
    return {
      posts: [],
      page: 1,
      currentPage: 1,
      total: 0, // 总条数
      pageSize: 15, // 每页的数据条数
      isLoading: true,
    };
  },
  mounted() {
    this.getSearchPosts(this.page);
  },
  computed: {
    isHide() {
      return this.total < this.pageSize;
    },
  },
  methods: {
    getSearchPosts(num) {
      this.$get(this.$API.API_SEARCH_POSTS, {
        key: this.$route.query.key,
        page: num,
      }).then((res) => {
        this.total = res.data.total;
        this.posts = res.data.posts;
        this.isLoading = false;
      });
    },
    toCategory(id, category) {
      window.sessionStorage.setItem("categoryId", id);
      this.$router.push({
        name: "PostByCategory",
        params: {
          name: category,
        },
      });
    },
    goBack() {
      this.$router.push("/");
      this.$emit("cleanSearchInput");
    },
    handleCurrentChange(val) {
      this.isLoading = false;
      this.currentPage = val;
      this.getSearchPosts(val);
      document.body.scrollTop = document.documentElement.scrollTop = 0;
    },
  },
  watch: {
    // 监听路由是否变化
    $route(to, from) {
      if (to.query.key != from.query.key) {
        this.key = to.query.key; // 把最新id赋值给定义在data中的id
        this.getSearchPosts(); // 重新调用加载数据方法
      }
    },
  },
};
</script>

<style scoped lang='less'>
.search-content {
  margin-left: 230px;
  margin-top: 15px;
}

.posts-ul {
  padding: 0;
}

.post-item {
  list-style: none;
}

.posts-ul {
  padding: 0;
}

.post-link {
  font-size: 22px;
  font-weight: 500;
  position: relative;
  display: inline-block;
  color: #596172;
}

.post-link::before {
  content: "";
  display: block;
  width: 100%;
  height: 1px;
  position: absolute;
  bottom: -1px;
  left: 0;
  background-color: #3d615e;
  transform: scaleX(0);
  transition: transform 0.4s ease-in-out;
}

.post-link:hover:before {
  transform: scaleX(1);
}

.post-link:hover {
  color: #177e77;
}

.post-main {
  margin-top: 5px;
}

.post-content {
  font-size: 15px;
  color: #505560;
  font-weight: 300;
  word-break: break-all;
  word-wrap: break-word;
  text-align: justify;
}

.post-content a::after {
  content: "\00bb";
}

.read-desc {
  display: table;
  margin-top: 15px;
  color: #3d615e;
  font-size: 15px;
  border-bottom: 2px dotted #505560;
  font-weight: 300;
}

.read-desc:hover {
  color: #000;
}

.separate {
  margin: 20px 0;
  border-bottom: 1px solid #e8ecf1;
}

.post-meta-separate {
  border-left: 1px solid #999;
  margin: 0 7px;
}

.post-meta {
  margin: 10px 0;
  font-size: 12px;
  color: #999;
  font-weight: 200;
}

.post-cate a {
  display: inline-block;
  border-bottom: 1px solid #999;
}

.post-cate a:hover {
  color: rgb(0, 0, 0);
  border-bottom: 1px solid rgb(0, 0, 0);
}

.post-meta .iconfont,
.post-desc .iconfont {
  font-size: 12px;
  margin: 0 3px;
}

.post-desc {
  text-align: right;
  margin-top: 10px;
  font-size: 13px;
  font-weight: 200;
  color: #505560;
}

.loading /deep/ .el-loading-spinner {
  float: right;
  width: 75%;
  margin-top: 200px;
  text-align: center;
  position: relative;
}

.search {
  margin-top: 15px;
}

.posts-ul {
  animation: slide-in-bottom 1s;
}

@keyframes slide-in-bottom {
  0% {
    transform: translateY(500px);
    opacity: 0;
  }

  100% {
    transform: translateY(0);
    opacity: 1;
  }
}

.el-pagination {
  float: right;
}
</style>