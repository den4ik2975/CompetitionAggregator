<script setup>
import { onMounted, ref, reactive, watch, provide } from 'vue'
  import axios from 'axios'

  import Header from './components/Header.vue'
  import Drawer from './components/Drawer.vue'

  const url = 'https://77cfb0c9bf907cd8.mokky.dev'

  const items = ref([])

  const drawerOpen = ref(false)

  const openDrawer = () => {
    drawerOpen.value = true
  }

  const closeDrawer = () => {
    drawerOpen.value = false
  }

  const filters = reactive({
    sortBy: '',
    searchQuery: '',
    filterBy: '',
  });

  const onChangeSelect = (event) => {
    filters.sortBy = event.target.value;
  }

  const onChangeSearchInput = (event) => {
    filters.searchQuery = event.target.value;
  }

  const onChangeFilter = (event) => {
    if (filters.filterBy.includes(`${event.target.id}[]=${event.target.value}&`)) {
      filters.filterBy = filters.filterBy.replace(`${event.target.id}[]=${event.target.value}&`, '')
    } else {
      filters.filterBy += `${event.target.id}[]=${event.target.value}&`;
    }
  }

  const subjects = [
    {
      "name": "Физика",
      "checked": false,
    },
    {
      "name": "Математика",
      "checked": false,
    },
    {
      "name": "Химия",
      "checked": false,
    },
    {
      "name": "Биология",
      "checked": false,
    },
    {
      "name": "История",
      "checked": false,
    },
    {
      "name": "Литература",
      "checked": false,
    },
    {
      "name": "Русский язык",
      "checked": false,
    },
    {
      "name": "Обществознание",
      "checked": false,
    },
    {
      "name": "Языковедение",
      "checked": false,
    },

  ]

  const grades = [
    {
      "name": "1 класс",
      "checked": false,
    },
    {
      "name": "2 класс",
      "checked": false,
    },
    {
      "name": "3 класс",
      "checked": false,
    },
    {
      "name": "4 класс",
      "checked": false,
    },
    {
      "name": "5 класс",
      "checked": false,
    },
    {
      "name": "6 класс",
      "checked": false,
    },
    {
      "name": "7 класс",
      "checked": false,
    },
    {
      "name": "8 класс",
      "checked": false,
    },
    {
      "name": "9 класс",
      "checked": false,
    },
    {
      "name": "10 класс",
      "checked": false,
    },
    {
      "name": "11 класс",
      "checked": false,
    },
  ]

  const onClickFavorite = async (item) => {
    try {
      if (!item.isFavorite) {
        const obj = {
          parentId: item.id,
        };
        item.isFavorite = true;
        const { data } = await axios.post(url + `/favorites`, obj);
        item.favoriteId = data.id;
      } else {
        item.isFavorite = false;
        await axios.delete(url + `/favorites/${item.favoriteId}`);
        item.favoriteId = null;
      }

    } catch (error) {
      console.log(error)
    }
  }

  const fetchFavorites = async () => {
    try {
      const { data: favorites } = await axios.get(url + `/favorites`)
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
      const checkedIds = []
      for (const subject of subjects) { subject.checked = false }
      for (const grade of grades) { grade.checked = false }

      const { data } = await axios.get(
        url + `/olympiad?sortBy=${filters.sortBy}&name=*${filters.searchQuery}*&${filters.filterBy}`)

      for (const element of filters.filterBy.split('&')) {
        if (element.split('=')[1]) {
          checkedIds.push(element.split('=')[1])
        }
      }

      for (const subject of subjects) { if (checkedIds.includes(subject.name)) { subject.checked = true }}
      for (const grade of grades) { if (checkedIds.includes(grade.name)) { grade.checked = true }}

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

  onMounted(async() => {
    await fetchItems();
    await fetchFavorites();
  })

  watch(filters, fetchItems)

  provide('onClickFavorite', onClickFavorite)
  provide('items', items)
  provide('onChangeSelect', onChangeSelect)
  provide('openDrawer', openDrawer)
  provide('url', url)

</script>

<template>
  <Drawer v-if="drawerOpen" :close-drawer="closeDrawer" :on-change-filter="onChangeFilter" :grades="grades" :subjects="subjects"/>
  <Header :onChangeSearchInput="onChangeSearchInput"/>

  <div class="main w-3/5 m-auto pt-2 relative">

    <router-view></router-view>

  </div>

</template>

<style>

  @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@300..700&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

</style>
