<script setup>
import { defineProps, computed, reactive } from 'vue';
import List from '@/components/List.vue';

  
const props = defineProps({
  eaesGoodsListName: String,
  eaesGoodsList: Array,
  eaesGoodsListTableColumns: Object,
});

</script>

<template>
  
  <div class="grid grid-cols-6 gap-3 m-2">

    <div class="col-span-6">
      <div class="">
        <List :name="eaesGoodsListName" :data="eaesGoodsList" :listTableColumns="eaesGoodsListTableColumns" 
          :limitRecords="14" :tableHeight="'600px'"/>
      </div>
    </div>

  </div>
  
</template>
