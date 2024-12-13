<script setup>
import { defineProps, computed, reactive } from 'vue';
import BarHorizont from '@/components/BarHorizont.vue';
import BarChart from '@/components/BarChart.vue';
import Card from '@/components/Card.vue';
import List from '@/components/List.vue';

  
const props = defineProps({
  accountBookBarRecTnvedQuantityDatax: Array,
  accountBookBarRecTnvedQuantityDatay: Array,
  accountBookCardRecProductQuantity: 0,
  accountBookCardRecDtQuantity: 0,
  accountBookListName: String,
  accountBookListAccountBook: Array,
  accountBookListTableColumns: Object,
});

</script>

<template>
  
  <div class="grid grid-cols-6 gap-3 m-2">

    <div class="col-span-2">

      <div class="grid grid-rows-3 grid-flow-col gap-3">

        <div class="grid grid-cols-2 gap-3">
          <div class="">
            <Card :label="'Количество принятого товара'" :value="accountBookCardRecProductQuantity" />
          </div>
          <div class="">
            <Card :label="'Количество принятых ДТ'" :value="accountBookCardRecDtQuantity" />
          </div>
        </div>

        <div class=" row-span-2">
          <BarChart :name="'bar-h-03'" :title="'Принятые ТНВЭД'" :xtitle="'Группа ТНВЭД'" :ytitle="'Количество'"
          :datax="accountBookBarRecTnvedQuantityDatax"
          :datay="accountBookBarRecTnvedQuantityDatay" 
          :barcolor="'#7B68EE'" 
          />
        </div>

      </div>

    </div>

    <div class="col-span-4">
      <div class="">
        <List :name="accountBookListName" :data="accountBookListAccountBook" :listTableColumns="accountBookListTableColumns" />
      </div>
    </div>

  </div>
  
</template>

<!-- #00E396  #FF69B4  #CD5C5C  #FFA07A  #7B68EE  #00FF7F  #00BFFF -->
