<template>
  <div id="app">
    <Navbar /> <!-- 引入导航栏组件 -->
    <div class="layui-body">
      <!-- 内容区域 -->
      <div class="layui-container">
        <div class="layui-row layui-col-space-20">
          <div class="layui-col-md-8 left-column">
            <div class="layui-card">
              <div class="layui-card-header" style="text-align: center; font-size: 20px; font-weight: bold;">井盖管理</div>
              <!-- 添加井盖按钮 -->
              <el-button class="increase_button" type="primary" @click="tableClean(),add_dialog_visible = true " size="small">
                添加井盖
              </el-button>
              <div class="layui-card-body map-container">

                <div style="margin: 0 auto;">

                  <!-- 数据表格 -->
                  <el-table :data="covers" style="margin: 20px auto;">
                    <el-table-column label="编号" prop="ID"/>
                    <el-table-column label="位置" prop="Location"/>
                    <el-table-column label="坐标" prop="Coordinates"/>
                    <el-table-column label="问题" prop="IssueDescription"/>
                    <el-table-column label="状态" prop="Status"/>
                    <el-table-column label="图片" prop="ImageURL">
                      <template #default="{ row }">
                        <el-button type="primary" style="margin-left: 16px" @click="showImage(row)">
                          查看
                        </el-button>
                      </template>
                    </el-table-column>
                    <el-table-column align="right" label="操作" width="200px">
                      <template #default="scope">
                        <el-button size="small" @click="handleEdit(scope.$index,scope.row)">
                          编辑
                        </el-button>
                        <el-button
                            size="small"
                            type="danger"
                            @click="handleDelete(scope.$index,scope.row)"
                        >
                          删除
                        </el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                </div>

                <!--添加井盖界面-->
                <el-dialog
                    title="添加井盖"
                    v-model="add_dialog_visible"
                    width="30%"
                    :before-close="handleClose"

                >
                  <el-form
                      ref="ruleFormRef"
                      :model="cover_form"
                      status-icon
                      label-width="120px"
                      class="demo-ruleForm"
                  >
                    <el-form-item label="编号" prop="ID">
                      <el-input v-model="cover_form.ID" placeholder="请输入井盖的编号" autocomplete="off"/>
                    </el-form-item>
                    <el-form-item label="位置" prop="Location">
                      <el-input v-model="cover_form.Location" placeholder="请输入井盖的位置" autocomplete="off"/>
                    </el-form-item>
                    <el-form-item label="坐标" prop="Coordinates">
                      <div>
                        <el-input v-model="longitude" placeholder="请输入横坐标" autocomplete="off"
                                  :rules="coordinateRules"></el-input>
                        <span style="margin: 0 10px;">,</span>
                        <el-input v-model="latitude" placeholder="请输入纵坐标" autocomplete="off"
                                  :rules="coordinateRules"></el-input>
                      </div>
                    </el-form-item>
                    <el-form-item label="问题" prop="IssueDescription">
                      <el-input v-model="cover_form.IssueDescription" placeholder="请输入井盖的问题" autocomplete="off"/>
                    </el-form-item>
                    <el-form-item label="状态" prop="Status">
                      <el-select v-model="cover_form.Status" placeholder="请选择状态">
                        <el-option
                            v-for="statusOption in statusOptions"
                            :key="statusOption.value"
                            :label="statusOption.label"
                            :value="statusOption.value">
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <el-form-item label="图片" prop="ImageURL">
                      <el-input v-model="cover_form.ImageURL" autocomplete="off"/>
                    </el-form-item>
                    <el-form-item>
                      <el-button type="primary" @click="submitForm(ruleFormRef)">提交</el-button>
                      <el-button @click="resetForm(ruleFormRef)">重置</el-button>
                    </el-form-item>
                  </el-form>
                </el-dialog>

                <!-- 编辑井盖界面 -->
                <el-dialog
                    title="编辑井盖"
                    v-model="edit_dialog_visible"
                    width="30%"
                    :before-close="handleClose"
                >
                  <el-form
                      ref="editFormRef"
                      :model="cover_form"
                      status-icon
                      label-width="120px"
                      class="demo-ruleForm"
                  >
                    <el-form-item label="编号" prop="ID">
                      <el-input v-model="cover_form.ID" placeholder="请输入井盖的编号" autocomplete="off"/>
                    </el-form-item>
                    <el-form-item label="位置" prop="Location">
                      <el-input v-model="cover_form.Location" placeholder="请输入井盖的位置" autocomplete="off"/>
                    </el-form-item>
                    <el-form-item label="坐标" prop="Coordinates">
                      <div>
                        <el-input v-model="longitude" placeholder="请输入井盖的横坐标" autocomplete="off"
                                  :rules="coordinateRules"></el-input>
                        <span style="margin: 0 10px;">,</span>
                        <el-input v-model="latitude" placeholder="请输入井盖的纵坐标" autocomplete="off"
                                  :rules="coordinateRules"></el-input>
                      </div>
                    </el-form-item>

                    <el-form-item label="问题" prop="IssueDescription">
                      <el-input v-model="cover_form.IssueDescription" placeholder="请输入井盖的问题" autocomplete="off"/>
                    </el-form-item>
                    <el-form-item label="状态" prop="Status">
                      <el-select v-model="cover_form.Status" placeholder="请选择井盖的状态">
                        <el-option
                            v-for="statusOption in statusOptions"
                            :key="statusOption.value"
                            :label="statusOption.label"
                            :value="statusOption.value">
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <el-form-item label="图片" prop="ImageURL">
                      <el-input v-model="cover_form.ImageURL" autocomplete="off"/>
                    </el-form-item>
                    <el-form-item>
                      <el-button type="primary" @click="submitEditForm(editFormRef)">提交</el-button>
                      <el-button @click="resetForm(editFormRef)">重置</el-button>
                    </el-form-item>
                  </el-form>
                </el-dialog>
              </div>
            </div>
          </div>
          <div class="layui-col-md-4 right-column">
            <div class="layui-card num_card">
              <div>
                <div class="info-card-header">监控中井盖</div>
                <div class="info-card-body">
                  <p id="total">0</p>
                </div>
              </div>
              <el-button class="num_button" @click="getCovers()">查看</el-button>
            </div>
            <div class="layui-card num_card">
              <div>
                <div class="info-card-header">正常井盖</div>
                <div class="info-card-body">
                  <p id="normal">0</p>
                </div>
              </div>
              <el-button class="num_button" @click="getGoodCovers()">查看</el-button>
            </div>
            <div class="layui-card num_card">
              <div>
                <div class="info-card-header">隐患井盖</div>
                <div class="info-card-body">
                  <p id="hazard">0</p>
                </div>
              </div>
              <el-button class="num_button" @click="getNOTGoodCovers()">查看</el-button>
            </div>
          </div>
         </div>
      </div>
    </div>
  </div>

  <el-drawer v-model="drawer" title="图片详情" :with-header="false">
    <img :src="currentImage" style="max-width: 100%; max-height: 100%;" />
  </el-drawer>
