<script setup>
import { defineProps, ref, reactive, onMounted, computed } from 'vue';
import 'primeicons/primeicons.css';
// import router from '@/router';
import axios from 'axios';

const props = defineProps({
  name: String,
});

</script>


<template>

<div class="" v-if="props.name"> <!-- necessary div for waiting data from root component!!! -->

<div @click="" class="listArea m-0 px-3 py-2 border border-gray-200 rounded-lg
  bg-white drop-shadow-md hover:drop-shadow-lg ">

<!-- *******************************  NAV AREA  ************************* --> 
<nav class="overflow-auto">
  <div class="text-sm font-semibold inline-block">
    <div class="text-xl font-normal">Товары, помещенные под таможенную процедуру свободного склада</div>
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
          Единица измерения
        </div>
      </td>
      <td colspan="3" class="border">
        <div class="px-2 py-2 min-w-max">
          <div>Товары, помещенные под таможенную процедуру</div>
          <div>свободного склада (количество)</div>
        </div>
      </td>
      <td colspan="5" class="border">
        <div class="px-2 py-2 min-w-max">
          <div>Использование товаров, помещенных под таможенную</div>
          <div>процедуру свободного склада (количество)</div>
        </div>
      </td>
      <td rowspan="2" class="border">
        <div class="px-2 py-2 ">
          Потребление в процессе производства (переработки товаров)
        </div>
      </td>
      <td colspan="2" class="border">
        <div class="px-2 py-2">
          Уничтожение
        </div>
      </td>
      <td rowspan="2" class="border">
        <div class="px-2 py-2">
          Получение приплода, выращивание и откорм животных, птиц, аквакультуры, а также выращивание деревьев и растений
        </div>
      </td>
      <td rowspan="2" class="border">
        <div class="px-2 py-2">
          Хранение
        </div>
      </td>
      <td rowspan="2" class="border">
        <div class="px-2 py-2">
          Использование
        </div>
      </td>
      <td colspan="4" class="border">
        <div class="px-2 py-2 min-w-max">
          <div>Вывоз товаров без завершения 			</div>
          <div>таможенной процедуры свободного		</div>	
            <div>склада с разрешения таможенного		</div>	
              <div>органа			</div>
        </div>
      </td>
      <td colspan="4" class="border">
        <div class="px-2 py-2 min-w-max">
          <div>Завершение таможенной процедуры	</div>		
          <div>свободного склада			</div>
        </div>
      </td>
      <td rowspan="2" class="border">
        <div class="px-2 py-2">
          Реквизиты документа бух.учета
        </div>
      </td>
      <td rowspan="2" class="border">
        <div class="px-2 py-2">
          Номер декларации на товар
        </div>
      </td>
      <td rowspan="2" class="border">
        <div class="px-2 py-2">
          Передача на складирование (место хранения)
        </div>
      </td>
      <td rowspan="2" class="border">
        <div class="px-2 py-2">
          Передача в производство (цель переработки, использование в производстве)
        </div>
      </td>
      <td rowspan="2" class="border">
        <div class="px-2 py-2">
          Передача товаров во владение в соотв. с п.9 ст. 213 ТК ЕАЭС
        </div>
      </td>
      <td rowspan="2" class="border">
        <div class="px-2 py-2">
          Изменение статуса товара (ч.6, ст. 160 ФЗ 3289-ФЗ)
        </div>
      </td>
      <td rowspan="2" class="border">
        <div class="px-2 py-2">
          Помещение под иную таможенную процедуру
        </div>
      </td>
      <td rowspan="2" class="border">
        <div class="px-2 py-2">
          Вывоз товаров с терр. св. склада в соотв. с п.5 ст. 213 ТК ЕАЭС № разрешения
        </div>
      </td>
      <td rowspan="2" class="border">
        <div class="px-2 py-2">
          Номер сквозного идентификатора
        </div>
      </td>
      <td rowspan="2" class="border">
        <div class="px-2 py-2">
          Номер субсчета
        </div>
      </td>

    </tr>
    <!-- 2nd level -->
    <tr class="h-8 bg-blue-400 text-sm font-semibold text-white text-center">

      <td class="border">
        <div class="px-2 py-2 ">
          на начало отчетного периода
        </div>
      </td>
      <td class="border">
        <div class="px-2 py-2 ">
          за отчетный период
        </div>
      </td>
      <td class="border">
        <div class="px-2 py-2 ">
          на конец отчетного периода
        </div>
      </td>

      <td class="border">
        <div class="px-2 py-2 ">
          строительство объектов недвижимости на территории свободного склада (наименование объекта)
        </div>
      </td>
      <td class="border">
        <div class="px-2 py-2 ">
          оборудование, машины и агрегаты, используемые на территории свободного склада (запасные части)
        </div>
      </td>
      <td class="border">
        <div class="px-2 py-2 ">
          эксплуатация и функционирование свободного склада
        </div>
      </td>
      <td class="border">
        <div class="px-2 py-2 ">
          производство (переработка товаров)
        </div>
      </td>
      <td class="border">
        <div class="px-2 py-2 ">
          отбор проб и образцов
        </div>
      </td>

      <td class="border">
        <div class="px-2 py-2 ">
          в результате аварии
        </div>
      </td>
      <td class="border">
        <div class="px-2 py-2 ">
          по разрешению таможенного органа
        </div>
      </td>

      <td class="border">
        <div class="px-2 py-2 ">
          ремонт, техническое обслуживание оборудования
        </div>
      </td>
      <td class="border">
        <div class="px-2 py-2 ">
          технические испытания, исследования, демонстрация
        </div>
      </td>
      <td class="border">
        <div class="px-2 py-2 ">
          вывоз на другой свободный склад
        </div>
      </td>
      <td class="border">
        <div class="px-2 py-2 ">
          вывоз для завершения таможенной процедуры свободного склада в иной таможенный орган
        </div>
      </td>

      <td class="border">
        <div class="px-2 py-2 ">
          наименование товара/код товара по ТН ВЭД ЕАЭС
        </div>
      </td>
      <td class="border">
        <div class="px-2 py-2 ">
          код таможенной процедуры
        </div>
      </td>
      <td class="border">
        <div class="px-2 py-2 ">
          номер таможенной декларации
        </div>
      </td>
      <td class="border">
        <div class="px-2 py-2 ">
          количество единиц измерения
        </div>
      </td>

    </tr>

    <!-- 3rd level -->
    <tr class="h-8 bg-blue-400 text-sm font-semibold text-white text-center">
      <td class="border" v-for="n in Array.from({length: 36}, (_, i) => i + 1)"><div class="px-2 py-2" >{{ n }}</div></td>
    </tr>

  </thead>

  <tbody>

    <tr class="border-t text-xs font-normal text-center cursor-pointer hover:bg-gray-100" >
      <td colspan="5" class=""><div class="px-2 py-2 text-sm text-left min-w-max font-bold">Иностранные товары</div></td>
    </tr>
    <tr class="border-t text-xs font-normal text-center cursor-pointer hover:bg-gray-100" >
      <td class=""><div class="px-2 py-2 min-w-max">1</div></td>
      <td class=""><div class="px-2 py-2 min-w-max">товар1</div></td>
      <td class="" v-for="n in [...Array(34).keys()]"><div class="px-2 py-2 min-w-max">0</div></td>
    </tr>

    <tr class="border-t text-xs font-normal text-center cursor-pointer hover:bg-gray-100" >
      <td colspan="5" class=""><div class="px-2 py-2 text-sm text-left min-w-max font-bold">Товары Евразийского экономического союза</div></td>
    </tr>
    <tr class="border-t text-xs font-normal text-center cursor-pointer hover:bg-gray-100" >
      <td class=""><div class="px-2 py-2 min-w-max">1</div></td>
      <td class=""><div class="px-2 py-2 min-w-max">товар2</div></td>
      <td class="" v-for="n in [...Array(34).keys()]"><div class="px-2 py-2 min-w-max">0</div></td>
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