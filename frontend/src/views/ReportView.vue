<template>
  <section class="container">
    <div class="px-5 my-5">
      <h1 class="fs-1 fw-bold text-dark">Personal particulars</h1>

      <div v-if="isLoggedOff">
        <p class="mt-3 text-dark-emphasis">
          To get started, please
          <router-link to="/login">log in</router-link> or
          <router-link to="/signup">sign up</router-link>.
        </p>
      </div>

      <div v-else>
        <div class="row mt-4">
          <div class="col-6">
            <div class="card mb-3 h-100">
              <div class="card-header">
                <h3 class="fw-bold text-dark m-0">Patient details</h3>
              </div>
              <div class="card-body">
                <p class="mb-1 fw-bold">User ID</p>
                <p>N/A</p>

                <p class="mt-3 mb-1 fw-bold">Age</p>
                <p>N/A</p>

                <p class="mt-3 mb-1 fw-bold">Date of birth</p>
                <p>N/A</p>
              </div>
            </div>
          </div>

          <div class="col-6">
            <div class="card mb-3 h-100">
              <div class="card-header">
                <h3 class="fw-bold text-dark m-0">Prediction results</h3>
              </div>
              <div class="card-body">
                <p>
                  The <b>ChexNet</b> model has analyzed the patient's image and
                  predicted that the patient has <b>atelectasis</b>. Please
                  remember that these results are generated by machine learning
                  algorithms and should be used in conjunction with professional
                  medical advice.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div class="col mt-3">
          <div class="card mb-3">
            <div class="card-header m-0">
              <h3 class="fw-bold text-dark m-0">Comments</h3>
            </div>
            <div class="card-body">
              <div class="py-1">
                <p><b>Comment 1:</b> The model's prediction seems accurate.</p>
              </div>
              <div class="py-1">
                <p>
                  <b>Comment 2:</b> Great job! The prediction aligns with the
                  professional diagnosis.
                </p>
              </div>
              <div class="py-1">
                <p>
                  <b>Comment 3:</b> I've reviewed the model's prediction and
                  it's quite impressive how it has managed to identify the
                  subtle signs of the disease. While it's not 100% accurate,
                  it's important to remember that even human experts can have
                  differing opinions on the same case. This tool can be a
                  valuable aid in the diagnostic process, providing a second
                  opinion and helping to identify areas that may require further
                  examination. As always, these results should be used in
                  conjunction with professional medical advice.
                </p>
              </div>
              <div class="py-1">
                <p>
                  <b>Comment 4:</b> The prediction was slightly off, but still
                  within an acceptable range.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div class="col mt-3">
          <div class="card mb-3">
            <div class="card-header m-0">
              <h3 class="fw-bold text-dark m-0">Report</h3>
            </div>
            <div class="card-body">
              <p>
                Our system provides a comprehensive report on the patient's
                health status based on the prediction results. This report
                includes detailed information about the patient and the disease
                it has based on the model's prediction. To generate this report,
                simply click on the <b>Generate Report</b> button. Please note
                that this report should be used in conjunction with professional
                medical advice.
              </p>

              <button class="custom-button-dark" @click="generateReport">
                Generate Report
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import jsPDF from "jspdf";

export default {
  name: "ReportView",
  computed: {
    isLoggedOff() {
      return this.$store.state.token === "";
    },
  },
  created() {
    this.$store.commit("setSelectedNavbarItem", "report");
  },
  mounted() {
    document.title = "Report";
  },
  methods: {
    generateReport() {
      const doc = new jsPDF("p", "mm", "a4");

      // Set up margins
      const marginLeft = 20;
      const marginTop = 20;
      const lineHeight = 10;
      let currentY = marginTop;

      // Add header
      doc.setFontSize(18);
      doc.text("Personal particulars", marginLeft, currentY);
      currentY += lineHeight * 2;

      // Add SubHeader 1
      doc.setFontSize(16);
      doc.text("Patient details", marginLeft, currentY);
      currentY += lineHeight;

      // Add User ID
      doc.setFontSize(12);
      doc.text("User ID", marginLeft, currentY);
      currentY += lineHeight / 2;
      doc.setFontSize(10);
      doc.text("N/A", marginLeft, currentY);
      currentY += lineHeight;

      // Add Age
      doc.text("Age", marginLeft, currentY);
      currentY += lineHeight / 2;
      doc.setFontSize(10);
      doc.text("N/A", marginLeft, currentY);
      currentY += lineHeight;

      // Add Date of Birth
      doc.text("Date of birth", marginLeft, currentY);
      currentY += lineHeight / 2;
      doc.setFontSize(10);
      doc.text("N/A", marginLeft, currentY);
      currentY += lineHeight * 2;

      // Add SubHeader 2
      doc.setFontSize(16);
      doc.text("Prediction results", marginLeft, currentY);
      currentY += lineHeight;

      // Add Prediction Text
      const predictionText = `The ChexNet model has analyzed the patient's image and predicted that the patient has atelectasis. Please remember that these results are generated by machine learning algorithms and should be used in conjunction with professional medical advice.`;
      doc.setFontSize(12);
      doc.text(predictionText, marginLeft, currentY, { maxWidth: 170 });
      currentY += lineHeight * 3; // Adjust based on text length

      // Add SubHeader 3
      doc.setFontSize(16);
      doc.text("Comments", marginLeft, currentY);
      currentY += lineHeight;

      // Add Comments
      const comments = [
        "Comment 1: The model's prediction seems accurate.",
        "Comment 2: Great job! The prediction aligns with the professional diagnosis.",
        "Comment 3: I've reviewed the model's prediction and it's quite impressive how it has managed to identify the subtle signs of the disease. While it's not 100% accurate, it's important to remember that even human experts can have differing opinions on the same case. This tool can be a valuable aid in the diagnostic process, providing a second opinion and helping to identify areas that may require further examination. As always, these results should be used in conjunction with professional medical advice.",
        "Comment 4: The prediction was slightly off, but still within an acceptable range.",
      ];

      comments.forEach((comment, index) => {
        let maxWidth = 170;
        doc.setFontSize(12);
        doc.text(comment, marginLeft, currentY, { maxWidth: maxWidth });

        let commentLines = doc.splitTextToSize(comment, maxWidth);
        currentY += lineHeight * (1 + commentLines.length) / 2;
      });

      doc.save("patient_report.pdf");
    },
  },
};
</script>
