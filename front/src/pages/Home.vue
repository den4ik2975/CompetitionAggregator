<script setup>

  import CardList from '../components/CardList.vue'
  import { inject } from 'vue'

  const onClickFavorite = inject('onClickFavorite')
  const items = inject('items')
  const onChangeSelect = inject('onChangeSelect')
  const openDrawer = inject('openDrawer')

</script>

<template>
  <label class="left-0 absolute mt-1.5">| Все олимпиады</label>
  <div class=" flex items-center gap-4 right-0 absolute">
    <button @click="openDrawer">Фильтры</button>

    <select @change="onChangeSelect" class="rounded-md p-1">
      <option value="">По умолчанию</option>
      <option value="name">По названию</option>
      <option value="date">По дате</option>
    </select>
  </div>

  <CardList :items="items" :on-click-favorite="onClickFavorite" />

</template>
