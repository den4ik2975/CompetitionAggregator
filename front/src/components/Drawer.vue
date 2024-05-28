<script setup>
  defineProps ({
    closeDrawer: Function,
    onChangeFilter: Function,
    grades: Object,
    subjects: Object,
  })

</script>

<template>

  <div @click="closeDrawer" class="fixed z-50 top-0 h-full w-full bg-black opacity-70" />
  <div class="filter-main fixed h-full z-50 top-0 bg-white p-8">

    <button @click="closeDrawer" class="flex items-center gap-1 absolute right-8 top-8 text-gray-500">Закрыть
      <img src="/close.svg" alt="Close" />
    </button>

    <section>
      <h2 class="text-gray-500">Класс</h2>
      <ul class="grades-list my-7 text-base">
        <li v-for="grade in grades" :key="grade.id" class="flex items-center gap-1.5">
          <input type="checkbox" @change="onChangeFilter" :checked="grade.checked" id="grades" :value="grade.id">
          <label :for="grade">{{ grade.name }}</label>
        </li>
      </ul>
    </section>

    <section>
      <h2 class="text-gray-500">Предмет</h2>
      <ul class="subjects-list my-7 text-base">
        <li v-for="subject in subjects" :key="subject.id" class="flex items-center gap-1.5">
          <input type="checkbox" @change="onChangeFilter" :checked="subject.checked" id="subjects" :value="subject.name">
          <label :for="subject">{{ subject.name }}</label>
        </li>
      </ul>
    </section>

    <button class="close-button w-full mt-40 transition">Очистить</button>

    </div>

</template>

<style scoped>

.filter-main {
  width: 500px;
  right: 0;
}

.subjects-list {
  column-count: 2;
}

.grades-list {
  column-count: 2;
}

.close-button {
  border: 1px solid black;
  border-radius: 6px;
  padding: 5px;
}

.close-button:hover {
  background-color: #a8bdc5;
}

</style>