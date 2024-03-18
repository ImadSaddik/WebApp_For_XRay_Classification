<template>
  <section class="container">
    <div class="row px-5 mt-5">
      <h1 class="fs-1 fw-bold text-dark mb-3">Password reset</h1>

      <div
        v-if="resetLinkSent"
        class="alert alert-success alert-dismissible fade show"
        role="alert"
      >
        Check your email for a link to reset your password.
        <button
          @click="resetLinkSent = false"
          type="button"
          class="btn-close"
          data-bs-dismiss="alert"
          aria-label="Close"
        ></button>
      </div>

      <div
        v-if="errorOccurred"
        class="alert alert-success alert-dismissible fade show"
        role="alert"
      >
        {{ errorMessage }}
        <button
          @click="errorOccurred = false"
          type="button"
          class="btn-close"
          data-bs-dismiss="alert"
          aria-label="Close"
        ></button>
      </div>

      <p class="text-dark-emphasis">
        Provide your email address for us to send you a link enabling password
        reset.
      </p>

      <div class="row input-group input-group-sm">
        <label for="email" class="mb-2 fw-bold">Email Address</label>
        <div class="col-6">
          <input
            id="email"
            type="email"
            class="form-control rounded-3 py-2 px-3"
            placeholder="Your email"
            v-model="email"
          />
          <button @click="resetPassword" class="custom-button-dark mt-3">
            Reset password
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";

export default {
  name: "ResetPassword",
  data() {
    return {
      email: "",
      resetLinkSent: false,
      errorOccurred: false,
      errorMessage: "",
    };
  },
  methods: {
    async resetPassword() {
      const data = JSON.stringify({
        email: this.email,
      });

      await axios
        .post("/api/v1/users/reset_password/", data, {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "csrftoken",
          },
        })
        .then((response) => {
          this.resetLinkSent = true;
        })
        .catch((error) => {
          this.errorOccurred = true;
          this.errorMessage = error.response.data.detail;
        });
    },
  },
  mounted() {
    document.title = "Reset password";
  },
};
</script>