</template>



<script>
import Navbar from '@/views/Navbar.vue'; // 引入导航栏组件
import axios from 'axios'
export default {
  name: 'YourComponentName',
  mounted() {
    this.getStatistics();
  },
  methods: {
    getStatistics() {
      // 模拟获取统计信息的方法
        axios.get("/api/covers/total").then(res => {
        const data_total = res.data.total; // 假设返回的数据结构中有一个total字段表示井盖总数
        const data_good = res.data.good_total;
        const data_wrong = data_total-data_good;
        // 更新页面上的统计信息
        this.$nextTick(() => {
          document.getElementById('total').innerText = data_total;
          document.getElementById('normal').innerText = data_good;
          document.getElementById('hazard').innerText = data_wrong;
        });
      }).catch(error => {
        console.error('获取统计信息失败：', error);
      });
    }
  }
}
</script>

<script setup>

import {reactive, onMounted, ref} from "vue";
import { ElMessageBox } from 'element-plus';

const drawer = ref(false);
const currentImage = ref("");

const covers = reactive([]);
const add_dialog_visible = ref(false);
const ruleFormRef = ref();
const cover_form = reactive({
  ID: "",
  Location: "",
  Coordinates: "",
  IssueDescription: "",
  Status: "",
  ImageURL: "",
});

const showImage = (row) => {
  currentImage.value = row.ImageURL;
  drawer.value = true;
};

const statusOptions = [
  {label: 'good', value: 'good'},
  {label: 'circle', value: 'circle'},
  {label: 'broke', value: 'broke'},
  {label: 'lose', value: 'lose'},
  {label: 'uncovered', value: 'uncovered'},
  {label: '维修中', value: '维修中'}
];

const coordinateRules = [
  {
    validator: (rule, value, callback) => {
      const coordinatePattern = /^-?\d+(\.\d+)?,-?\d+(\.\d+)?$/;
      if (!coordinatePattern.test(value)) {
        callback(new Error('请输入正确的坐标格式，例如：经度,纬度'));
      } else {
        callback();
      }
    },
    trigger: 'blur'
  }
];

const longitude = ref("");
const latitude = ref("");

