<template>
  <el-dialog
      title="井盖信息"
      :visible.sync="visible"
      width="30%"
      :before-close="handleBeforeClose"
  >
    <el-form ref="formRef" :model="formData" status-icon label-width="120px">
      <!-- 表单项目 -->
      <el-form-item label="井盖ID" prop="id">
        <el-input v-model.number="formData.id"></el-input>
      </el-form-item>
      <el-form-item label="位置" prop="location" required>
        <el-input v-model.trim="formData.location"></el-input>
      </el-form-item>
      <!-- ... 其他表单项 ... -->

      <el-form-item>
        <el-button type="primary" @click.prevent="submit">提交</el-button>
        <el-button @click.prevent="close">关闭</el-button>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script setup>
import { ref, watch, toRefs } from 'vue';
import { ElForm } from 'element-plus';
import service from '@/utils/http'; // 引入封装好的 http 实例
const props = defineProps({
  visible: Boolean,
  editData: Object
});

const emits = defineEmits(['update:visible', 'submit', 'close']);
const formRef = ref(null);
const formData = ref({
  id: null,
  location: '',
});

watch(() => props.editData, (newVal) => {
  if (newVal) {
    formData.value = { ...newVal };
  } else {
    // 如果没有提供editData，则重置表单为默认值
    formData.value = { id: null, location: '' };
  }
}, { immediate: true });

function submit() {
  formRef.value.validate((valid) => {
    if (valid) {
      // 根据 formData 是否包含 id 来决定是创建还是更新操作
      const isUpdate = formData.value.id;
      const url = isUpdate ? `/covers/${formData.value.id}` : '/covers';
      const method = isUpdate ? 'put' : 'post';

      service[method](url, formData.value).then(() => {
        emits('submit', formData.value);
        formRef.value.resetFields();
      }).catch(error => {
        console.error('提交表单失败：', error);
      });
    } else {
      console.log('error submit!!');
      return false;
    }
  });
}

function close() {
  emits('close');
}

function handleBeforeClose(done) {
  // 这里可以执行关闭前的逻辑，比如表单验证或者保存草稿提示等
}
</script>

<style scoped>
/* 对话框内部样式 */
</style>
