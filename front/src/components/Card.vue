<script setup>
  defineProps({
    title: String,
    date: String,
    description: String,
    subjects: Array,
    grades: String,
    isFavorite: Boolean,
    isParticipant: Boolean,
    isNotified: Boolean,
  })
</script>

<template>
  <div class="p-7 relative">

    <div class="flex items-center gap-1.5 right-0 absolute mr-7">
      <img src="/notify.svg" alt="Notify" class="cursor-pointer"/>
      <img src="/favorite.svg" alt="Favorite" class="cursor-pointer"/>
      <img src="/participant.svg" alt="Participant" class="cursor-pointer"/>
    </div>

    <div>
      <div class="flex items-center gap-4 text-sm">
        <p class="font-bold">История</p>
        <p>{{ grades }}</p>
      </div>

      <a class="text-2xl">{{ title }}</a>
      <p class="date text-2xl">{{ date }}</p>
      <p class="text-base mt-4">{{ description }}</p>
    </div>

  </div>
</template>

<style>
  .date {
    color: #A30000;
  }
</style>