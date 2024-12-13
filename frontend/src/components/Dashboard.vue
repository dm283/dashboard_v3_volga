<script setup>
import { ref, defineProps, computed, reactive } from 'vue';
import TabForeignGoods from '@/components/TabForeignGoods.vue';
import TabEaesGoods from '@/components/TabEaesGoods.vue';

  
const props = defineProps({
  tabNumberVar: 1,

  foreignGoodsListName: String,
  foreignGoodsList: Array,
  foreignGoodsListTableColumns: Object,

  eaesGoodsListName: String,
  eaesGoodsList: Array,
  eaesGoodsListTableColumns: Object,
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
      Иностранные товары
    </div>
    <div :class="{'navTabsSelected': openTab == 2, 'navTabs': openTab != 2}" @click="toggleTabs(2)">
      Товары ЕАЭС
    </div>
  </nav>

  <div id="dashboardContent" class="">
    <div v-if="openTab == 1">
      <TabForeignGoods
        :foreignGoodsListName="foreignGoodsListName" 
        :foreignGoodsList="foreignGoodsList" 
        :foreignGoodsListTableColumns="foreignGoodsListTableColumns"
      />
    </div>
    <div v-if="openTab == 2">
      <TabEaesGoods
        :eaesGoodsListName="eaesGoodsListName" 
        :eaesGoodsList="eaesGoodsList" 
        :eaesGoodsListTableColumns="eaesGoodsListTableColumns"
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