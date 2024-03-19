<template>
  <section class="container">
    <div class="px-5 my-5">
      <h1 class="fs-1 fw-bold text-dark">Classify your image</h1>
      <p v-if="!isLoggedOff" class="mt-3 text-dark-emphasis">
        To get started, upload an image and click the predict button. The
        uploaded image will be saved in the database and can be accessed later,
        down below.
      </p>

			<p v-else class="mt-3 text-dark-emphasis">
				To get started, please <router-link to="/login">log in</router-link> or <router-link to="/signup">sign up</router-link>.
			</p>

      <div v-if="!isLoggedOff" class="row mt-5 d-flex flex-column align-items-center">
        <div
          v-if="!imageUploaded"
          class="col-4 border border-3 rounded-4 d-flex align-items-center justify-content-center"
          style="height: 60vh"
        >
          <i class="fa-solid fa-file-image fa-2xl text-dark-emphasis"></i>
        </div>

        <div v-else class="col-4 p-0" style="height: 60vh">
          <img
            :src="selectedFileURL"
            class="img-fluid border border-3 rounded-4"
            alt="Selected image"
            style="width: 100%; height: 100%; object-fit: cover"
          />
        </div>

        <div class="col-4 mt-3">
          <div class="row">
            <div class="col ps-0">
              <input
                type="file"
                ref="fileInput"
                @change="handleFileUpload"
                style="display: none"
              />
              <button
                class="custom-button-dark"
                @click="triggerFileUpload"
                style="width: 100%"
              >
                Upload
              </button>
            </div>
            <div class="col pe-0">
              <button class="custom-button-dark" style="width: 100%">
                Predict
              </button>
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
  name: "ActivateAccountView",
	computed: {
    isLoggedOff() {
      return this.$store.state.token === "";
    },
  },
  data() {
    return {
      selectedFile: null,
      selectedFileURL: null,
      imageUploaded: false,
    };
  },
  methods: {
    triggerFileUpload() {
      this.$refs.fileInput.click();
    },
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
      this.selectedFileURL = URL.createObjectURL(this.selectedFile);
      this.imageUploaded = true;

      console.log(this.selectedFile);
      console.log(this.selectedFileURL);
    },
    async activateAccount() {
      const data = JSON.stringify({});

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
    document.title = "Predict";
  },
};
</script>
