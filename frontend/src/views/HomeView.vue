<template>
  <section class="container-fluid p-0" style="background-color: black">
    <div class="position-relative d-flex flex-column">
      <img
        src="../assets/background_1.png"
        class="img-fluid custom-image"
        alt="..."
        style="
          width: 100%;
          height: calc(100vh - 56px);
          object-fit: cover;
          opacity: 0.2;
        "
      />

      <div class="container position-absolute top-50 start-50 translate-middle">
        <div class="row">
          <div class="col">
            <div>
              <h1 class="text-center fs-1 fs-sm-1 fw-bold text-white mb-2">
                Utilize AI for patient health diagnosis
              </h1>
              <p class="text-center fs-4 fw-light text-white">
                It's easy, simple, effective, and reliable
              </p>
              <div class="text-center mt-5">
                <button type="button" class="custom-button-light">Start now</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";

export default {
  name: "HomeView",
  components: {},
  computed: {
    isUserLoggedOff() {
      return this.$store.state.token === "";
    },
  },
  data() {
    return {};
  },
  created() {
    this.$store.commit("setSelectedNavbarItem", "home");
  },
  mounted() {
    document.title = "Home";
  },
  methods: {},
};
</script>
