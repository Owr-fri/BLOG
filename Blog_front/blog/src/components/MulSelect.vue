<template>
    <div>
        <el-select v-model="selected" filterable allow-create :multiple="isMultiple" placeholder="请选择" size='mini'>
            <el-option
            v-for="item in options"
            :key="item.id"
            :label="item.name"
            :value="item.id"
            >
            </el-option>
        </el-select>
    </div>
</template>

<script>
  export default {
    name:'mulSelect',

    data() {
      return {
        selected:"",
      }
    },

    props:{
      options:{},
      isMultiple:{
        default:true
      },
    }

  }
</script>