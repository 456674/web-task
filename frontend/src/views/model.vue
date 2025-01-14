<template>
  <el-container>
    <!-- 导航栏在最左侧 -->
    <el-aside width="200px">
      <Navbar/>
    </el-aside>

    <!-- 主体内容区域 -->
    <el-main>
      <el-row :gutter="24">
        <!-- 上传框，占据1/3列 -->
        <el-col :span="8">
          <div class="full-height-container">

            <el-upload
                class="upload-demo"
                drag
                action="http://127.0.0.1:5000/upload"
                :on-success="handleSuccess"
                :file-list="fileList"
                list-type="picture-card">
              <i class="el-icon-plus"></i>
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                将文件拖到此处，或
                <em>点击上传</em>
                上传后处理后图片会在中央展示
              </div>
            </el-upload>
          </div>
        </el-col>

        <!-- 显示框：显示后端返回的处理后的图片，占据1/3列 -->
        <el-col :span="8">
          <div v-if="processedImageUrl" class="full-height-container">
            <!-- 弧形容器 -->
            <div class="title-container">
              <h2>处理后图片</h2>
            </div>
            <img :src="processedImageUrl" alt="处理后的图片" class="image-preview">
          </div>
        </el-col>

        <!-- 模型效果图，占据1/3列 -->
        <el-col :span="8">
          <div class="full-height-container">
            <div class="title-container">
            <h2>模型效果展示</h2>
            </div>
            <img :src="imageUrl" alt="模型效果图" class="image-preview">
            <!-- 显示预测类别 -->
            <div v-if="predictedClass" class="predicted-class">
              <div class="title1-container">
              模型：YOLOv8n 预测类别: {{ predictedClass }}
              </div>
            </div>

          </div>

        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
import Navbar from '@/views/Navbar.vue'; // 引入导航栏组件

export default {
  components: { Navbar },
  data() {
    return {
      imageUrl: '/api/plot', // 模型效果图的URL
      processedImageUrl: '', // 用于存储服务器返回的处理后图片的URL
      predictedClass: '', // 存储预测类别
      fileList: [] // 文件列表
    };
  },
  methods: {
    handleSuccess(response, file, fileList) {
      // 上传成功，从响应中获取处理后图片的URL
      this.processedImageUrl = response.image_url;
      this.predictedClass = response.classes; // 假设响应中包含预测类别
    }
  }
};
</script>

<style scoped>
.title-container {
  background-color: orange; /* 设置背景颜色为橙色 */
  padding: 10px 20px; /* 添加一些内边距 */
  border-radius: 20px; /* 设置圆角 */
  display: inline-block; /* 让容器适应内容宽度 */
  margin-bottom: 20px; /* 在标题和图片之间添加一些空间 */

}
.title-container h2{
color: white;

}
.title1-container {
  background-color: forestgreen; /* 设置背景颜色为橙色 */
  padding: 10px 20px; /* 添加一些内边距 */
  border-radius: 0px; /* 设置圆角 */
  display: inline-block; /* 让容器适应内容宽度 */
  margin-top: 20px; /* 在标题和图片之间添加一些空间 */
}
.full-height-container {
  display: flex;
  flex-direction: column;
  justify-content: center; /* 垂直居中 */
  align-items: center; /* 水平居中 */
  height: calc(95vh ); /* 减去顶部导航栏的高度，如果有的话 */
  background-color: skyblue;
  border-radius: 20px 20px 20px 20px;
  overflow: hidden;
}
.upload-demo {
  display: flex; /* 使用flex布局使内容居中 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  width: 100%; /* 占据容器宽度的80% */
  height: 100%; /* 占据容器高度的80% */
  margin: auto; /* 自动外边距确保水平居中 */
  border: none;
}

.upload-demo .el-upload {
  border: none;
}

.upload-demo:hover {
  border-color: transparent;
}

.display-container, .model-container {
  text-align: center;
}
.image-preview {
  max-width: 90%; /* 图片最大宽度为容器宽度 */
  max-height: 80%; /* 图片最大高度为容器高度的80% */
  object-fit: contain; /* 确保图片比例不变，且完全包含在框内 */
}
.processed-image, .model-image {
  max-width: 100%;
  height: auto;
}

</style>
