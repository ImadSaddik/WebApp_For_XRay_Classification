<template>
  <section class="container">
    <div class="px-5 my-5">
      <h1 class="fs-1 fw-bold text-dark">Gallery</h1>
      <p v-if="isLoggedOff" class="mt-3 text-dark-emphasis">
        To look at the images you uploaded, please <router-link to="/login">log in</router-link> or
        <router-link to="/signup">sign up</router-link>.
      </p>
    </div>
  </section>
</template>

<script>
import axios from "axios";

export default {
  name: "GalleryView",
  computed: {
    isLoggedOff() {
      return this.$store.state.token === "";
    },
  },
  data() {
    return {};
  },
  methods: {},
  created() {
    this.$store.commit("setSelectedNavbarItem", "gallery");
  },
  mounted() {
    document.title = "Gallery";
  },
};
</script>
