<script setup>
import { ref, defineProps, computed, reactive } from 'vue';
import TabArticul from '@/components/TabArticul.vue';
import TabArrival from '@/components/TabArrival.vue';
import TabGoodsMovement from '@/components/TabGoodsMovement.vue';

  
const props = defineProps({
  tabNumberVar: 1,

  articulBarTnvedDatax: Array,
  articulBarTnvedDatay: Array,
  articulCardDtCnt: 0,
  articulCardArticulCnt: 0,
  articulListName: String,
  articulListArticul: Array,
  articulListTableColumns: Object,

  arrivalBarTnvedDatax: Array,
  arrivalBarTnvedDatay: Array,
  arrivalCardGoodsCnt: 0,
  arrivalCardDtCnt: 0,
  arrivalListName: String,
  arrivalListGoodsArrival: Array,
  arrivalListTableColumns: Object,

  goodsMovementListName: String,
  goodsMovementListAccountBook: Array,
  goodsMovementListTableColumns: Object,
});

const emit = defineEmits(['changeTab']) // emit

const openTab = ref(props.tabNumberVar);

const toggleTabs = (tabNumber) => {
  openTab.value = tabNumber;
  emit('changeTab', tabNumber) // emit
};

</script>

<template>
  
  <nav class="border flex bg-blue-50 text-indigo-500">
    <div :class="{'navTabsSelected': openTab == 1, 'navTabs': openTab != 1}" @click="toggleTabs(1)">
      Артикулы Своб.склада
    </div>
    <div :class="{'navTabsSelected': openTab == 2, 'navTabs': openTab != 2}" @click="toggleTabs(2)">
      Приход товара
    </div>
    <div :class="{'navTabsSelected': openTab == 3, 'navTabs': openTab != 3}" @click="toggleTabs(3)">
      Движение товара
    </div>
  </nav>

  <div id="dashboardContent" class="">
    <div v-if="openTab == 1">
      <TabArticul
        :articulBarTnvedDatax="articulBarTnvedDatax" 
        :articulBarTnvedDatay="articulBarTnvedDatay" 
        :articulCardDtCnt="articulCardDtCnt" 
        :articulCardArticulCnt="articulCardArticulCnt"
        :articulListName="articulListName" 
        :articulListArticul="articulListArticul" 
        :articulListTableColumns="articulListTableColumns"
      />
    </div>
    <div v-if="openTab == 2">
      <TabArrival
        :arrivalBarTnvedDatax="arrivalBarTnvedDatax" 
        :arrivalBarTnvedDatay="arrivalBarTnvedDatay" 
        :arrivalCardGoodsCnt="arrivalCardGoodsCnt" 
        :arrivalCardDtCnt="arrivalCardDtCnt"
        :arrivalListName="arrivalListName" 
        :arrivalListGoodsArrival="arrivalListGoodsArrival" 
        :arrivalListTableColumns="arrivalListTableColumns"
      />
    </div>
    <div v-if="openTab == 3">
      <TabGoodsMovement 
        :goodsMovementListName="goodsMovementListName" 
        :goodsMovementListAccountBook="goodsMovementListAccountBook" 
        :goodsMovementListTableColumns="goodsMovementListTableColumns"
        />
    </div>
  </div>
  
</template>


<style lang="postcss" scoped>
.navTabs {
  @apply  rounded-t-lg px-5 py-2 cursor-pointer hover:text-indigo-600
}

.navTabsSelected {
    @apply bg-white  rounded-t-lg px-5 py-2 cursor-pointer hover:text-indigo-600
  }
</style>