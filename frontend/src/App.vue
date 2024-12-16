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
const foreignGoodsListTableColumns = {
'goods':		'Наименование товара',
'g33':	'Код ТНВЭД',
'nbux':		'Документ бух.учета',
'ngtd':		'Номер ДТ',
'packs':		'Кол-во учет',
'ed_izm':		'Ед.изм.учет',
'packs_dt':	'Кол-во ДТ',
'g41a':		'Ед.изм.ДТ',
'datebux':		'Дата размещ.',
'naccount':	'№ субсчета',
'packs_0':		'Тек.остаток',
'place':		'Место хранения',
'packs_1':		'Передано в произ-во',
'packs_2':		'Потребление',
'packs_3':		'Списание (форсмажор)',
'packs_4':		['Уничтожение', '(ст. 160 ФЗ-289)'],
// 'packs_4':		'Уничтожение (ст. 160 ФЗ-289)',
'packs_5':		['Передача товара', '(п.9 ст.213 ТК ЕАЭС)'],
// 'packs_5':		'Передача товара (п.9 ст.213 ТК ЕАЭС)',
'packs_6':		['Изменение статуса', '(ч.6, ст. 160 ФЗ-289)'],
// 'packs_6':		'Изменение статуса (ч.6, ст. 160 ФЗ-289)',
'packs_7':		'Помещение под иную ТП',
'packs_8':		['Вывоз товаров', '(оборудования)', '(п.5 ст.213 ТК ЕАЭС)'],
// 'packs_8':		'Вывоз товаров (оборудования) (п.5 ст.213 ТК ЕАЭС)',
'guid_cat':	'Номер идентификатора'
}

const eaesGoodsListTableColumns = {
'nn':		'№ п/п',
'goods':		'Наименование товара',
'g33':		'Код ТНВЭД',
'status':		'Статус',
'packs':		'Количество',
'ed_izm':		'Ед.изм.',
'ndoc':		'Наименование документа'
}


const filterForeignGoodsDateFrom = ref();
const filterForeignGoodsDateTo = ref();
const filterEaesGoodsDateFrom = ref()
const filterEaesGoodsDateTo = ref()

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

      state.foreignGoods = {};
      state.eaesGoods = {};

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

      state.foreignGoods.listGoods = state.data['foreign_goods_list']
      state.eaesGoods.listGoods = state.data['eaes_goods_list']
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
    'filterForeignGoodsDateFrom': filterForeignGoodsDateFrom, 
    'filterForeignGoodsDateTo': filterForeignGoodsDateTo, 
    'filterEaesGoodsDateFrom': filterEaesGoodsDateFrom, 
    'filterEaesGoodsDateTo': filterEaesGoodsDateTo, 
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
  filterForeignGoodsDateFrom.value = '';
  filterForeignGoodsDateTo.value = '';
  filterEaesGoodsDateFrom.value = ''
  filterEaesGoodsDateTo.value = ''

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
      Витрина Свободного склада (СС)
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

      <div class="mt-5 mb-2 ml-3 font-semibold">ИНОСТРАННЫЕ ТОВАРЫ</div>

      <div class="mx-5 mb-2">
        <label class="formLabelStyle">Дата размещения</label>
        <div class="flex ">
          <div class="pt-1">c</div>
          <input
            type="date"
            v-model="filterForeignGoodsDateFrom"
            id="filterForeignGoodsDateFrom"
            name="filterForeignGoodsDateFrom"
            :class="filterForeignGoodsDateFrom ? 'formInputStyleFilled' : 'formInputStyle'"
            placeholder=""
          />
          <div class="pt-1">по</div>
          <input
            type="date"
            v-model="filterForeignGoodsDateTo"
            id="filterForeignGoodsDateTo"
            name="filterForeignGoodsDateTo"
            :class="filterForeignGoodsDateTo ? 'formInputStyleFilled' : 'formInputStyle'"
            placeholder=""
          />   
        </div>
      </div>

      <hr class="mt-7"> 

      <div class="mt-5 mb-2 ml-3 font-semibold">ТОВАРЫ ЕАЭС</div>

      <div class="mx-5 mb-2">
        <label class="formLabelStyle">Дата</label>
        <div class="flex ">
          <div class="pt-1">c</div>
          <input
            type="date"
            v-model="filterEaesGoodsDateFrom"
            id="filterEaesGoodsDateFrom"
            name="filterEaesGoodsDateFrom"
            :class="filterEaesGoodsDateFrom ? 'formInputStyleFilled' : 'formInputStyle'"
            placeholder=""
          />
          <div class="pt-1">по</div>
          <input
            type="date"
            v-model="filterEaesGoodsDateTo"
            id="filterEaesGoodsDateTo"
            name="filterEaesGoodsDateTo"
            :class="filterEaesGoodsDateTo ? 'formInputStyleFilled' : 'formInputStyle'"
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
    <div class="inline-block px-4">Витрина Свободного склада (СС)</div>
  </div>
  <div class="text-center lg:flex lg:float-right">
    <div class="inline-block px-4 text-base">{{ state.updateDateTime }}</div>
    <!-- 09-09-2024 17:30 -->
    <div class="header-btn"><i class="pi pi-refresh" style="font-size: 1.3rem" @click="updateData()"></i></div>
    <!-- <div class="header-btn"><i class="pi pi-ellipsis-v" style="font-size: 1.3rem"></i></div> -->
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

    :foreignGoodsListName="'Иностранные товары'" 
    :foreignGoodsList="state.foreignGoods.listGoods" 
    :foreignGoodsListTableColumns="foreignGoodsListTableColumns"

    :eaesGoodsListName="'Товары ЕАЭС'" 
    :eaesGoodsList="state.eaesGoods.listGoods" 
    :eaesGoodsListTableColumns="eaesGoodsListTableColumns"
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