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
        To get started, please <router-link to="/login">log in</router-link> or
        <router-link to="/signup">sign up</router-link>.
      </p>

      <div
        v-if="!isLoggedOff"
        class="row mt-5 d-flex flex-column align-items-center"
      >
        <div
          v-if="!imageUploaded"
          class="col-4 border border-3 rounded-4 d-flex align-items-center justify-content-center"
          style="height: 60vh"
        >
          <i class="fa-solid fa-file-image fa-2xl text-dark-emphasis"></i>
        </div>

        <div v-else class="col-4 p-0" style="height: 60vh">
          <img
            :src="uploadedImage"
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

      <div v-if="numberOfUploadedImagesByUser > 0 && !isLoggedOff">
        <h1 class="mt-5 fs-1 fw-bold text-dark">Uploaded images</h1>
        <p class="mt-2 mb-0 text-dark-emphasis">
          You can use one of the images you uploaded earlier for prediction. Just click on the image to select it and then click the predict button.
        </p>

        <div class="row mt-3 gx-5">
          <div
            v-for="image in uploadedImagesByUser"
            :key="image.image_id"
            class="col-4"
          >
            <div class="mt-5" style="height: 50vh">
              <img
                @click="getSelectedImage(image.getImage)"
                :src="image.getImage"
                class="img-fluid border border-3 rounded-4"
                alt="Selected image"
                style="width: 100%; height: 100%; object-fit: cover; cursor: pointer;"
              />
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
      uploadedImage: null,
      imageUploaded: false,
      numberOfUploadedImagesByUser: 0,
      uploadedImagesByUser: [],
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
          console.log(response);
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
        })
        .catch((error) => {
          console.log(error);
        });
    }
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
