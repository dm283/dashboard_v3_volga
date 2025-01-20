<script setup>
import { defineProps, computed, reactive } from 'vue';
import ListMulti from '@/components/ListMulti.vue';

  
const props = defineProps({
  multiListName: String,
});

</script>

<template>
  
  <div class="grid grid-cols-6 gap-3 m-2 mb-16">

    <div class="col-span-6">
      <div class="">
        <ListMulti :name="multiListName"/>
      </div>
    </div>

  </div>
  
</template>
