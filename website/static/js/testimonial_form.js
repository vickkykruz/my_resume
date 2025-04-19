document.getElementById("testimonialForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const loading = document.querySelector(".loading");
  const feedback = document.getElementById("form-feedback");

  // Show loading animation
  loading.style.display = "block";
  feedback.style.display = "none";
  feedback.className = "form-feedback"; // Reset classes

  const formData = new FormData(this);

  try {
    const response = await fetch("/submit-testimonial-form", {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    loading.style.display = "none";

    if (response.ok) {
      feedback.innerText = result.success || "Testimonial submitted successfully.";
      feedback.classList.add("alert", "alert-success");
      this.reset(); // Only reset on success
    } else {
      feedback.innerText = result.error || "Something went wrong.";
      feedback.classList.add("alert", "alert-danger");
    }

    feedback.style.display = "block";
  } catch (error) {
    loading.style.display = "none";
    feedback.innerText = "Failed to send request.";
    feedback.classList.add("alert", "alert-danger");
    feedback.style.display = "block";
  }
});
