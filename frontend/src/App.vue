<script setup>
import { defineProps, ref, reactive, onMounted, computed } from 'vue';
import 'primeicons/primeicons.css';
// import router from '@/router';
import axios from 'axios';
// import { RouterView } from 'vue-router';
import PulseLoader from 'vue-spinner/src/PulseLoader.vue';

import Navbar from './components/Navbar.vue';
import Dashboard from './components/Dashboard.vue';
import BarChart from '@/components/BarChart.vue';
import BarHorizont from '@/components/BarHorizont.vue';
import logo from '@/assets/alta_logo_full.jpg';


// import from config.ini file in backend folder
import data from "../../backend/config.ini?raw";
import { ConfigIniParser } from "config-ini-parser";
let parser = new ConfigIniParser(); //Use default delimiter
parser.parse(data);
var backendIpAddress = parser.get("main", "backend_ip_address");
var backendPort = parser.get("main", "backend_port");
var companyName = parser.get("content", "company_name");


const state = reactive({
  data: [],
  isLoading: true,
})

const token = ref('')
const filterSubstring = ref('')
const isAuthorized = ref(true)
const login = ref('');
const password = ref('');
const authFormMessage = ref('')


// tables columns names
const articulArticulListTableColumns = {
    'catalog':'Код артикула','name':'Описание артикула','packs':'Кол-во','unit':'Ед.изм.',
    'netto':'Вес нетто','status':'Статус','cell_id':'Размещение', 
    'ngtd':'Номер ДТ', 'date':'Дата приема', 'g32':'№ тов.', 'g33':'Код ТНВЭД', 'guid_cat':'Уникальный номер артикула'
}

const arrivalGoodsArrivalListTableColumns = {
  'ngtd': 'Номер ДТ', 'date': 'Дата приема', 'g32': '№ тов.','g33': 'Код ТНВЭД',
    'g31': 'Наименование товара','g35': 'Вес брутто','g38': 'Вес нетто','g31_4': 'Кол.доп.ед',
    'g41a': 'Ед.изм.', 'status': 'Статус товара', 'cell_id': 'Размещение сырья'
}

const goodsMovementListTableColumns = {
  'ngtd':'Номер ДТ', 'g32':'№ тов.', 'g33':'Код ТНВЭД', 'g31':'Наименование товара', 'pin':'Кол-во пр.', 'pout':'Кол-во выд.',
  'g41a':'Ед.изм.', 'g38in':'Прих.нетто', 'g38out':'Выд.нетто', 'status':'Статус товара'
}

const filterArrivalDateFrom = ref();
const filterArrivalDateTo = ref();
const filterGoodsMovementDateOpFrom = ref()
const filterGoodsMovementDateOpTo = ref()

const showFiltersBar = ref(false);


const authHeader = () => {
  //
  let user = JSON.parse(localStorage.getItem('user'));

  if (user && user.access_token) {
    return { Authorization: 'Bearer ' + user.access_token };
  } else {
    return {};
  }
}


async function getData() {
  //
  try {
      state.data = [];

      state.articul = {};
      state.articul.barTnved = {};
      state.articul.barTnved.datax = [];
      state.articul.barTnved.datay = [];

      state.arrival = {};
      state.arrival.barTnved = {};
      state.arrival.barTnved.datax = [];
      state.arrival.barTnved.datay = [];

      state.goodsMovement = {};

      const response = await axios.get(`http://${backendIpAddress}:${backendPort}/dashboard/?`+filterSubstring.value, { headers: authHeader() });

      //let query = `http://${backendIpAddress}:${backendPort}/dashboard/` + '?token=' + token.value + filterSubstring.value
      //let query = 'http://localhost:8000/dashboard/' + '?token=' + token.value + filterSubstring.value
      // console.log('query =', query)
      //const response = await axios.get(query);
      
      // console.log('API RESPONSE =', response.status)
      // if (response.status == 200) {
      //   isAuthorized.value = true;
      // };

      state.data = response.data;

      state.companyName = state.data['company_name']
      state.updateDateTime = state.data['current_datetime']

      state.articul.cardDtCnt = state.data['articul_dt_cnt'][0]['articul_dt_cnt'];
      state.articul.cardArticulCnt = state.data['articul_articul_cnt'][0]['articul_articul_cnt'];
      for (let i of state.data['articul_tnved']) {
        state.articul.barTnved.datax.push(i['g33']);
        state.articul.barTnved.datay.push(i['cnt'])
      }   
      state.articul.listArticul = state.data['articul_articul']

      state.arrival.cardGoodsCnt = state.data['arrival_goods_cnt'][0]['arrival_goods_cnt'];
      state.arrival.cardDtCnt = state.data['arrival_dt_cnt'][0]['arrival_dt_cnt'];
      for (let i of state.data['arrival_tnved']) {
        state.arrival.barTnved.datax.push(i['g33']);
        state.arrival.barTnved.datay.push(i['cnt'])
      }   
      state.arrival.listGoodsArrival = state.data['arrival_goods_arrival']

      state.goodsMovement.listGoodsMovement = state.data['goods_movement']
    } catch (error) {
      console.error('Error fetching items', error.response.status);
      if (error.response.status == 401) {
        isAuthorized.value = false;
      }
    } finally {
      state.isLoading = false;
    }
};


