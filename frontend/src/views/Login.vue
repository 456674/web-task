<template>
  <div class="loginbg">
    <div class="loginbox">
      <h1>Login</h1>
      <p><i><img src="../assets/账号.png" class="icon" ></i><input type="text" placeholder="请输入您的账号"></p>
      <p><i><img src="../assets/密码.png" class="icon"></i><input type="password" placeholder="请输入您的密码"></p>
      <div class="loginButton" @click="login">登录</div>
      <router-link to="/register" style="float: right; margin-right: 20px">
        注册
      </router-link>
    </div>
  </div>
</template>


<script setup>
import axios from 'axios'
import {reactive, onMounted, ref} from "vue";
import { useRouter } from 'vue-router';
import { useStore } from 'vuex';

const router = useRouter();
const user_form = reactive({
  Username: "",
  Password: "",
});
const login = () => {
  axios.post('http://localhost:5000/login', user_form)
      .then(response => {
        if (response.data.success) {
          // 登录成功
          const data = response.data.results;
          /*store.dispatch('updateAccountId', data.USERID); // 更新 Vuex store 中的 accountId*/
          router.push({ path: '/home' }); // 使用 Vue Router 进行页面跳转
        } else {
          // 登录失败
          alert('用户名或密码错误');
        }
      })
      .catch(error => {
        console.error(error);
        // 处理登录失败的逻辑
      });
};


</script>
<style>
body {
  margin: 0;
}

.loginbg {
  background-image: url('../assets/1.png');
  background-size: cover;
  background-position: center;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.loginbox h1 {
  text-align: center;
  margin-top: 30px; /* 根据需要调整间距 */
}


.loginbg img {
  width: 100%;
  transition: 1.5s all;
}

.loginbox {
  width: 500px;
  height: 300px;
  border: 1px solid #2b2b2b;
  border-radius: 10px;
  box-shadow: 0 0 20px 20px #00000030;
  position: absolute;
  z-index: 1;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  margin: auto auto;
  background: rgba(255, 255, 255, 0.75); /* 设置透明度为5% */
}

.loginbox h1 {
  text-align: center;
}

.loginbox p {
  font-size: 18px;
  display: block;
  width: 380px;
  margin: 20px auto;
}

.loginbox i {
  display: inline-block;
  width: 25px;
  height: 25px;
  padding-top: 5px;
}

.icon {
  width: 25px;
}

.loginbox input {
  width: 335px;
  height: 18px;
  font-size: 18px;
  margin-left: 8px;
  background: #ffffff00;
  border: none;
  border-bottom: 2px solid #000;
  color: #D7DDE8;
}

.loginbox input:focus {
  outline: none;
}

.loginButton {
  width: 200px;
  height: 40px;
  margin: 30px auto;
  text-align: center;
  line-height: 40px;
  background: #B373BD;
  cursor: pointer;
  border-radius: 10px;
  color: #FFFFFF;
}

.loginButton:hover {
  box-shadow: 0 0 10px 10px #00000020;
}
</style>
