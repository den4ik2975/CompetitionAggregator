<script setup>
  defineProps({
    id: Number,
    name: String,
    date: String,
    info: String,
    subjects: Array,
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

    <router-link :to="'/olympiad/'">
      <div>
        <div class="flex items-center gap-1.5 text-sm font-bold">
          <p v-for="subject in subjects" :key="subject" :class="subject">{{ subject }}</p>
          <p class="ml-1 text-gray-500">{{ grade }}</p>
        </div>

        <a class="text-2xl">{{ name }}</a>
        <p class="date text-2xl">{{ date }}</p>
        <p class="text-base mt-4">{{ info }}</p>
      </div>
    </router-link>

  </div>

</template>

<style scoped>
  .date {
    color: #A30000;
  }

  .История {
    background-color: #EAD5CA;
    color: #8E4F2D;
    font-weight: bold;
    padding: 4px 8px 4px 8px;
    border-radius: 4px;
  }
  .Физика {
    background-color: #E7C2C2;
    color: #9A4A4A;
    font-weight: bold;
    padding: 4px 8px 4px 8px;
    border-radius: 4px;
  }
  .Химия {
    background-color: #CBE1E0;
    color: #287975;
    font-weight: bold;
    padding: 4px 8px 4px 8px;
    border-radius: 4px;
  }
  .Биология {
    background-color: #CCDDC9;
    color: #3E6F36;
    font-weight: bold;
    padding: 4px 8px 4px 8px;
    border-radius: 4px;
  }
  .Математика {
    background-color: #C5D7E9;
    color: #33628D;
    font-weight: bold;
    padding: 4px 8px 4px 8px;
    border-radius: 4px;
  }
  .Обществознание {
    background-color: #D9D1E7;
    color: #5E4A81;
    font-weight: bold;
    padding: 4px 8px 4px 8px;
    border-radius: 4px;
  }
  .Языковедение {
    background-color: #EFDEEC;
    color: #AA629D;
    font-weight: bold;
    padding: 4px 8px 4px 8px;
    border-radius: 4px;
  }
  .Литература {
    background-color: #F0E2CC;
    color: #6e634a;
    font-weight: bold;
    padding: 4px 8px 4px 8px;
    border-radius: 4px;
  }
  .Информатика {
    background-color: #DED1ED;
    color: #724F9D;
    font-weight: bold;
    padding: 4px 8px 4px 8px;
    border-radius: 4px;
  }

</style>