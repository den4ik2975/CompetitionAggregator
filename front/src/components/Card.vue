<script setup>

  defineProps({
    id: Number,
    title: String,
    date: String,
    description: String,
    subjects: Array,
    classes: String,
    isFavorite: Boolean,
    isParticipant: Boolean,
    isNotified: Boolean,
    onClickFavorite: Function,
  })

</script>

<template>

  <div class="p-7 relative">

    <div class="flex items-center gap-1.5 right-0 absolute mr-7">
      <img :src="isNotified ? '/isnotified.svg' : '/notify.svg'"
           @click=""
           alt="Notify"
           class="cursor-pointer"/>
      <img :src="isParticipant ? '/isparticipant.svg' : '/participant.svg'"
           @click=""
           alt="Participant"
           class="cursor-pointer"/>
      <img :src="isFavorite ? '/isfavorite.svg' : '/favorite.svg'"
           @click="onClickFavorite"
           alt="Favorite"
           class="cursor-pointer"/>

    </div>

    <router-link :to="{name: 'Olympiad', params: {id: id}}">
      <div>
        <div class="flex items-center gap-1.5 text-sm font-bold">
          <p v-for="subject in subjects" :key="subject" :class="subject">{{ subject }}</p>
          <p class="ml-1 text-gray-500">{{ classes }}</p>
        </div>

        <a class="text-2xl">{{ title }}</a>
        <p class="date text-2xl">{{ date }}</p>
        <p class="text-base mt-4">{{ description }}</p>
      </div>
    </router-link>

  </div>

</template>

<style scoped>

</style>