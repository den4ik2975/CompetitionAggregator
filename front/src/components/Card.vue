<script setup>
  defineProps({
    id: Number,
    name: String,
    date: String,
    info: String,
    subjects: String,
    grade: String,
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

    <div>
      <div class="flex items-center gap-4 text-sm">
        <p class="font-bold">{{ subjects }}</p>
        <p>{{ grade }}</p>
      </div>

      <a class="text-2xl">{{ name }}</a>
      <p class="date text-2xl">{{ date }}</p>
      <p class="text-base mt-4">{{ info }}</p>
    </div>

  </div>
</template>

<style>
  .date {
    color: #A30000;
  }
</style>