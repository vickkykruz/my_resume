/*document.getElementById("contactForm").addEventListener("submit", async function (e) {
  e.preventDefault(); // Prevent normal form submission

  // Show loading animation
  document.querySelector(".loading").style.display = "block";
  document.querySelector(".error-message").style.display = "none";
  document.querySelector(".sent-message").style.display = "none";

  // Collect form data
  const formData = new FormData(this);

  try {
    const response = await fetch("/send-mail", {
      method: "POST",
      body: formData
    });

    const result = await response.json();

    document.querySelector(".loading").style.display = "none";
    document.querySelector(".error-message").style.display = "none";

    if (response.ok) {
      document.querySelector(".sent-message").style.display = "block";
      this.reset(); // Reset form
      document.querySelector(".error-message").style.display = "none";
    } 
    //else {
    //  document.querySelector(".error-message").innerText = result.error || "Something went wrong.";
    //  document.querySelector(".error-message").style.display = "block";
    //}
  } catch (error) {
    console.log("Error: ", e)
    document.querySelector(".loading").style.display = "none";
    document.querySelector(".error-message").innerText = "Failed to send request.";
    document.querySelector(".error-message").style.display = "none";
  }
});
*/


document.getElementById("contactForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const loading = document.querySelector(".loading");
  const feedback = document.getElementById("form-feedback");

  // Show loading animation
  loading.style.display = "block";
  feedback.style.display = "none";
  feedback.className = "form-feedback"; // Reset classes

  const formData = new FormData(this);

  try {
    const response = await fetch("/send-mail", {
      method: "POST",
      body: formData
    });

    const result = await response.json();
    loading.style.display = "none";

    if (response.ok) {
      feedback.innerText = result.success || "Message sent successfully.";
      feedback.classList.add("alert", "alert-success");
    } else {
      feedback.innerText = result.error || "Something went wrong.";
      feedback.classList.add("alert", "alert-danger");
    }

    feedback.style.display = "block";
    if (response.ok) this.reset(); // Reset form only on success

  } catch (error) {
    loading.style.display = "none";
    feedback.innerText = "Failed to send request.";
    feedback.classList.add("alert", "alert-danger");
    feedback.style.display = "block";
  }
});
