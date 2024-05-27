<script setup>
  defineProps ({
    onChangeSearchInput: Function,
  })
</script>

<template>
  <header class="bg-white flex justify-between shadow-md px-6 py-3 z-30 fixed top-0 w-full">
    <router-link to="/">
      <div class="flex items-center ml-12 mr-2">
        <img src="/logo.svg" alt="Logo" />
        <div>
          <a class="logo">Olympozavr</a>
        </div>
      </div>
    </router-link>

    <div class="search rounded flex justify-between items-center p-1.5">

      <input @input="onChangeSearchInput" class="search-field rounded p-1.5" placeholder="Введите название олимпиады...">
      <label class="search-button flex items-center gap-1"><img src="/search.svg" alt="Search"/>Поиск</label>

    </div>

    <ul class="flex items-center gap-14" >
      <router-link to="/favorites">
        <li class="flex items-center gap-1">
          <img src="/favorite.svg" alt="Favorite" />
          <a href="https://htmlbook.ru/html/BUTTON" >Избранное</a>
        </li>
      </router-link>
      <router-link to="/user">
        <li class="flex items-center gap-1 pr-9">
          <img src="/profile.svg" alt="Profile" />
          <a href="https://htmlbook.ru/html/BUTTON" >Войти</a>
        </li>
      </router-link>
    </ul>

  </header>
</template>

<style>
  .logo {
    font-family: "Comfortaa", serif;
    font-size: 30px;
  }

  .search {
    width: 1100px;
    height: 50px;
    border: 1px solid black;
  }

  .search-field {
    width: 947px;
    height: 36px;
    border: 1px solid #CDCDCD;
    background-color: #F5F5F5;
    color: #909090;
  }

  .search-button {
    margin: auto 22px auto 27px;
  }
</style>