import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from "../views/Login.vue"
import Index from '../views/Index.vue'
import Post from '../views/Post.vue'
import PostList from '../components/PostList.vue'
import Manage from '../views/Manage.vue'
import Label from '../views/Label.vue'
import Category from '../views/Category.vue'
import CategoryList from '../components/CategoryList.vue'
import PostByCategory from '../components/PostByCategory.vue'
import PostByLabel from '../components/PostByLabel.vue'
import TagCloud from "../components/TagCloud.vue"
import Picture from '../views/Picture.vue'
import Ppicture from '../components/PublishPicture.vue'
import PicturePage from '../views/PicturePage.vue'
import PublishPost from '../components/PublishPost.vue'
import ManagePost from '../components/ManagePost.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    component: Index,
    children:[
      {
        path:'',
        name:'PostList',
        component:PostList,
      },
      {
        path:'label',
        component:Label,
        children:[
          {
            path: ':name',
            name: 'PostByLabel',
            component: PostByLabel,
          },
          {
            path: '',
            name: 'TagCloud',
            component: TagCloud,
          }
        ]
      },
      {
        path:'category',
        component:Category,
        children:[
          {
            path: '',
            name: 'CategoryList',
            component: CategoryList,
          },
          {
            path: ':name',
            name: 'PostByCategory',
            component: PostByCategory,
          }
        ]
      },
      {
        path:'picture',
        name:'Picture',
        component:Picture,
      },
    ]
  },
  {
    path: '/post/:p',
    name: 'Post',
    component: Post,
    
  },
  {
    path: '/manage',
    name: 'Manage',
    component: Manage,
    children: [
      {
        path:'ppost',
        name:'Ppost',
        component:PublishPost,
      },
      {
        path:'mpost',
        name:'Mpost',
        component:ManagePost,
      },
      {
        path:'ppicture',
        name:'Ppicture',
        component:Ppicture,
      },
    ]
  },
  {
    path:'/picture/:title',
    name:'PicturePage',
    component:PicturePage
  },

]

const router = new VueRouter({
  mode: 'history',
  // base: process.env.BASE_URL,
  routes
})

export default router