async function updateData() {
  //
  state.isLoading = true;
  await getData();
};

const handleSubmit = async () => {
  //
  const filters = {
    'filterArrivalDateFrom': filterArrivalDateFrom, 
    'filterArrivalDateTo': filterArrivalDateTo, 
    'filterGoodsMovementDateOpFrom': filterGoodsMovementDateOpFrom, 
    'filterGoodsMovementDateOpTo': filterGoodsMovementDateOpTo, 
  }; 
  filterSubstring.value = '&';
  
  for (let f in filters) {
    if (filters[f].value) {
      filterSubstring.value += f + '=' + filters[f].value + '&'
    }
  }
  
  state.isLoading = true;
  await getData();   
};


onMounted(async () => {
    await getData()
});


const clearFilters = async () => {
  filterArrivalDateFrom.value = '';
  filterArrivalDateTo.value = '';
  filterGoodsMovementDateOpFrom.value = ''
  filterGoodsMovementDateOpTo.value = ''

  state.isLoading = true;
  await handleSubmit();
}

const authSubmit = async () => {
  //
  let formData = new FormData();
  formData.append('username', login.value);
  formData.append('password', password.value);

  try {
    const response = await axios.post(
      `http://${backendIpAddress}:${backendPort}/token`,
      formData, {headers: {'Content-Type': 'multipart/form-data'}});
    if (response.data.access_token) {
      localStorage.setItem('user', JSON.stringify(response.data));
      isAuthorized.value = true;
      state.isLoading = true;
      await getData();
    }

    // const response = await axios.post(
      
    //   `http://${backendIpAddress}:${backendPort}/dashboard/signin?` + 'login=' + login.value + '&password=' + password.value
    //   // 'http://localhost:8000/dashboard/signin?' + 'login=' + login.value + '&password=' + password.value
    // );
    // // console.log('accepted!');
    // // console.log('response data your_new_token =', response.data.your_new_token)
    // token.value = response.data.your_new_token;

    // console.log('API RESPONSE =', response.status)
    // if (response.status == 202) {
    //   isAuthorized.value = true;
    // };

    // state.isLoading = true;
    // await getData()
  } catch (error) {
    authFormMessage.value = 'Некорректный логин или пароль.'
    isAuthorized.value = false;
  };
}

const signOut = async () => {
  //
  localStorage.removeItem('user');
  login.value = '';
  password.value = '';
  isAuthorized.value = false;
  await getData();


  // try {
  //   let query = `http:///${backendIpAddress}:${backendPort}/dashboard/signout` + '?token=' + token.value
  //   // let query = 'http://localhost:8000/dashboard/signout' + '?token=' + token.value
  //   const response = await axios.post(query);
  //   // const response = await axios.post('http://localhost:8000/dashboard/signout');
  //   // console.log('sign out response =' , response.data.message)
  //   if (response.data.message == 'signed out') {
  //     login.value = '';
  //     password.value = '';
  //     isAuthorized.value = false;
  //   }
  // } catch (error) {
  //   console.error('unable to sign out', error);
  // }
};

const tabNumberVar = ref(1);  // initial tab number
const changeTabValue = (n) => {
  // rememberance of tab number from Dashboard component
  tabNumberVar.value = n;
};

</script>


<template>

