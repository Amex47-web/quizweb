document.addEventListener("DOMContentLoaded", () => {
    const overlay = document.getElementById("auth-overlay");
    const loginForm = document.getElementById("login-tab");
    const signupForm = document.getElementById("signup-tab");
    const loginTabButton = document.getElementById("login-tab-butn");
    const signupTabButton = document.getElementById("signup-tab-butn");
    const closeButton = document.getElementById("close_btn");
    const mobileSite = document.querySelector("#mobile-site");
    const desktopLinks = document.querySelector("#desktop-links");
    const menuButton = document.querySelector("#menu-butn");
    const crossButton = document.querySelector("#cross-butn");

    // Toggle Mobile Menu Visibility
    menuButton.addEventListener("click", () => {
        mobileSite.classList.remove("hidden");
    });

    crossButton.addEventListener("click", () => {
        mobileSite.classList.add("hidden");
    });

    // Manage Responsiveness Dynamically
    const handleResize = () => {
        if (window.innerWidth <= 768) {
            desktopLinks.classList.add("hidden");
        } else {
            desktopLinks.classList.remove("hidden");
            mobileSite.classList.add("hidden"); // Ensure mobile menu is hidden
        }
    };

    // Initial Check + Event Listener
    handleResize();
    window.addEventListener("resize", handleResize);


    // Open the authentication overlay
    document.getElementById("login_btn")?.addEventListener("click", () => {
        overlay?.classList.remove("hidden");
    });

    // Close the authentication overlay
    closeButton?.addEventListener("click", () => {
        overlay?.classList.add("hidden");
    });

    // Switch to the Login form
    loginTabButton?.addEventListener("click", () => {
        loginForm?.classList.remove("hidden");
        signupForm?.classList.add("hidden");
        loginTabButton?.classList.add("active-tab");
        signupTabButton?.classList.remove("active-tab");
    });

    // Switch to the Signup form
    signupTabButton?.addEventListener("click", () => {
        signupForm?.classList.remove("hidden");
        loginForm?.classList.add("hidden");
        signupTabButton?.classList.add("active-tab");
        loginTabButton?.classList.remove("active-tab");
    });

    // Handle Login form submission
    loginForm?.addEventListener("submit", (e) => {
        e.preventDefault();

        const email = loginForm.querySelector("input[name='email']").value.trim();
        const password = loginForm.querySelector("input[name='password']").value.trim();

        if (!email || !password) {
            alert("Email and password are required.");
            return;
        }

        axios.post("/login", { email, password })
            .then((response) => {
                if (response.data.message === "Login successful") {
                    console.log("Login successful:", response.data.user);
                    alert("Welcome, " + response.data.user + "!");
                    overlay?.classList.add("hidden");
                    window.location.href = "/"; // Redirect to the homepage
                }
            })
            .catch((error) => {
                if (error.response) {
                    alert(error.response.data.error || `Error ${error.response.status}: An issue occurred.`);
                } else {
                    alert("Network error. Please check your connection.");
                }
                console.error("Axios error:", error);
            });
    });

    // Handle Signup form submission
    signupForm?.addEventListener("submit", (e) => {
        e.preventDefault();

        const username = signupForm.querySelector("input[name='username']").value.trim();
        const email = signupForm.querySelector("input[name='email']").value.trim();
        const password = signupForm.querySelector("input[name='password']").value.trim();

        if (!username || !email || !password) {
            alert("All fields are required.");
            return;
        }

        const submitButton = signupForm.querySelector("button");
        submitButton.disabled = true;
        console.log("signup submit button ",submitButton);
        submitButton.value = "Signing up...";

        axios.post("/signup", { username, email, password })
            .then((response) => {
                if (response.data.message === "Signup successful") {
                    console.log("Signup successful:", response.data.user);
                    alert("Signup successful! Please log in.");
                    signupForm.reset(); // Clear the form
                    loginTabButton?.click(); // Switch to the login form
                }
            })
            .catch((error) => {
                if (error.response) {
                    alert(error.response.data.error || `Error ${error.response.status}: An issue occurred.`);
                } else {
                    alert("Network error. Please check your connection.");
                }
                console.error("Axios error:", error);
            })
            .finally(() => {
                submitButton.disabled = false;
                submitButton.value = "Sign up";
            });
    });

    // Handle protected actions
    document.querySelectorAll(".protected-action").forEach((link) => {
        link.addEventListener("click", (e) => {
            e.preventDefault(); // Prevent default link behavior
            const url = link.getAttribute("href"); // Get the URL for the protected route
            console.log("link is clicked ",link);
            axios.get(url)
            .then((response) => {
                console.log("Axios response:", response);
                if (response.status === 200 && response.data.error === 'Unauthorized') {
                    console.log("Unauthorized detected with 200 response.");
                    overlay?.classList.remove("hidden");
                    overlay?.classList.add("active");
                } else if (response.status === 200) {
                    console.log("Access granted:", url);
                    window.location.href = url;
                    // overlay?.classList.remove("hidden");
                    // overlay?.classList.add("active");
                }
            })
            .catch((error) => {
                if (error.response && error.response.status === 401) {
                    console.log("Unauthorized access; showing login overlay.");
                    overlay?.classList.remove("hidden");
                    overlay?.classList.add("active");
                } else {
                    alert("An error occurred. Please try again.");
                    console.error("Error:", error);
                }
            });

        });
    });
});
