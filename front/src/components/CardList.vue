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
          :name="item.name"
          :date="item.date"
          :info="item.info"
          :grade="item.grade"
          :subjects="item.subjects"
          :onClickFavorite="() => onClickFavorite(item)"
          :is-favorite="item.isFavorite"
          :key="item.id"/>
  </div>
</template>

<style scoped>

</style>