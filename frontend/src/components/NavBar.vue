<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary" style="height: 56px">
    <div class="container-fluid px-sm-5">
      <router-link
        class="navbar-brand"
        to="/"
        @click="handleNavbarItemClick(HOME_PAGE)"
      >
        <!-- <img src="../assets/logo.svg" alt="" /> -->
      </router-link>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNavAltMarkup"
        aria-controls="navbarNavAltMarkup"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="row w-100 navbar-nav">
          <div class="col d-lg-flex align-items-center">
            <router-link
              class="nav-link ms-5"
              :class="{ 'fw-bold': getSelectedNavbarItem === HOME_PAGE }"
              to="/"
              @click="handleNavbarItemClick(HOME_PAGE)"
            >
              Home
            </router-link>
            <router-link
              class="nav-link ms-3"
              :class="{ 'fw-bold': getSelectedNavbarItem === PREDICT_PAGE }"
              to="/predict"
              @click="handleNavbarItemClick(PREDICT_PAGE)"
            >
              Predict
            </router-link>
            <router-link
              class="nav-link ms-3"
              :class="{ 'fw-bold': getSelectedNavbarItem === GALLERY_PAGE }"
              to="/gallery"
              @click="handleNavbarItemClick(GALLERY_PAGE)"
            >
              Gallery
            </router-link>
            <router-link
              class="nav-link ms-3"
              :class="{ 'fw-bold': getSelectedNavbarItem === REPORT_PAGE }"
              to="/report"
              @click="handleNavbarItemClick(REPORT_PAGE)"
            >
              Report
            </router-link>
            <hr class="d-block d-lg-none" />
          </div>
          <div class="col-auto d-flex align-items-center">
            <div v-show="isLoggedOff">
              Log In
              <router-link
                to="/login"
                data-bs-toggle="tooltip"
                data-bs-placement="bottom"
                data-bs-title="Log in"
                @click="handleNavbarItemClick(NONE)"
              >
                <i
                  type="button"
                  class="ms-3 fa-solid fa-arrow-right-to-bracket fa-lg"
                  style="color: #000"
                ></i>
              </router-link>
            </div>
            <div v-show="!isLoggedOff">
              {{ getEmail }}
              <a
                data-bs-toggle="tooltip"
                data-bs-placement="bottom"
                data-bs-title="Log out"
              >
                <i
                  type="button"
                  class="ms-3 fa-solid fa-door-open fa-lg"
                  style="color: #a51d2d"
                  @click="logOut"
                ></i>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import axios from "axios";

export default {
  name: "NavBar",
  computed: {
    isLoggedOff() {
      return this.$store.state.token === "";
    },
    getEmail() {
      return this.$store.state.email;
    },
    getSelectedNavbarItem() {
      return this.$store.state.selectedNavbarItem;
    },
  },
  mounted () {
    this.handleNavbarItemClick(this.HOME_PAGE)
  },
  data() {
    return {
      HOME_PAGE: "home",
      PREDICT_PAGE: "predict",
      GALLERY_PAGE: "gallery",
      REPORT_PAGE: "report",
      NONE: "",
    };
  },
  methods: {
    logOut() {
      console.log("Logging out");
      this.$emit("logged-out");
      axios.defaults.headers.common.Authorization = "";

      localStorage.removeItem("token");
      localStorage.removeItem("email");

      this.$store.commit("removeToken");
      this.$store.commit("removeEmail");
    },
    handleNavbarItemClick(item) {
      localStorage.setItem("selectedNavbarItem", item);
    },
  },
};
</script>
