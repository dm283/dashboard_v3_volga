<script setup>
import { defineProps, computed, reactive } from 'vue';
import List from '@/components/List.vue';

  
const props = defineProps({
  ispolProductedGoodsListName: String,
  ispolProductedGoodsList: Array,
  ispolProductedGoodsListTableColumns: Object,
});

</script>

<template>
  
  <div class="grid grid-cols-6 gap-3 m-2">

    <div class="col-span-6">
      <div class="">
        <List :name="ispolProductedGoodsListName" :data="ispolProductedGoodsList" :listTableColumns="ispolProductedGoodsListTableColumns" 
          :limitRecords="14" :tableHeight="'600px'"/>
      </div>
    </div>

  </div>
  
</template>
