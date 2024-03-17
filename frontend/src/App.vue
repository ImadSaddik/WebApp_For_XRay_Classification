<template>
  <NavBar />
  <router-view />
</template>

<script>
import NavBar from "@/components/NavBar.vue";

export default {
  name: "App",
  components: {
    NavBar,
  },
};
</script>

<style>
.custom-button-light {
  background-color: white;
  width: 200px;
  color: black;
  border-radius: 100px;
  border: none;
  padding: 10px 20px;
  transition: background-color 0.3s ease;
}

.custom-button-light:hover {
  background-color: #9c9c9c;
}

.custom-button-dark {
  background-color: black;
  width: 200px;
  color: white;
  border-radius: 100px;
  border: none;
  padding: 10px 20px;
  transition: background-color 0.3s ease;
}

.custom-button-dark:hover {
  background-color: #000000a0;
}
</style>