<div v-if="!isAuthorized" class="flex">
    
  <div class="mt-40 mx-auto bg-gray-50 border rounded-lg overflow-hidden">
    <div class="py-2 px-5 bg-blue-400 text-center text-white text-lg">
      Dashboard | Витрина Свободного склада (СС)
    </div>
    <form @submit.prevent="authSubmit" enctype="multipart/form-data" class="mx-5 mt-2 ">
      <div class="my-2">
        <label class="block mb-2">Логин</label>
        <input
            type="text"
            v-model="login"
            id="login"
            name="login"
            class="border rounded-lg w-full h-8 p-3"
            placeholder=""
            required
            v-on:focus="authFormMessage=''"
          />
      </div>
      <div class="my-2">
        <label class="block mb-2">Пароль</label>
        <input
            type="password"
            v-model="password"
            id="password"
            name="password"
            class="border rounded-lg w-full h-8 p-3"
            placeholder=""
            required
            v-on:focus="authFormMessage=''"
          />
      </div>
      <div class="my-5 text-center">
        <button
          class="bg-green-500 text-white font-semibold rounded-full px-3 py-2 w-60
            shadow-md hover:shadow-lg hover:bg-green-600"
          type="submit"
        >
        Вход
        </button>
      </div>
    </form>
    <div class="mb-3 text-red-500 text-center">
      {{ authFormMessage }}
    </div>
  </div>
</div>


<div v-if="isAuthorized" class="">

  <!-- **************   FILTERS BAR    ******************* -->
  <div v-if="showFiltersBar" class="absolute z-10 w-screen h-full bg-black bg-opacity-50">
    <div  class="absolute z-20 top-0 right-0 border w-96 h-full bg-white">
  <!-- <div v-if="showFiltersBar" class="absolute z-10 right-0 border w-96 h-screen bg-white"> -->
    <div class="p-3 bg-gray-200 overflow-auto">
    <div class="float-left text-xl ">
      Фильтры данных
    </div>
    <div class="float-right cursor-pointer hover:text-gray-500" @click="showFiltersBar=false">
      <i class="pi pi-times" style="font-size: 1.5rem"></i>
    </div>
    </div>

    <form @submit.prevent="handleSubmit" class="mx-0 mt-3 ">

      <div class="mt-5 mb-2 ml-3 font-semibold">ПРИХОД ТОВАРА</div>

      <div class="mx-5 mb-2">
        <label class="formLabelStyle">Дата приёма</label>
        <div class="flex ">
          <div class="pt-1">c</div>
          <input
            type="date"
            v-model="filterArrivalDateFrom"
            id="filterArrivalDateFrom"
            name="filterArrivalDateFrom"
            :class="filterArrivalDateFrom ? 'formInputStyleFilled' : 'formInputStyle'"
            placeholder=""
          />
          <div class="pt-1">по</div>
          <input
            type="date"
            v-model="filterArrivalDateTo"
            id="filterArrivalDateTo"
            name="filterArrivalDateTo"
            :class="filterArrivalDateTo ? 'formInputStyleFilled' : 'formInputStyle'"
            placeholder=""
          />   
        </div>
      </div>

      <hr class="mt-7"> 

      <div class="mt-5 mb-2 ml-3 font-semibold">ДВИЖЕНИЕ ТОВАРА</div>

      <div class="mx-5 mb-2">
        <label class="formLabelStyle">Дата операции</label>
        <div class="flex ">
          <div class="pt-1">c</div>
          <input
            type="date"
            v-model="filterGoodsMovementDateOpFrom"
            id="filterGoodsMovementDateOpFrom"
            name="filterGoodsMovementDateOpFrom"
            :class="filterGoodsMovementDateOpFrom ? 'formInputStyleFilled' : 'formInputStyle'"
            placeholder=""
          />
          <div class="pt-1">по</div>
          <input
            type="date"
            v-model="filterGoodsMovementDateOpTo"
            id="filterGoodsMovementDateOpTo"
            name="filterGoodsMovementDateOpTo"
            :class="filterGoodsMovementDateOpTo ? 'formInputStyleFilled' : 'formInputStyle'"
            placeholder=""
          />   
        </div>
      </div>

      <hr class="mt-7">

      <div class="mt-7 flex justify-center space-x-5 py-3 px-5 text-center">
        <button
          class="bg-sky-400 text-white font-semibold rounded-full w-60
            drop-shadow-md hover:shadow-lg hover:bg-sky-500"
          type="submit"
        >
        Применить
        </button>
        <button
          class="bg-rose-400 text-white font-semibold rounded-full px-3 py-2 w-60
            drop-shadow-md hover:shadow-lg hover:bg-rose-500"
          type="button"
          @click="clearFilters()"
        >
        Сбросить
        </button>
      </div>
    </form>

  </div>
