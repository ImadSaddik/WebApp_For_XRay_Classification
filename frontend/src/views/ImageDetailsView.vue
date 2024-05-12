<template>
  <section class="container">
    <div class="px-5 my-5">
      <h1 class="fs-1 fw-bold text-dark">Image details</h1>

      <div class="row gx-5 mt-5">
        <div class="col-6">
          <img
            :src="image.getImage"
            class="img-fluid border border-3 rounded-4"
            alt="Uploaded image"
            style="width: 100%; height: 100%; object-fit: cover"
          />
        </div>

        <div class="col-6">
          <h3 class="fw-bold text-dark">Information</h3>
          <p class="mt-3 mb-1 fw-bold">User ID</p>
          <p>This image belongs to the user with id = {{ image.user_id }}</p>

          <p class="mt-3 mb-1 fw-bold">Classification</p>
          <p>This image is classified as <b>{{ image.classification }}</b></p>

          <p class="mt-3 mb-1 fw-bold">No longer need the image ?</p>
          <button class="mt-1 custom-button-dark" @click="deleteImage">
            Delete Image
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import axios from "axios";

export default {
  name: "ImageDetailsView",
  data() {
    return {
      image: {},
    };
  },
  methods: {
    getImage() {
      this.image = JSON.parse(localStorage.getItem("selected_patient_image"));
    },
		async deleteImage() {
			const data = JSON.stringify({
				image_id: this.image.image_id,
			});

			await axios
				.post("api/v1/deleteImage/", data, {
					headers: {
							"Content-Type": "application/json",
							"X-CSRFToken": "csrftoken"
						}
				})
				.then(() => {
					this.$router.push({ name: 'gallery', replace: true});
					localStorage.removeItem("selected_patient_image");
				})
				.catch((error) => {
					console.error(error);
				});
		}
  },
	created() {
    if (localStorage.getItem("selected_patient_image") === null){
      this.$router.push({ name: "gallery", replace: true });
    }
  },
  mounted() {
    document.title = "Image details";
    this.getImage();
  },
};
</script>
