<template>
  <el-container style="height: 100vh;">
    <el-aside width="200px" style="background-color: #333842;">
    <el-menu default-active="1" router :collapse="isCollapse" style="background-color: #333842;" text-color="#fff" active-text-color="#ffd04b">
      <el-menu-item index="/home">
        <i class="el-icon-house"></i>
        <span slot="title">首页</span>
      </el-menu-item>
      <el-menu-item index="/covers">
        <i class="el-icon-info"></i>
        <span slot="title">监控</span>
      </el-menu-item>
      <el-menu-item index="/ab">
        <i class="el-icon-info"></i>
        <span slot="title">待处理</span>
      </el-menu-item>
      <el-menu-item index="/model">
        <i class="el-icon-info"></i>
        <span slot="title">模型</span>
      </el-menu-item>
      <el-menu-item index="/video">
      <i class="el-icon-info"></i>
      <span slot="title">视频流</span>
      </el-menu-item>

      <!-- 更多的菜单项... -->
    </el-menu>
    </el-aside>
  </el-container>
</template>

<script setup>
import { ref } from 'vue';

// 控制侧边栏折叠状态
const isCollapse = ref(false);
</script>

<style scoped>
/* 设置侧边栏的背景色和文字颜色 */
.el-aside {
  background-color: #333842;
}

.el-menu {
  color: #333842;
}

/* 设置菜单激活项文字颜色 */
.el-menu .is-active {
  color: #ffd04b;
}
</style>
