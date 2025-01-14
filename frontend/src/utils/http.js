// http.js
import axios from 'axios';

const service = axios.create({
    baseURL: 'http://47.245.93.147:5000/', // 替换成你的API服务器地址
    timeout: 5000 // 请求超时时间
});


export default service;
