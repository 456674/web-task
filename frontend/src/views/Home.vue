<template>
  <div id="app">
    <Navbar /> <!-- 引入导航栏组件 -->
    <div class="layui-body">
      <!-- 内容区域 -->
      <div class="layui-container">
        <div class="layui-row layui-col-space-20">
          <div class="layui-col-md-8 left-column">
            <div class="content" ref="mapRef"></div>
               <div class="l">
              <div style="display:flex;">
                <div class="layui-card num_card">
                  <div>
                    <div class="info-card-header">监控中井盖</div>
                    <div class="info-card-body">
                      <p id="total">0</p>
                    </div>
                  </div>
                </div>
                <div class="layui-card num_card">
                  <div>
                    <div class="info-card-header">正常井盖</div>
                    <div class="info-card-body">
                      <p id="normal">0</p>
                    </div>
                  </div>
                </div>
                <div class="layui-card num_card">
                  <div>
                    <div class="info-card-header">隐患井盖</div>
                    <div class="info-card-body">
                      <p id="hazard">0</p>
                    </div>
                  </div>
                </div>
              </div>
              <div ref="bieRef" style="width: 500px;height: 500px;"></div>

              </div>
          </div>
      </div>
    </div>
  </div>
  </div>
</template>



<script>
import Navbar from '@/views/Navbar.vue'; // 引入导航栏组件
import axios from 'axios'
import * as echarts from "echarts";
import {onMounted, reactive, ref} from "vue";
import china from '@/assets/china.json'
import hunan from '@/assets/hunan.json'
// import chongqing from './assets/chongqing.json'

import { getMap } from "@/utils/Map";
export default {
  components: { Navbar },
  mounted() {

  },
  methods: {
  }
}
</script>

<script setup>
import Navbar from '@/views/Navbar.vue'; // 引入导航栏组件
import axios from 'axios';
import * as echarts from "echarts";
import { onMounted, ref } from "vue";
import hunan from '@/assets/hunan.json';

const bieRef = ref(null);
const mapRef = ref(null);
let mapChart;

// 将POINT格式的坐标转换为经纬度数组
function convertCoordinates(point) {
  const match = point.match(/POINT \(([^ ]+) ([^ ]+)\)/);
  return match ? [parseFloat(match[1]), parseFloat(match[2])] : null;
}

// 获取统计信息
function getStatistics() {
  // 模拟获取统计信息的方法
  axios.get("/api/covers/total").then(res => {
    const data_total = res.data.total; // 假设返回的数据结构中有一个total字段表示井盖总数
    const data_good = res.data.good_total;
    const data_wrong = data_total - data_good;
    // 更新页面上的统计信息
    document.getElementById('total').innerText = data_total;
    document.getElementById('normal').innerText = data_good;
    document.getElementById('hazard').innerText = data_wrong;
  }).catch(error => {
    console.error('获取统计信息失败：', error);
  });
}

// 获取井盖信息并绘制饼图、地图散点
function getCovers() {
  axios.get("/api/covers/").then(res => {
    let o = {};
    let scatterData = []; // 存储转换后的经纬度和其他信息

    for (const result of res.data.results) {
      if ("维修中" === result.Status) continue;
      if (o[result.Status]) o[result.Status] += 1;
      else o[result.Status] = 1;

      const coords = convertCoordinates(result.Coordinates);
      if (coords) {
        scatterData.push({
          name: result.Location,
          value: [...coords, result.ID], // 经纬度和井盖ID
          status: result.Status,
          issueDescription: result.IssueDescription,
          itemStyle: {
            normal: {
              color: result.Status === 'good' ? "rgba(0,255,0,.7)" : "rgba(255,0,0,.7)",
              shadowBlur: 2,
              shadowColor: "D8BC37"
            }
          }
        });
      }
    }

    let data = Object.keys(o).map(status => ({ value: o[status], name: status }));

    var myChart = echarts.init(bieRef.value);
    var option = {
      // ...饼图配置...
      title: {
        text: '状态统计',
        left: 'center'
      },
      tooltip: {
        trigger: 'item'
      },
      legend: {
        orient: 'vertical',
        left: 'left'
      },
      series: [
        // ...其他系列...
        {
          name: '状态统计',
          type: 'pie',
          radius: '50%',
          data,
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          }
        }
      ]
    };

    myChart.setOption(option);

    // 设置地图散点
    mapChart.setOption({
      series: [{
        type: "scatter",
        coordinateSystem: "geo",
        data: scatterData,
        symbol: "pin",
        legendHoverLink: true,
        symbolSize: [25, 25],
        label: {
          show: true,
          formatter(value) {
            return value.data.value[2];
          },
          color: "#fff",
        },
        itemStyle: scatterData.iter,
      }]
    });
  }).catch(error => {
    console.error('获取井盖信息失败：', error);
  });
}


