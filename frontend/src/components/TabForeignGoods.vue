<script setup>
import { defineProps, computed, reactive } from 'vue';
import List from '@/components/List.vue';

  
const props = defineProps({
  foreignGoodsListName: String,
  foreignGoodsList: Array,
  foreignGoodsListTableColumns: Object,
});

</script>

<template>
  
  <div class="grid grid-cols-6 gap-3 m-2">

    <div class="col-span-6">
      <div class="">
        <List :name="foreignGoodsListName" :data="foreignGoodsList" :listTableColumns="foreignGoodsListTableColumns" 
          :limitRecords="13" :tableHeight="'600px'" />
      </div>
    </div>

  </div>
  
</template>
