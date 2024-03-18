<template>
  <section class="container-fluid d-flex flex-row p-0">
    <div class="w-50">
      <img
        src="../assets/background_2.png"
        class="img-fluid custom-image"
        alt="..."
        style="height: calc(100vh - 56px); object-fit: cover"
      />
    </div>

    <div class="row w-50 px-2 px-sm-5 pb-5 d-flex">
      <div class="col px-2 px-sm-5">
        <h1 class="display-5 fs-1 fw-bold text-dark mt-5 mb-4">Sign Up</h1>
        <div
          v-if="showAlertDialog"
          class="alert alert-warning alert-dismissible fade show rounded-3"
          role="alert"
        >
          <div v-for="error in errors" :key="error">
            <strong>Error! </strong> {{ error }}
          </div>
          <button
            type="button"
            class="btn-close"
            data-bs-dismiss="alert"
            aria-label="Close"
            @click="showAlertDialog = false"
          ></button>
        </div>
        <form v-if="!hideForm" @submit.prevent="submitForm">
          <div class="input-group input-group-sm mb-3">
            <input
              type="text"
              class="form-control rounded-3 py-2 px-3"
              placeholder="Username"
              id="exampleInputUsername"
              v-model="username"
            />
          </div>
          <div class="input-group input-group-sm mb-3">
            <input
              class="form-control rounded-3 py-2 px-3"
              placeholder="Email"
              id="exampleInputEmail"
              v-model="email"
              type="email"
            />
          </div>
          <div class="input-group input-group-sm mb-3">
            <input
              class="form-control rounded-3 py-2 px-3"
              placeholder="Password"
              id="exampleInputPassword1"
              v-model="password"
              :type="showHidePassword ? 'password' : 'text'"
            />
          </div>
          <div class="input-group input-group-sm mb-3">
            <input
              class="form-control rounded-3 py-2 px-3"
              placeholder="Repeat password"
              id="exampleInputPassword2"
              v-model="repeatPassword"
              :type="showHidePassword ? 'password' : 'text'"
            />
          </div>
          <div class="mb-3 form-check">
            <label
              class="form-check-label text-dark-emphasis"
              for="showHidePasswordCheckBox"
              >{{ showHidePassword ? "Show password" : "Hide password" }}</label
            >
            <input
              type="checkbox"
              class="form-check-input"
              id="showHidePasswordCheckBox"
              @click="showHidePassword = !showHidePassword"
            />
          </div>
          <p class="text-dark-emphasis">
            Or <router-link to="/login">Click here</router-link>, if you already have an account.
          </p>
          <button type="submit" class="custom-button-dark mt-3">Create account</button>
        </form>

        <div v-if="hideForm">
          <p class="text-dark-emphasis">
            Account created successfully. Please check your email to verify your account.
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";

export default {
  name: "SignUpView",
  components: {},
  mounted() {
    document.title = "Sign Up";
  },
  data() {
    return {
      username: "",
      email: "",
      password: "",
      repeatPassword: "",
      showHidePassword: true,
      showAlertDialog: false,
      hideForm: false,
      errors: [],
    };
  },
  methods: {
    async submitForm() {
      if (this.errorExist()) {
        return;
      }

      const formData = {
        name: this.username,
        email: this.email,
        password: this.password,
        re_password: this.repeatPassword,
      };

      axios.defaults.headers.common.Authorization = "";
      await axios
        .post("/api/v1/users/", formData)
        .then((response) => {
          this.errors = [];
          this.showAlertDialog = false;
          this.hideForm = true;
          console.log("successfully signed up");
        })
        .catch((error) => {
          console.log(error);
          this.errors.push("Something went wrong. Please try again.");
          this.showAlertDialog = true;
        });
    },
    errorExist() {
      this.errors = [];

      if (this.username === "") {
        this.errors.push("The username field is required.");
      }

      if (this.email === "") {
        this.errors.push("The email fiels is required.")
      }

      if (this.password === "") {
        this.errors.push("The password field is required.");
      }

      if (this.repeatPassword === "") {
        this.errors.push("The repeat password field is required.");
      }

      if (this.password !== this.repeatPassword) {
        this.errors.push("The two password fields didn't match.");
      }

      if (this.errors.length) {
        this.showAlertDialog = true;
        return true;
      }
    },
  },
};
</script>
