<script setup>
import { defineProps, ref, reactive, onMounted, computed } from 'vue';
import 'primeicons/primeicons.css';
// import router from '@/router';
import axios from 'axios';

const props = defineProps({
  name: String,
  filterProcGoodsDateFrom: String,
  filterProcGoodsDateTo: String,
});

</script>


<template>

<div class="" v-if="props.name"> <!-- necessary div for waiting data from root component!!! -->

<div @click="" class="listArea m-0 px-3 py-2 border border-gray-200 rounded-lg
  bg-white drop-shadow-md hover:drop-shadow-lg ">

<!-- *******************************  NAV AREA  ************************* --> 
<nav class="overflow-auto">
  <div class="text-sm font-semibold inline-block">
    <div class="text-xl font-normal text-center">
      Товары, изготовленные (полученные) с использованием товаров, помещенных под таможенную процедуру
      свободного склада, и товаров Евразийского экономического союза, не помещенных под таможенную процедуру свободного склада
    </div>
  </div>

  <div class="float-right">
  <!-- ***************   PAGINATION BLOCK   ********************* -->
  <div id="paginationBlock" class="inline-block mr-3">
  <div class="space-x-1.5">
    <div class="paginationBtn" @click="">
      <i class="pi pi-angle-double-left" style="font-size: 1rem"></i>
    </div>
    <div class="paginationBtn" @click="">
      <i class="pi pi-angle-left" style="font-size: 1rem"></i>
    </div>
    0-0 из 0
    <div class="paginationBtn" @click="">
      <i class="pi pi-angle-right" style="font-size: 1rem"></i>
    </div>
    <div class="paginationBtn" @click="">
      <i class="pi pi-angle-double-right" style="font-size: 1rem"></i>
    </div>
  </div>
  </div>

  <!-- DOWNLOAD BUTTON DROPDOWN -->
  <div class="inline-block mr-1">
    <button class="w-8 h-8 rounded-lg bg-green-400 text-white hover:opacity-75" 
      @click="">
      <i class="pi pi-download" style="font-size: 1rem"></i>
    </button>
    <!-- <div v-show="isDropDownloadShow" class="mt-1 -ml-11 w-20 border rounded-md border-gray-300 
      bg-white text-xs font-semilbold absolute z-10 overflow-hidden">
      <ul @click="toggleDropdown('download')">
        <li class="h-8 pl-3 py-1.5 uppercase cursor-pointer hover:bg-gray-100" 
           @click="exportFile(dataSet=state.localData, fileName='dashboard_data', fileType=option)" v-for="option in ['xlsx', 'csv']">{{ option }}</li>
      </ul>
    </div> -->
  </div>

</div>

<div class="flex text-sm font-semibold text-slate-400">
  <div class="">Дата отчёта</div> 
  <div class="ml-1">{{ props.filterProcGoodsDateFrom.slice(8, 10) }}/{{ props.filterProcGoodsDateFrom.slice(5, 7) }}/{{ props.filterProcGoodsDateFrom.slice(0, 4) }}
    - {{ props.filterProcGoodsDateTo.slice(8, 10) }}/{{ props.filterProcGoodsDateTo.slice(5, 7) }}/{{ props.filterProcGoodsDateTo.slice(0, 4) }}
  </div>
</div>

</nav>

<!-- table area ************************* --> 
<section class="mt-2 border rounded-lg overflow-x-auto">
<table class="w-full">

  <thead>
    <!-- 1st level -->
    <tr class="h-8 bg-blue-400 text-sm font-semibold text-white text-center">
      <td rowspan="2" class="border">
        <div class="px-2 py-2 min-w-max">
          № п/п
        </div>
      </td>
      <td rowspan="2" class="border">
        <div class="px-2 py-2 ">
          Наименование товара
        </div>
      </td>
      <td rowspan="2" class="border">
        <div class="px-2 py-2 ">
          Код товара по ТН ВЭД ЕАЭС
        </div>
      </td>
      <td rowspan="2" class="border">
        <div class="px-2 py-2 ">
          Статус товара
        </div>
      </td>
      <td colspan="3" class="border">
        <div class="px-2 py-2 min-w-max">
          <div>Нормы выхода/нормы расхода</div>
        </div>
      </td>

    </tr>
    <!-- 2nd level -->
    <tr class="h-8 bg-blue-400 text-sm font-semibold text-white text-center">

      <td class="border">
        <div class="px-2 py-2 ">
          Количество
        </div>
      </td>
      <td class="border">
        <div class="px-2 py-2 ">
          Единица измерения
        </div>
      </td>
      <td class="border">
        <div class="px-2 py-2 ">
          Номер документа
        </div>
      </td>

    </tr>

    <!-- 3rd level -->
    <tr class="h-8 bg-blue-400 text-sm font-semibold text-white text-center">
      <td class="border" v-for="n in Array.from({length: 7}, (_, i) => i + 1)"><div class="px-2 py-2" >{{ n }}</div></td>
    </tr>

  </thead>

  <tbody>

    <tr class="border-t text-xs font-normal text-center cursor-pointer hover:bg-gray-100" >
      <td colspan="5" class=""><div class="px-2 py-2 text-sm text-left min-w-max font-bold">
        Товары, изготовленные (полученные) с использованием товаров, помещенных под таможенную процедуру свободного склада
      </div></td>
    </tr>
    <tr class="border-t text-xs font-normal text-center cursor-pointer hover:bg-gray-100" >
      <td class=""><div class="px-2 py-2 min-w-max">1</div></td>
      <td class="" v-for="n in [...Array(6).keys()]"><div class="px-2 py-2 min-w-max">-</div></td>
    </tr>

    <tr class="border-t text-xs font-normal text-center cursor-pointer hover:bg-gray-100" >
      <td colspan="5" class=""><div class="px-2 py-2 text-sm text-left min-w-max font-bold">
        Товары, помещенные под таможенную процедуру свободного склада, использованные при изготовлении (получении) товаров
      </div></td>
    </tr>
    <tr class="border-t text-xs font-normal text-center cursor-pointer hover:bg-gray-100" >
      <td class=""><div class="px-2 py-2 min-w-max">1</div></td>
      <td class="" v-for="n in [...Array(6).keys()]"><div class="px-2 py-2 min-w-max">-</div></td>
    </tr>

    <tr class="border-t text-xs font-normal text-center cursor-pointer hover:bg-gray-100" >
      <td colspan="5" class=""><div class="px-2 py-2 text-sm text-left min-w-max font-bold">
        Товары ЕАЭС, не помещенные под таможенную процедуру свободного склада, использованные при изготовлении (получении) товаров
      </div></td>
    </tr>
    <tr class="border-t text-xs font-normal text-center cursor-pointer hover:bg-gray-100" >
      <td class=""><div class="px-2 py-2 min-w-max">1</div></td>
      <td class="" v-for="n in [...Array(6).keys()]"><div class="px-2 py-2 min-w-max">-</div></td>
    </tr>

  </tbody>

</table>
</section>

</div>
</div>
</template>


<style lang="postcss" scope>
.listArea {
  height: v-bind('props.tableHeight');
}

.paginationBtn {
  @apply bg-gray-50 inline-block cursor-pointer w-8 h-8 border rounded-lg text-center py-1
}

.paginationBtn:hover {
  @apply bg-gray-100
}

#btn-1:hover, #btn-2:hover, #btn-3:hover,
#btn-4:hover, #btn-5:hover, #btn-6:hover {
  background-color: #E4E4E7;
  color: #18181B;
}
</style>