<template>
  <section class="container">
    <div class="px-5 mt-5">
      <h1 class="fs-1 fw-bold text-dark">Account status</h1>
      <p v-if="activationStatus" class="text-dark-emphasis">
        Account activated successfully. You can now <router-link to="/login">log in</router-link>.
      </p>
      <p v-else-if="activationStatus === false" class="text-dark-emphasis">
        Account activation failed. Please try again.
      </p>
    </div>
  </section>
</template>

<script>
import axios from "axios";

export default {
  name: "ActivateAccountView",
  data() {
    return {
      activationStatus: null,
    };
  },
  methods: {
    async activateAccount() {
      const data = JSON.stringify({
        uid: this.$route.params.uid,
        token: this.$route.params.token,
      });

      await axios
        .post("/api/v1/users/activation/", data, {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "csrftoken",
          },
        })
        .then((response) => {
          this.activationStatus = true;
        })
        .catch((error) => {
          this.activationStatus = false;
          console.error(error);
        });
    },
  },
  created() {
    this.activateAccount();
  },
  mounted() {
    document.title = "Activate account";
  },
};
</script>
