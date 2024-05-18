<script setup>
</script>

<template>
  <header class="bg-white flex justify-between shadow-sm px-6 py-3">
    <div class="flex items-center ml-12 mr-2">
      <img src="/logo.svg" alt="Logo"/>
      <div>
        <a class="logo">Olympozavr</a>
      </div>
    </div>

    <div class="search rounded flex justify-between items-center p-1.5">

      <input class="search-field rounded p-1.5" value="Введите название олимпиады...">
      <button class="search-button flex items-center gap-1"><img src="/search.svg" alt="Search"/>Поиск</button>

    </div>

    <ul class="flex items-center gap-14" >
      <li class="flex items-center gap-1">
        <img src="/favorite.svg" alt="Favorite" />
        <a href="https://htmlbook.ru/html/BUTTON" >Избранное</a>
      </li>
      <li class="flex items-center gap-1 pr-9">
        <img src="/profile.svg" alt="Profile" />
        <a href="https://htmlbook.ru/html/BUTTON" >Войти</a>
      </li>
    </ul>

  </header>

  <div class="main bg-white w-3/5 m-auto h-screen mt-20 shadow-md">

  </div>

</template>

<style scoped>
  @import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@300..700&display=swap');
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');

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
