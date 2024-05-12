<template>
  <section class="container">
    <div class="px-5 my-5">
      <h1 class="fs-1 fw-bold text-dark">Gallery</h1>
      <p v-if="isLoggedOff" class="mt-3 text-dark-emphasis">
        To look at the images you uploaded, please
        <router-link to="/login">log in</router-link> or
        <router-link to="/signup">sign up</router-link>.
      </p>

      <div v-else>
        <p v-if="numberOfUploadedImagesByUser === 0" class="mt-3 text-dark-emphasis">
          You have not uploaded any images yet.
        </p>

        <div v-else class="row mt-5">
          <div
            v-for="image in uploadedImagesByUser"
            :key="image.id"
            class="col-4 mb-4"
          >
            <img
              @click="navigateToImageDetailsPage(image)"
              :src="image.getImage"
              class="img-fluid border border-3 rounded-4"
              alt="Uploaded image"
              style="width: 100%; height: 100%; object-fit: cover; cursor: pointer;"
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
  name: "GalleryView",
  computed: {
    isLoggedOff() {
      return this.$store.state.token === "";
    },
  },
  data() {
    return {
      numberOfUploadedImagesByUser: 0,
      uploadedImagesByUser: [],
    };
  },
  methods: {
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
    navigateToImageDetailsPage(image) {
      localStorage.setItem("selected_patient_image", JSON.stringify(image));
      this.$router.push("/image_details");
    }
  },
  created() {
    this.$store.commit("setSelectedNavbarItem", "gallery");
  },
  mounted() {
    document.title = "Gallery";

    this.getNumberOfUploadedImages();
    this.getUploadedImages();
  },
};
</script>
