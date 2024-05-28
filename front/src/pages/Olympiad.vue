<script setup>
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { URL } from '../utils/constants.js'

const props = defineProps ({
  id: String,
})

const items = ref([])

const getOlympiad = async () => {
  try {
    const { data } = await axios.get(URL + `/olympiad/${props.id}`)
    items.value = data

    items.value.subjects = items.value.subjects.split(', ')
  } catch (error) {
    console.log(error)
  }
}

onMounted(async() => {
  await getOlympiad();
})

</script>

<template>
  <div class="p-7 relative mt-12 w-full bg-white m-auto shadow-md">

    <div class="flex items-center gap-1.5 right-0 absolute mr-7">
      <img :src="items.is_notified ? '/isnotified.svg' : '/notify.svg'"
           @click=""
           alt="Notify"
           class="cursor-pointer"/>
      <img :src="items.is_participant ? '/isparticipant.svg' : '/participant.svg'"
           @click=""
           alt="Participant"
           class="cursor-pointer"/>
      <img :src="items.is_favorite ? '/isfavorite.svg' : '/favorite.svg'"
           @click="items.onClickFavorite"
           alt="Favorite"
           class="cursor-pointer"/>

    </div>

    <div class="grid grid-cols-2">
      <div>
        <div class="flex items-center gap-1.5 text-sm font-bold flex-wrap mb-6">
          <p v-for="subject in items.subjects" :key="subject" :class="subject">{{ subject }}</p>
          <p class="ml-1 text-gray-500">{{ items.classes }}</p>
        </div>

        <p class="text-2xl">{{ items.title }}</p>
        <p class="date text-2xl">{{ items.date }}</p>

        <h2 class="text-2xl mt-4">| Расписание</h2>
        <ul class="mt-4">
          <li class="grid grid-cols-2 gap-2 my-4 place-content-between" v-for="date in items.dates" :key="date.name">
            <p>{{ date.name }}</p>
            <p class="date">{{ date.date_start }} {{ date.date_end }}</p>
          </li>
        </ul>

      </div>

      <div class="content-center ml-10">
        <p class="max-w-96 text-gray-500" >{{ items.description }}</p>
      </div>
    </div>

  </div>
</template>

<style scoped>

</style>