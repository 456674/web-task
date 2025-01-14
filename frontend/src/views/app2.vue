<template>
  <div>
    <el-container style="height: 100vh;">
      <el-aside width="200px" style="background-color: #333842;">
        <el-menu default-active="1" router :collapse="isCollapse" background-color="#333842" text-color="#fff" active-text-color="#ffd04b">
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
          <!-- 更多的菜单项... -->
        </el-menu>
      </el-aside>

      <el-main>
        <!-- 路由视图，不同页面的内容将在这里展示 -->
        <router-view></router-view>
      </el-main>

    </el-container>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

// 控制侧边栏折叠状态
const isCollapse = ref(false);

const router = useRouter();

const handleNavigation = (route) => {
  router.push(route);
};
</script>

<style scoped>
/* 在这里添加更多的 CSS 样式 */
</style>
