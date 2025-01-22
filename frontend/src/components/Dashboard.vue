<script setup>
import { ref, defineProps, computed, reactive } from 'vue';
import TabForeignGoods from '@/components/TabForeignGoods.vue';
import TabEaesGoods from '@/components/TabEaesGoods.vue';
import TabProductedGoods from '@/components/TabProductedGoods.vue';
import TabIspolProductedGoods from '@/components/TabIspolProductedGoods.vue';
import TabMulti from '@/components/TabMulti.vue';

  
const props = defineProps({
  tabNumberVar: 5,

  filterProcGoodsDateFrom: String,
  filterProcGoodsDateTo: String,

  foreignGoodsListName: String,
  foreignGoodsList: Array,
  foreignGoodsListTableColumns: Object,

  eaesGoodsListName: String,
  eaesGoodsList: Array,
  eaesGoodsListTableColumns: Object,

  productedGoodsListName: String,
  productedGoodsList: Array,
  productedGoodsListTableColumns: Object,

  ispolProductedGoodsListName: String,
  ispolProductedGoodsList: Array,
  ispolProductedGoodsListTableColumns: Object,
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
    <!-- <div :class="{'navTabsSelected': openTab == 1, 'navTabs': openTab != 1}" @click="toggleTabs(1)">
      Иностранные товары
    </div>
    <div :class="{'navTabsSelected': openTab == 2, 'navTabs': openTab != 2}" @click="toggleTabs(2)">
      Товары ЕАЭС
    </div>
    <div :class="{'navTabsSelected': openTab == 3, 'navTabs': openTab != 3}" @click="toggleTabs(3)">
      Изг.товары, сырье
    </div>
    <div :class="{'navTabsSelected': openTab == 4, 'navTabs': openTab != 4}" @click="toggleTabs(4)">
      Испол.изг.товаров
    </div> -->
    <div :class="{'navTabsSelected': openTab == 5, 'navTabs': openTab != 5}" @click="toggleTabs(5)">
      Товары под процедурой
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
    <div v-if="openTab == 3">
      <TabProductedGoods
        :productedGoodsListName="productedGoodsListName" 
        :productedGoodsList="productedGoodsList" 
        :productedGoodsListTableColumns="productedGoodsListTableColumns"
      />
    </div>
    <div v-if="openTab == 4">
      <TabIspolProductedGoods
        :ispolProductedGoodsListName="ispolProductedGoodsListName" 
        :ispolProductedGoodsList="ispolProductedGoodsList" 
        :ispolProductedGoodsListTableColumns="ispolProductedGoodsListTableColumns"
      />
    </div>
    <div v-if="openTab == 5">
      <TabMulti
        :multiListName="'multiListName'" 
        :filterProcGoodsDateFrom="filterProcGoodsDateFrom"
        :filterProcGoodsDateTo="filterProcGoodsDateTo"
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