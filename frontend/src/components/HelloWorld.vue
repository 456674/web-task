<template>
  <div class="hello">
    <button @click="handleMsg">获取msg</button>
    <h1>{{ msg }}</h1>
  </div>
</template>

<script>
import {getmsg} from "@/api/helloworld";

export default {
  name: 'HelloWorld',
  data() {
    return {
      msg:''
    }
  },
  methods: {
    handleMsg() {
      getmsg().then(res => {
        this.msg = res.data
      })
    }
  }
}
</script>
