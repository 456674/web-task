import china from '../assets/china.json'
import heilongjiang from '../assets/heilongjiang.json'
import jilin from '../assets/jilin.json'
import liaoning from '../assets/liaoning.json'
import neimenggu from '../assets/neimenggu.json'
import beijing from '../assets/beijing.json'
import hebei from '../assets/hebei.json'
import tianjing from '../assets/tianjing.json'
import shandong from '../assets/shandong.json'
import sshanxi from '../assets/sshanxi.json'
import ningxia from '../assets/ningxia.json'
import qinghai from '../assets/qinghai.json'
import shanxi from '../assets/Shanxi.json'
import henan from '../assets/henan.json'
import jiangsu from '../assets/jiangsu.json'
import anhui from '../assets/anhui.json'
import shanghai from '../assets/shanghai.json'
import zhejiang from '../assets/zhejiang.json'
import hubei from '../assets/hubei.json'
import chongqing from '../assets/chongqing.json'
import sichuan from '../assets/sichuan.json'
import yunnan from '../assets/yunnan.json'
import guizhou from '../assets/guizhou.json'
import hunan from '../assets/hunan.json'
import jiangxi from '../assets/jiangxi.json'
import fujian from '../assets/fujian.json'
import guangxi from '../assets/guangxi.json'
import guangdong from '../assets/guangdong.json'
import taiwan from '../assets/taiwan.json'
import hainan from '../assets/hainan.json'
import gansu from '../assets/gansu.json'
import xizang from '../assets/xizang.json'
import xinjiang from '../assets/xinjiang.json'

const mapList = {
    '黑龙江省': 'heilongjiang',
    '吉林省': 'jilin',
    '辽宁省': 'liaoning',
    '内蒙古自治区': 'neimenggu',
    '北京市': 'beijing',
    '河北省': 'hebei',
    '天津市': 'tianjing',
    '山东省': 'shandong',
    '山西省': 'sshanxi',
    '宁夏回族自治区': 'ningxia',
    '青海省': 'qinghai',
    '陕西省': 'shanxi',
    '河南省': 'henan',
    '江苏省': 'jiangsu',
    '安徽省': 'anhui',
    '上海市': 'shanghai',
    '浙江省': 'zhejiang',
    '湖北省': 'hubei',
    '重庆市': 'chongqing',
    '四川省': 'sichuan',
    '云南省': 'yunnan',
    '贵州省': 'guizhou',
    '湖南省': 'hunan',
    '江西省': 'jiangxi',
    '福建省': 'fujian',
    '广西壮族自治区': 'guangxi',
    '广东省': 'guangdong',
    '台湾省': 'taiwan',
    '海南省': 'hainan',
    '甘肃省': 'gansu',
    '西藏自治区': 'xizang',
    '新疆维吾尔自治区': 'xinjiang'
}

const mapData = {
    heilongjiang,
    jilin,
    liaoning,
    neimenggu,
    beijing,
    hebei,
    tianjing,
    shandong,
    sshanxi,
    ningxia,
    qinghai,
    shanxi,
    henan,
    jiangsu,
    anhui,
    shanghai,
    zhejiang,
    hubei,
    chongqing,
    sichuan,
    yunnan,
    guizhou,
    hunan,
    jiangxi,
    fujian,
    guangxi,
    guangdong,
    taiwan,
    hainan,
    gansu,
    xizang,
    xinjiang,
}

export function getMap(mapName){
    
    const cityName = mapList[mapName]
    if(cityName){
        return [cityName,mapData[cityName]]
    }
    return ['china',china]
}
