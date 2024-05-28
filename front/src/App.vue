<script setup>
import { onMounted, ref, reactive, watch, provide } from 'vue'
  import axios from 'axios'

  import Header from './components/Header.vue'
  import Drawer from './components/Drawer.vue'

  import { URL } from './utils/constants.js'
  import Auth from '@/components/Auth.vue'
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
    if (filters.filterBy.includes(`${event.target.id}=${event.target.value}&`)) {
      filters.filterBy = filters.filterBy.replace(`${event.target.id}=${event.target.value}&`, '')
    } else {
      filters.filterBy += `${event.target.id}=${event.target.value}&`;
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
      "id": '1',
      "name": "1 класс",
      "checked": false,
    },
    {
      "id": '2',
      "name": "2 класс",
      "checked": false,
    },
    {
      "id": '3',
      "name": "3 класс",
      "checked": false,
    },
    {
      "id": '4',
      "name": "4 класс",
      "checked": false,
    },
    {
      "id": '5',
      "name": "5 класс",
      "checked": false,
    },
    {
      "id": '6',
      "name": "6 класс",
      "checked": false,
    },
    {
      "id": '7',
      "name": "7 класс",
      "checked": false,
    },
    {
      "id": '8',
      "name": "8 класс",
      "checked": false,
    },
    {
      "id": '9',
      "name": "9 класс",
      "checked": false,
    },
    {
      "id": '10',
      "name": "10 класс",
      "checked": false,
    },
    {
      "id": '11',
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
        const { data } = await axios.post(URL + `/favorites`, obj);
        item.favoriteId = data.id;
      } else {
        item.isFavorite = false;
        await axios.delete(URL + `/favorites/${item.favoriteId}`);
        item.favoriteId = null;
      }

    } catch (error) {
      console.log(error)
    }
  }

  const fetchFavorites = async () => {
    try {
      const { data: favorites } = await axios.get(URL + `/`)
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

      console.log(URL + `/?sortBy=${filters.sortBy}&search=${filters.searchQuery}&${filters.filterBy}`)

      const { data } = await axios.get(
        URL + `?sortBy=${filters.sortBy}&search=${filters.searchQuery}&${filters.filterBy}`)

      // CHECKED FILTER
      for (const element of filters.filterBy.split('&')) {
        if (element.split('=')[1]) {
          checkedIds.push(element.split('=')[1])
        }
      }
      for (const subject of subjects) { if (checkedIds.includes(subject.name)) { subject.checked = true }}
      for (const grade of grades) { if (checkedIds.includes(grade.id)) { grade.checked = true }}

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
  provide('url', URL)

</script>

<template>
  <Drawer v-if="drawerOpen" :close-drawer="closeDrawer" :on-change-filter="onChangeFilter" :grades="grades" :subjects="subjects"/>
  <Header :onChangeSearchInput="onChangeSearchInput"/>

  <div class="main w-3/5 m-auto pt-2 relative">
    <Auth/>

    <router-view></router-view>

  </div>

  <div ref="sentinel"></div>

</template>

<style>

  @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@300..700&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

</style>
