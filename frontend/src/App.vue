<template>
  <el-config-provider :locale="zhCn">
    <router-view />
  </el-config-provider>
</template>

<script setup lang="ts">
/**
 * 引入 Element Plus 的配置提供者组件和中文语言包。
 * 使用 Element Plus 的配置提供者组件来设置全局的中文语言环境。
 * 这样，整个应用程序中的 Element Plus 组件都将使用中文语言包。
 */
import { ElConfigProvider } from 'element-plus';
import zhCn from 'element-plus/es/locale/lang/zh-cn';
</script>
<style>

</style>
