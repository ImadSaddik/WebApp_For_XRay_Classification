<template>
  <section class="container">
    <div class="px-5 my-5">
      <div v-if="showPopup" class="alert alert-success alert-dismissible fade show popup" role="alert">
        <strong>Success!</strong> The image is now used in the prediction.
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="alert"
          aria-label="Close"
          @click="showPopup = false"
        ></button>
      </div>

      <h1 class="fs-1 fw-bold text-dark">Classify your image</h1>
      <p v-if="!isLoggedOff" class="mt-3 text-dark-emphasis">
        To get started, upload an image and click the predict button. The
        uploaded image will be saved in the database and can be accessed later,
        down below.
      </p>

      <p v-else class="mt-3 text-dark-emphasis">
        To get started, please <router-link to="/login">log in</router-link> or
        <router-link to="/signup">sign up</router-link>.
      </p>

      <div
        v-if="!isLoggedOff"
        class="row mt-5 d-flex flex-column align-items-center"
      >
        <div
          v-if="!imageUploaded"
          class="col-4 p-0 border border-3 rounded-4 position-relative d-flex flex-column"
        >
          <div>
            <img
              src="../assets/white_background.jpeg"
              class="img-fluid rounded-4"
              alt="Uploaded image"
              style="width: 100%; height: 100%; object-fit: cover"
            />
          </div>
          <div class="position-absolute top-50 start-50 translate-middle">
            <i class="fa-solid fa-file-image fa-2xl text-dark-emphasis"></i>
          </div>
        </div>

        <div v-else class="col-4 mb-4">
          <img
            :src="uploadedImage"
            class="img-fluid border border-3 rounded-4"
            alt="Uploaded image"
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
              <button
                class="custom-button-dark"
                style="width: 100%"
                @click="predictImage"
              >
                Predict
              </button>
            </div>
          </div>
        </div>

        <div class="col mt-5">
          <div
            v-if="predicted_class"
            class="alert alert-secondary alert-dismissible fade show"
            role="alert"
          >
            <h4 class="alert-heading">Prediction</h4>
            <p>
              The predicted class for the uploaded image is
              <strong>{{ predicted_class }}</strong
              >.
            </p>

            <router-link to="/report">
              <button class="custom-button-dark">Show report</button>
            </router-link>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="alert"
              aria-label="Close"
              @click="predicted_class = null"
            ></button>
          </div>
        </div>
      </div>

      <div v-if="numberOfUploadedImagesByUser > 0 && !isLoggedOff">
        <h1 class="mt-3 fs-1 fw-bold text-dark">Uploaded images</h1>
        <p class="mt-2 mb-0 text-dark-emphasis">
          You can use one of the images you uploaded earlier for prediction.
          Just click on the image to select it and then click the predict
          button.
        </p>

        <div class="row mt-5">
          <div
            v-for="image in uploadedImagesByUser"
            :key="image.image_id"
            class="col-4 mb-4"
          >
            <img
              @click="getSelectedImage(image.getImage)"
              :src="image.getImage"
              class="img-fluid border border-3 rounded-4"
              alt="Patient image"
              style="
                width: 100%;
                height: 100%;
                object-fit: cover;
                cursor: pointer;
              "
            />
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
      uploadedImage: null,
      imageUploaded: false,
      numberOfUploadedImagesByUser: 0,
      uploadedImagesByUser: [],
      predicted_class: null,
      image_id: null,
      showPopup: false,
    };
  },
  methods: {
    triggerFileUpload() {
      this.$refs.fileInput.click();
    },
    handleFileUpload(event) {
      const file = event.target.files[0];

      if (file) {
        const reader = new FileReader();
        reader.readAsDataURL(file);

        reader.onload = (event) => {
          this.uploadedImage = event.target.result;
          this.imageUploaded = true;

          this.saveImageToDatabase();
        };
      }
    },
    async saveImageToDatabase() {
      const formData = new FormData();
      formData.append("image", this.dataURItoBlob(this.uploadedImage));
      formData.append("email", this.$store.state.email);

      await axios
        .post("api/v1/addImage/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            "X-CSRFToken": "csrftoken",
          },
        })
        .then((response) => {
          this.image_id = response.data.image_id;
          console.log(response.data);

          this.getNumberOfUploadedImages();
          this.getUploadedImages();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    dataURItoBlob(dataURI) {
      const byteString = atob(dataURI.split(",")[1]);
      const mimeString = dataURI.split(",")[0].split(":")[1].split(";")[0];
      const arrayBuffer = new ArrayBuffer(byteString.length);
      const uint8Array = new Uint8Array(arrayBuffer);

      for (let i = 0; i < byteString.length; i++) {
        uint8Array[i] = byteString.charCodeAt(i);
      }
      return new Blob([arrayBuffer], { type: mimeString });
    },
    async getNumberOfUploadedImages() {
      const data = JSON.stringify({
        email: this.$store.state.email,
      });

      await axios
        .post("api/v1/getImageCountForUser/", data, {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "csrftoken",
          },
        })
        .then((response) => {
          this.numberOfUploadedImagesByUser = response.data.imageCount;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async getUploadedImages() {
      const data = JSON.stringify({
        email: this.$store.state.email,
      });

      await axios
        .post("api/v1/getImagesForUser/", data, {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "csrftoken",
          },
        })
        .then((response) => {
          console.log(response.data);
          this.uploadedImagesByUser = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async getSelectedImage(imageUrl) {
      const data = JSON.stringify({
        imageUrl: imageUrl,
      });

      await axios
        .post("api/v1/getImageFromUrl/", data, {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "csrftoken",
          },
        })
        .then((response) => {
          this.uploadedImage = response.data.image;
          this.imageUploaded = true;

          this.showPopup = true;
          setTimeout(() => {
            this.showPopup = false;
          }, 3000);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async predictImage() {
      const formData = new FormData();
      formData.append("image", this.dataURItoBlob(this.uploadedImage));

      await axios
        .post("api/v1/inference/", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            "X-CSRFToken": "csrftoken",
          },
        })
        .then((response) => {
          this.predicted_class = response.data.prediction;
          this.setPredictedClass();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    async setPredictedClass() {
      const data = JSON.stringify({
        image_id: this.image_id,
        predicted_class: this.predicted_class,
      });

      await axios
        .post("api/v1/setPredictedClass/", data, {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "csrftoken",
          },
        })
        .then((response) => {
          console.log(response.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  created() {
    this.$store.commit("setSelectedNavbarItem", "predict");
  },
  mounted() {
    document.title = "Predict";

    this.getNumberOfUploadedImages();
    this.getUploadedImages();
  },
};
</script>

<style scoped>
.popup {
  position: fixed;
  margin-left: 25%;
  bottom: 0;
  left: 0;
  width: 50%;
  z-index: 1000;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
