<script setup>
import { defineProps, computed, reactive } from 'vue';
import ListMulti2 from '@/components/ListMulti2.vue';

  
const props = defineProps({
  multiListName: String,
  filterProcGoodsDateFrom: String,
  filterProcGoodsDateTo: String,
});

</script>

<template>
  
  <div class="grid grid-cols-6 gap-3 m-2 mb-36">

    <div class="col-span-6">
      <div class="">
        <ListMulti2 :name="multiListName" :filterProcGoodsDateFrom="filterProcGoodsDateFrom" :filterProcGoodsDateTo="filterProcGoodsDateTo"/>
      </div>
    </div>

  </div>
  
</template>
