<script setup>
import { defineProps, computed, reactive } from 'vue';
import BarHorizont from '@/components/BarHorizont.vue';
import BarChart from '@/components/BarChart.vue';
import Card from '@/components/Card.vue';
import List from '@/components/List.vue';

  
const props = defineProps({
  arrivalBarTnvedDatax: Array,
  arrivalBarTnvedDatay: Array,
  arrivalCardGoodsCnt: 0,
  arrivalCardDtCnt: 0,
  arrivalListName: String,
  arrivalListGoodsArrival: Array,
  arrivalListTableColumns: Object,
});

</script>

<template>
  
  <div class="flex flex-col md:flex-row m-2 gap-3 ">

    <div class="flex-none w-fit md:w-auto">
      
      <div class="flex flex-col gap-3">

        <div class="grid grid-cols-2 gap-3">
          <div class="">
            <Card :label="'Количество принятого товара'" :value="arrivalCardGoodsCnt" />
          </div>
          <div class="">
            <Card :label="'Количество принятых ДТ(77)'" :value="arrivalCardDtCnt" />
          </div>
        </div>

        <div class="">
          <BarChart :name="'bar-h-03'" :title="'Принятые ТНВЭД(7)'" :xtitle="'Группа ТНВЭД'" :ytitle="'Количество'"
          :datax="arrivalBarTnvedDatax"
          :datay="arrivalBarTnvedDatay" 
          :barcolor="'#7B68EE'" 
          />
        </div>

      </div>

    </div>

    <div class="flex-auto w-auto md:w-64">
      <div class="">
        <List :name="arrivalListName" :data="arrivalListGoodsArrival" :listTableColumns="arrivalListTableColumns" />
      </div>
    </div>

    </div>
  
</template>

<!-- #00E396  #FF69B4  #CD5C5C  #FFA07A  #7B68EE  #00FF7F  #00BFFF -->
