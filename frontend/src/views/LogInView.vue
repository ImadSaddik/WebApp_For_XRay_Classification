<template>
  <section class="container-fluid d-flex flex-row p-0">
    <div class="w-50">
      <img
        src="../assets/background_1.png"
        class="img-fluid custom-image"
        alt="..."
        style="height: calc(100vh - 56px); object-fit: cover"
      />
    </div>
    <div class="row w-50 px-2 px-sm-5 pb-5 d-flex">
      <div class="col px-2 px-sm-5">
        <h1 class="display-5 fs-1 fw-bold text-dark mt-5 mb-4">Log In</h1>
        <div
          v-if="showAlertDialog"
          class="alert alert-warning alert-dismissible fade show rounded-3"
          role="alert"
        >
          <strong>Error! </strong> {{ errorMessage }}
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="alert"
            aria-label="Close"
            @click="showAlertDialog = false"
          ></button>
        </div>
        <form @submit.prevent="submitForm">
          <div class="input-group input-group-sm mb-3">
            <input
              type="text"
              class="form-control rounded-3 py-2 px-3"
              placeholder="Your username"
              v-model="username"
            />
          </div>
          <div class="input-group input-group-sm mb-3">
            <input
              class="form-control rounded-3 py-2 px-3"
              placeholder="Your password"
              v-model="password"
              :type="showHidePassword ? 'password' : 'text'"
            />
          </div>
          <div class="mb-3 form-check">
            <label
              class="form-check-label text-dark-emphasis"
              for="showHidePasswordCheckBox"
            >
              {{ showHidePassword ? "Show password" : "Hide password" }}
            </label>
            <input
              type="checkbox"
              class="form-check-input"
              id="showHidePasswordCheckBox"
              @click="showHidePassword = !showHidePassword"
            />
          </div>
          <p class="text-dark-emphasis">
            Forgot password? <a href="/reset_password">Click here</a>
          </p>
          <p class="text-dark-emphasis">
            Or <a href="/signup">Click here</a>, if you don't have an account.
          </p>
          <button type="submit" class="custom-button-dark mt-3">Log In</button>
        </form>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "LogInView",
  components: {},
  mounted() {
    document.title = "Log In";
  },
  data() {
    return {
      username: "",
      password: "",
      showHidePassword: true,
      showAlertDialog: false,
      errorMessage: "",
    };
  },
  methods: {
    async submitForm() {
      axios.defaults.headers.common.Authorization = "";
      localStorage.removeItem("token");

      const formData = {
        username: this.username,
        password: this.password,
      };

      await axios
        .post("/api/v1/token/login", formData)
        .then((response) => {
          const token = response.data.auth_token;
          axios.defaults.headers.common.Authorization = "Token " + token;

          localStorage.setItem("token", token);
          this.$store.dispatch("login", token);

          localStorage.setItem("username", this.username);
          this.$store.commit("setUsername", this.username);

          localStorage.setItem("selectedNavbarItem", "home");
          this.$store.commit("setSelectedNavbarItem", "home");

          this.$router.push({ name: "home", replace: true });
          console.log("successfully logged in");
        })
        .catch((error) => {
          console.log(error);
          this.showAlertDialog = true;
          this.errorMessage = "Invalid username or password.";
        });
    },
  },
};
</script>
