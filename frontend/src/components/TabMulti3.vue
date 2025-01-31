<script setup>
import { defineProps, computed, reactive } from 'vue';
import ListMulti3 from '@/components/ListMulti3.vue';

  
const props = defineProps({
  multiListName: String,
  filterProcGoodsDateFrom: String,
  filterProcGoodsDateTo: String,
});

</script>

<template>
  
  <div class="grid grid-cols-6 gap-3 m-2 mb-64">

    <div class="col-span-6">
      <div class="">
        <ListMulti3 :name="multiListName" :filterProcGoodsDateFrom="filterProcGoodsDateFrom" :filterProcGoodsDateTo="filterProcGoodsDateTo"/>
      </div>
    </div>

  </div>
  
</template>