const submitForm = (formE1) => {
  if (!longitude.value || !latitude.value) {
    console.error('经度或纬度为空');
    return;
  }

  // 构造坐标数据
  const coordinates = `${longitude.value},${latitude.value}`;

  // 修改表单数据
  cover_form.Coordinates = coordinates;

    axios.post("/api/covers/",cover_form).then(() => {
    add_dialog_visible.value = false;
    formE1.resetFields(); // 修改此处调用的方法
    getCovers();
    updateStatistics();
  }).catch(error => {
    console.error('提交表单失败：', error);
  });
}

const tableClean =() =>{
  cover_form.ID = "";
  cover_form.Location = "";
  cover_form.Coordinates = "";
  cover_form.IssueDescription = "";
  cover_form.Status = "";
  cover_form.ImageURL = "";
  longitude.value = "";
  latitude.value = "";
}

const resetForm = (formE1) => {
  formE1.resetFields();
  longitude.value = "";
  latitude.value = "";
}


const handleClose = (done) => {
  ElMessageBox.confirm('确认关闭？')
      .then(() => {

        done();
      })
      .catch(() => {
      });
}

// 修改前端代码中获取正常井盖信息的请求路径为 /covers/good
const getGoodCovers = () => {
    axios.get("/api/covers/good").then(res => {
    covers.splice(0, covers.length);
    covers.push(...res.data.results);
    console.log('更新数据');
  }).catch(error => {
    console.error('获取正常井盖信息失败：', error); // 输出更详细的错误信息
  });
};

const getNOTGoodCovers = () => {
    axios.get("/api/covers/not_good").then(res => {
    covers.splice(0, covers.length);
    covers.push(...res.data.results);
    console.log('更新数据');
  }).catch(error => {
    console.error('获取正常井盖信息失败：', error); // 输出更详细的错误信息
  });
};

const getCovers = () => {
    axios.get("/api/covers/").then(res => {
    covers.splice(0, covers.length);
    covers.push(...res.data.results);
    console.log('更新数据');
  }).catch(error => {
      console.error('获取井盖信息失败：', error); // 输出更详细的错误信息
    });
    ;
};

onMounted(() => {
  getCovers();
});

// App.vue

const handleDelete = (index, cover) => {
  if (!cover || !cover.ID) {
    console.error('尝试删除一个没有有效ID的井盖');
    return;
  }

    axios.delete(`/api/covers/${cover.ID}`).then(() => {
    getCovers();
    updateStatistics(); // 手动更新监控数据
  }).catch(error => {
    console.error('删除数据失败：', error);
  });
};

const updateStatistics = () => {
  // 在这里添加更新监控数据的逻辑，重新获取统计信息并更新页面上的统计数据
  axios.get("/api/covers/total").then(res => {
    const data_total = res.data.total;
    const data_good = res.data.good_total;
    const data_wrong = data_total - data_good;
    // 更新页面上的统计信息
    document.getElementById('total').innerText = data_total;
    document.getElementById('normal').innerText = data_good;
    document.getElementById('hazard').innerText = data_wrong;
  }).catch(error => {
    console.error('获取统计信息失败：', error);
  });
};



/*编辑表单*/
const editFormRef = ref()
const edit_dialog_visible = ref(false)

const handleEdit = (index, scope) => {
  for (let key in scope) {
    if (key === 'Coordinates') {
      console.log('原始坐标数据:', scope[key]);
      // 提取经度和纬度
      const match = scope[key].match(/POINT \(([-\d.]+) ([-\d.]+)\)/);
      if (match) {
        longitude.value = match[1];
        latitude.value = match[2];
        console.log('提取的经度:', longitude.value);
        console.log('提取的纬度:', latitude.value);
      } else {
        console.error('坐标格式不正确');
      }
    } else {
      cover_form[key] = scope[key];
    }
  }
  edit_dialog_visible.value = true;
}



//提交按钮
const submitEditForm = (formE1) => {
  // 构造坐标数据
  const coordinates = `${longitude.value},${latitude.value}`;

  // 修改表单数据
  cover_form.Coordinates = coordinates;

  axios.put(`/api/covers/${cover_form.ID}`, cover_form).then(() => {
    formE1.resetFields()
    edit_dialog_visible.value = false
    getCovers()
    updateStatistics();
  }).catch(error => {
    console.error('提交编辑表单失败：', error);
  });
}
</script>


<style scoped>
@import 'https://www.layuicdn.com/layui-v2.6.8/css/layui.css';

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
  width: 90%;
  height: 300px;
  overflow: auto;
  margin-bottom: 20px; /* 在下方添加20px的间隙 */
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

</style>






