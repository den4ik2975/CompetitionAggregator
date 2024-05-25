<script setup>
  import { onMounted, ref, reactive, watch } from 'vue'
  import axios from 'axios'

  import Drawer from './components/Drawer.vue'
  import CardList from '@/components/CardList.vue'
  import Header from '@/components/Header.vue'

  const items = ref([]);

  const filters = reactive({
    sortBy: '',
    searchQuery: '',
  });

  const onChangeSelect = (event) => {
    filters.sortBy = event.target.value;
  };

  const onChangeSearchInput = (event) => {
    filters.searchQuery = event.target.value;
  };

  const fetchFavorites = async () => {
    try {
      const { data: favorites } = await axios.get(`https://77cfb0c9bf907cd8.mokky.dev/favorites`)
      items.value = items.value.map(item => {
        const favorite = favorites.find(favorite => favorite.parentId === item.id);

        if (!favorite) {
          return item;
        }
        return {
          ...item,
          isFavorite: true,
          favoriteId: favorite.id,
        }
      });

    } catch (error) {
      console.log(error)
    }
  };

  const fetchItems = async () => {
    try {
      const params = {
        sortBy: filters.sortBy,

      };
      if (filters.searchQuery) {
        params.name = `*${filters.searchQuery}*`;
      }
      const { data } = await axios.get(
        `https://77cfb0c9bf907cd8.mokky.dev/olympiad`, {
          params
        })

      items.value = data.map((obj) => ({
        ...obj,
        isFavorite: false,
        favoriteID: null,
        isParticipant: false,
        isNotified: false,
      }))
    } catch (error) {
      console.log(error)
    }
  }

  const onClickFavorite = async (item) => {
    try {
      if (!item.isFavorite) {
        const obj = {
          parentId: item.id,
        };
        item.isFavorite = true;
        const { data } = await axios.post(`https://77cfb0c9bf907cd8.mokky.dev/favorites`, obj);
        item.favoriteId = data.id;
      } else {
        item.isFavorite = false;
        await axios.delete(`https://77cfb0c9bf907cd8.mokky.dev/favorites/${item.favoriteId}`);
        item.favoriteId = null;
      }

    } catch (error) {
      console.log(error)
    }
  }

  onMounted(async() => {
    await fetchItems();
    await fetchFavorites();
  })
  watch(filters, fetchItems)

</script>

<template>
  <Header :onChangeSearchInput="onChangeSearchInput"/>

  <div class="main w-3/5 m-auto pt-2 relative">

    <div class=" flex items-center gap-4 right-0 absolute">
      <button class="">Фильтры</button>

      <select @change="onChangeSelect" class="rounded-md p-1">
        <option value="">По умолчанию</option>
        <option value="name">По названию</option>
        <option value="date">По дате</option>
      </select>
    </div>

    <CardList :items="items" :on-click-favorite="onClickFavorite"/>

  </div>

</template>

<style>

  @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@300..700&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

</style>
