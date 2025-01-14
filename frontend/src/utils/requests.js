// 对于axios进行二次封装
import axios from "axios";

// axios.defaults.withCredentials = true

// 1.利用axios对象的方法create，去创建一个axios实例
const requests = axios.create({
    // 配置对象
    // 基础路径，发请求的时候y
    baseURL: 'http://127.0.0.1:5000',
    // 代表请求超时的时间5s
    timeput:5000,
})

// 对外暴露
export default requests;
