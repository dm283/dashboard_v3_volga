<script setup>
import { defineProps, computed, reactive } from 'vue';
import List from '@/components/List.vue';

  
const props = defineProps({
  goodsMovementListName: String,
  goodsMovementListAccountBook: Array,
  goodsMovementListTableColumns: Object,
});

</script>

<template>
  
  <div class="grid grid-cols-6 gap-3 m-2">

    <div class="col-span-6">
      <div class="">
        <List :name="goodsMovementListName" :data="goodsMovementListAccountBook" :listTableColumns="goodsMovementListTableColumns" />
      </div>
    </div>

  </div>
  
</template>
