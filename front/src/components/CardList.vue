<script setup>
import Card from '@/components/Card.vue'

defineProps({
  items: Array,
  onClickFavorite: Function,
})

</script>

<template>
  <div class="mt-12 w-full bg-white m-auto shadow-md">
    <Card v-for="item in items"
          :id="item.id"
          :title="item.title"
          :date="item.datestr"
          :description="item.description"
          :classes="item.classes"
          :subjects="item.subjects.split(', ')"
          :onClickFavorite="() => onClickFavorite(item)"
          :is-favorite="item.isFavorite"
          :key="item.id"
    />
  </div>
</template>

<style scoped>

</style>