// 初始化地图
onMounted(() => {
  mapChart = echarts.init(mapRef.value);
  echarts.registerMap('hunan', hunan);

  const option = {
    backgroundColor: '#404a59',
    geo: {
      map: 'hunan', // 使用注册的省份地图
      roam: true,
      zoom: 1.5,
      //设置地图区域的样式
      itemStyle: {
        //设置渐变色
        areaColor: {
          type: 'radial',
          x: 0.5,
          y: 0.5,
          r: 0.5,
          colorStops: [{
            offset: 0, color: '#435161' // 0% 处的颜色
          }, {
            offset: 1, color: '#567788' // 100% 处的颜色
          }],
          global: false // 缺省为 false
        },
        borderColor: '#74B2C0',
        borderWidth: '2',
        color: '#fff',
        //设置阴影
        shadowColor: '#567D92',
        shadowOffsetX: -5,
        shadowOffsetY: 5,
        shadowBlur: 10

      },
      //高亮的时候地图区域
      emphasis: {
        itemStyle: {
          areaColor: '#389BB7',
          color: '#fff',
          //设置阴影
          shadowColor: '#6AA9C3',
          shadowOffsetX: -5,
          shadowOffsetY: 5,
          shadowBlur: 10

        },
      },
      label: {
        show: true,
        fontSize: 12,
        color: '#fff',
      },

    },
    //地图上打点（散点图）
    series: [
      {
        type: "scatter",
        coordinateSystem: "geo",
        symbol: "pin",
        legendHoverLink: true,
        //图标的大小
        symbolSize: [25, 25],
        // 这里渲染标志里的内容以及样式
        label: {
          show: true,
          formatter(value) {
            return value.data.value[2];
          },
          color: "#fff",
        },
        // 标志的样式
        itemStyle: {
          normal: {
            color: "rgba(255,0,0,.7)",
            shadowBlur: 2,
            shadowColor: "D8BC37",
          },
        },
        // 数据格式，其中name,value是必要的，value的前两个值是数据点的经纬度，其他的数据格式可以自定义
        // 至于如何展示，完全是靠上面的formatter来自己定义的
        data: [],
      },
    ],

    //嵌入式文字，类似面包屑导航样式
  };

  mapChart.setOption(option);

  getStatistics();
  getCovers();
});

// 监听窗口大小变化，重新绘制地图
window.addEventListener('resize', () => mapChart.resize());
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

.info-card-header {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.info-card-body {
  font-size: 16px;
  color: #666666;
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
.content {
  width: 62%;
  height: 100vh;
}
.l {
  position: absolute;
  top: 0;
  right: 0;
  background: #ffffff;
}
.layui-card {
  border: none;
  background-color: #ffffff;
  border-radius: 30px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  flex: 1;
  height: 50px;
  margin: 20px;
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


.num_card {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  background-color: #f2f2f2;
  border-radius: 5px;
  padding: 10px;
}
</style>






