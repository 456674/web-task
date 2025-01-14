<template>
  <div id="app">
    <Navbar /> <!-- 引入导航栏组件 -->
    <div class="layui-body">
      <!-- 内容区域 -->
      <div class="layui-container">
        <div class="layui-row layui-col-space-20">
          <!-- Video Stream and Manhole Cover Management -->
          <div class="layui-col-md-8 left-column">
            <!-- Video Stream Card -->
            <!-- Video Stream Card -->
            <div class="layui-card">
              <div class="layui-card-header" style="text-align: center; font-size: 20px; font-weight: bold;">实时视频流</div>
              <div class="video-stream-container">
                <img src="http://119.3.153.128:5000/video_feed" alt="实时视频流">
              </div>
            </div>

            <!-- Existing Manhole Cover Management Code ... -->
          </div>
          <!-- Right Column for Category Changes and Statistics -->
          <div class="layui-col-md-4 right-column">
            <!-- Category Changes Card -->
            <div class="layui-card num_card">
              <div>
                <div class="info-card-header">类别变化</div>
                <div class="info-card-body">
                  <!-- Placeholder for Category Changes -->
                  <p id="categoryChanges">GOOD -> NONE</p>
                </div>
              </div>
            </div>
            <!-- Existing Statistics Cards ... -->
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Existing Drawer and Other Components ... -->

</template>

<script setup>
// Import statements and existing script logic ...
import Navbar from '@/views/Navbar.vue'; // 引入导航栏组件
import axios from 'axios'
// Add logic to handle video stream if necessary
</script>

<!-- Add styles for the video stream container if necessary -->
<style scoped>
/* Existing styles ... */
@import 'https://www.layuicdn.com/layui-v2.6.8/css/layui.css';
.video-stream-container img {
  display: block; /* 确保图片不会有额外的空白或间隙 */
  max-width: 100%; /* 确保图片宽度不超过容器宽度 */
  max-height: 80vh; /* 图片的最大高度不能超过视口高度的90% */
  object-fit: contain; /* 保持内容的宽高比并使其在容器内居中显示 */
  background-color: black; /* 背景色设置为黑色 */
}




#nav {
  position: fixed;
  top: 0;
  bottom: 0;
  left: 0;
  width: 200px;
  overflow: auto;
  border-right: 1px solid #eee;
  border-radius: 30px;
}

.layui-body {
  position: absolute;
  left: 200px;
  right: 0;
  top: 0;
  bottom: 0;
  z-index: 10;
  background-color: #f2f2f2;
  overflow: auto;
  padding: 15px;
}

.layui-container {
  width: 80vw;
  margin-left: 20px;
  margin-top: 20px;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 30px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);

}

.layui-card {
  border: none;
  background-color: #ffffff;
  border-radius: 30px;
  margin-bottom: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.map-container {
  width: 1200px;
  height: 400px;
  overflow: auto;
}

.info-card {
  margin-bottom: 20px;
  background-color: #f2f2f2;
  border-radius: 5px;
  padding: 10px;
}

.info-card-header {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.info-card-body {
  font-size: 16px;
  color: #666666;
}

.left-column {
  padding-right: 20px;
}

.right-column {
  padding-left: 20px;
}

.increase_button{
  border-radius: 20px;
  width: 80px;
  height: 30px;
  margin-left: 20px;
}

.num_button {
  border-radius: 20px;
  width: 80px;
  height: 30px;
}

.num_card {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  background-color: #f2f2f2;
  border-radius: 5px;
  padding: 10px;
}


/* Other styles... */
</style>