</div>

<!-- **************   HEADER    ******************* -->
<nav class="bg-gradient-to-r from-sky-600 to-sky-400 px-10 py-3 text-white overflow-auto">  
  <div class="text-center lg:flex lg:float-left text-xl">
    <div class="inline-block px-4 border-r-2">{{ companyName }}</div>
    <div class="inline-block px-4 border-r-2">Dashboard</div>
    <div class="inline-block px-4">Витрина Свободного склада (СС)</div>
  </div>
  <div class="text-center lg:flex lg:float-right">
    <div class="inline-block px-4 text-base">{{ state.updateDateTime }}</div>
    <!-- 09-09-2024 17:30 -->
    <div class="header-btn"><i class="pi pi-refresh" style="font-size: 1.3rem" @click="updateData()"></i></div>
    <div class="header-btn"><i class="pi pi-ellipsis-v" style="font-size: 1.3rem"></i></div>
    <div class="header-btn"><i class="pi pi-sign-out" style="font-size: 1.3rem" @click="signOut()"></i></div>
    <div class="header-btn" @click="showFiltersBar=(showFiltersBar) ? false:true">
      <i class="pi pi-filter" style="font-size: 1.3rem"></i></div>
  </div>
</nav>


  <!-- Show loading spinner while loading is true -->
  <div v-if="state.isLoading" class="text-center text-gray-500 py-6">
    <PulseLoader />
     ЗАГРУЗКА ДАННЫХ...
  </div>

  <!-- Show when loading is done -->
  <div v-else class="bg-gray-50">
  <Dashboard 
    @change-tab="changeTabValue"
    :tabNumberVar = "tabNumberVar"

    :articulBarTnvedDatax = "state.articul.barTnved.datax" 
    :articulBarTnvedDatay="state.articul.barTnved.datay" 
    :articulCardDtCnt="state.articul.cardDtCnt" 
    :articulCardArticulCnt="state.articul.cardArticulCnt" 
    :articulListName="'Артикул на складе'" 
    :articulListArticul="state.articul.listArticul" 
    :articulListTableColumns="articulArticulListTableColumns"

    :arrivalBarTnvedDatax = "state.arrival.barTnved.datax" 
    :arrivalBarTnvedDatay="state.arrival.barTnved.datay" 
    :arrivalCardGoodsCnt="state.arrival.cardGoodsCnt" 
    :arrivalCardDtCnt="state.arrival.cardDtCnt" 
    :arrivalListName="'Приход товара'" 
    :arrivalListGoodsArrival="state.arrival.listGoodsArrival" 
    :arrivalListTableColumns="arrivalGoodsArrivalListTableColumns"

    :goodsMovementListName="'Движение товара по складу	'" 
    :goodsMovementListAccountBook="state.goodsMovement.listGoodsMovement" 
    :goodsMovementListTableColumns="goodsMovementListTableColumns"
  /> 

  <footer>
    <div class="bg-slate-200 flex box-content border border-slate-200 h-7 pl-5 pr-10 text-left text-slate-500 text-sm font-semibold">
      <div class="flex-1"><img class="h-7" :src="logo"></div>
      <div class="py-1">&#169; "Альта-Софт" Лиц.: 00008</div>
    </div>
  </footer>

  </div>
</div>
</template>


<style lang="postcss" scoped>
.header-btn {
  @apply inline-block mx-3 mt-1 text-yellow-100 cursor-pointer hover:text-yellow-300
}

.formLabelStyle {
  @apply mx-1 block text-xs font-bold text-blue-500
}

.formInputStyle {
  @apply border-b-2 border-blue-300 text-gray-300 text-base font-medium w-36 py-1 px-1 mb-2
  hover:border-blue-400 focus:outline-none focus:border-blue-500 cursor-pointer
}

.formInputStyleFilled {
  @apply border-b-2 border-blue-300 text-gray-600 text-base font-medium w-36 py-1 px-1 mb-2
  hover:border-blue-400 focus:outline-none focus:border-blue-500 cursor-pointer
}
</style>