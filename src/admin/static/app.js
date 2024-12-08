// Helper Function to Handle API Calls
document.addEventListener("DOMContentLoaded", () => {
    const navbarLinks = document.querySelectorAll(".navbar a");
    const sections = document.querySelectorAll(".content-section");

    // Hide all sections except the first one
    sections.forEach((section, index) => {
        if (index === 0) {
            section.classList.add("active");
        } else {
            section.classList.remove("active");
        }
    });

    // Add click event listeners to navigation links
    navbarLinks.forEach((link) => {
        link.addEventListener("click", (e) => {
            e.preventDefault(); // Prevent default anchor behavior
            const targetSectionId = link.getAttribute("data-section");

            // Hide all sections
            sections.forEach((section) => {
                section.classList.remove("active");
            });

            // Show the target section
            const targetSection = document.getElementById(targetSectionId);
            if (targetSection) {
                targetSection.classList.add("active");
            }
        });
    });
});

async function apiCall(endpoint, method = "GET", body = null) {
    const headers = { "Content-Type": "application/json" };
    const options = { method, headers };

    if (body) {
        options.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(endpoint, options);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "An unknown error occurred");
        }
        return data;
    } catch (error) {
        console.error(`Error calling ${endpoint}:`, error);
        throw error;
    }
}

// Stop Auction Functionality
async function handleStopAuction(e) {
    e.preventDefault();
    const auctionId = document.getElementById("auction-id").value;
    const resultContainer = document.getElementById("stop-auction-result");
    resultContainer.textContent = "Processing...";

    try {
        const data = await apiCall("/api/stop-auction", "POST", { auction_id: auctionId });
        resultContainer.textContent = data.message;
    } catch (error) {
        resultContainer.textContent = `Error: ${error.message}`;
    }
}

// Remove and Block User Functionality
async function handleRemoveBlockUser(e) {
    e.preventDefault();
    const userId = document.getElementById("user-id").value;
    const resultContainer = document.getElementById("remove-block-user-result");
    resultContainer.textContent = "Processing...";

    try {
        const data = await apiCall("/api/remove-block-user", "POST", { user_id: userId });
        resultContainer.textContent = data.message;
    } catch (error) {
        resultContainer.textContent = `Error: ${error.message}`;
    }
}

// Manage Categories Functionality
async function handleManageCategory(e) {
    e.preventDefault();
    const action = document.getElementById("action").value;
    const categoryId = document.getElementById("category-id").value;
    const categoryName = document.getElementById("category-name").value;
    const resultContainer = document.getElementById("manage-category-result");
    resultContainer.textContent = "Processing...";

    try {
        const data = await apiCall("/api/manage-category", "POST", {
            action,
            category_id: categoryId,
            category_name: categoryName,
        });
        resultContainer.textContent = data.message;
    } catch (error) {
        resultContainer.textContent = `Error: ${error.message}`;
    }
}

// View Flagged Items Functionality
async function fetchFlaggedItems() {
    const resultContainer = document.getElementById("flagged-items-container");
    resultContainer.innerHTML = "<p>Loading...</p>";

    try {
        const data = await apiCall("/api/flagged-items");
        console.log(data.flagged_items);
        if (data.flagged_items.length > 0) {
            const itemHtml = data.flagged_items
                .map(
                    (item) => `
                <div class="flagged-item">
                    <h3>${item.name}</h3>
                    <p><strong>Description:</strong> ${item.description}</p>
                    <p><strong>Category:</strong> ${item.category}</p>
                    <p><strong>Flag Reason:</strong> ${item.flag_reason}</p>
                    <p><strong>Flagged Date:</strong> ${item.flagged_date}</p>
                </div>
                <hr>
            `
                )
                .join("");

            resultContainer.innerHTML = itemHtml;
        } else {
            resultContainer.innerHTML = "<p>No flagged items found.</p>";
        }
    } catch (error) {
        resultContainer.innerHTML = `<p>Error: ${error.message}</p>`;
    }
}

// View Active Auctions Functionality
async function fetchActiveAuctions() {
    const resultContainer = document.getElementById("active-auctions-list");
    resultContainer.innerHTML = "<li>Loading...</li>";

    try {
        const data = await apiCall("/api/active-auctions");
        console.log(data);
        if (data.active_auctions.length > 0){
            const auctionHtml = data.active_auctions
                .map(
                    (auction) => `
                <div class="auction-item">
                    <h3>${auction.title}</h3>
                    <p><strong>Description:</strong> ${auction.description}</p>
                    <p><strong>Starting Price:</strong> $${auction.starting_price.toFixed(2)}</p>
                    <p><strong>Current Price:</strong> $${auction.current_price.toFixed(2)}</p>
                    <p><strong>Start Time:</strong> ${new Date(auction.start_time).toLocaleString()}</p>
                    <p><strong>End Time:</strong> ${new Date(auction.end_time).toLocaleString()}</p>
                    <p><strong>Category:</strong> ${auction.category}</p>
                </div>
                <hr>
            `
                )
                .join("");

            resultContainer.innerHTML = auctionHtml;
        }else{
            resultContainer.innerHTML = `<li>No active auctions!</li>`;
        }
        
    } catch (error) {
        resultContainer.innerHTML = `<li>Error: ${error.message}</li>`;
    }
}

// Examine Metrics Functionality
async function handleMetrics(e) {
    e.preventDefault(); // Prevent page reload on form submission

    // Get values from the input fields
    const days = document.getElementById("days").value || 0; // Default to 0 if empty
    const weeks = document.getElementById("weeks").value || 0;
    const months = document.getElementById("months").value || 0;

    const resultContainer = document.getElementById("metrics-result");
    resultContainer.textContent = "Processing..."; // Feedback while processing

    try {
        // Construct query parameters
        const queryParams = new URLSearchParams({ days, weeks, months });

        // Make the API call
        const data = await apiCall(`/api/metrics?${queryParams.toString()}`);
        console.log(data);
        if (data.active_auctions.length > 0){
            const auctionHtml = data.active_auctions
                .map(
                    (auction) => `
                <div class="auction-item">
                    <h3>${auction.title}</h3>
                    <p><strong>Description:</strong> ${auction.description}</p>
                    <p><strong>Starting Price:</strong> $${auction.starting_price.toFixed(2)}</p>
                    <p><strong>Current Price:</strong> $${auction.current_price.toFixed(2)}</p>
                    <p><strong>Start Time:</strong> ${new Date(auction.start_time).toLocaleString()}</p>
                    <p><strong>End Time:</strong> ${new Date(auction.end_time).toLocaleString()}</p>
                    <p><strong>Category:</strong> ${auction.category}</p>
                </div>
                <hr>
            `
                )
                .join("");

            resultContainer.innerHTML = auctionHtml;
        }else{
            resultContainer.innerHTML = `<li>No stopped auctions in this timeframe!</li>`;
        }
    } catch (error) {
        // Display error message in case of failure
        resultContainer.textContent = `Error: ${error.message}`;
    }
}

// Attach the event listener
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("metrics-form").addEventListener("submit", handleMetrics);
});

async function fetchUnrespondedEmails() {
    const container = document.getElementById("unresponded-emails-container");
    container.innerHTML = "<p>Loading...</p>";

    try {
        const data = await apiCall("/api/unresponded-emails");

        // Build HTML for unresponded emails
        if (data.unresponded_emails.length > 0) {
            const emailsHtml = data.unresponded_emails
                .map(
                    (email) => `
                <div class="email-item">
                    <p><strong>Email Address:</strong> ${email.user_email}</p>
                    <p><strong>Message:</strong> ${email.message}</p>
                    <textarea id="response-text-${email.email_id}" placeholder="Enter response text"></textarea>
                    <button onclick="respondToEmail('${email.email_id}', '${email.user_email}')">Send Response</button>
                </div>
                <hr>
            `
                )
                .join("");

            container.innerHTML = emailsHtml;
        } else {
            container.innerHTML = "<p>No unresponded emails found.</p>";
        }
    } catch (error) {
        container.innerHTML = `<p>Error: ${error.message}</p>`;
    }
}


// Respond to Emails Functionality
async function respondToEmail(emailId, userEmail) {
    const responseText = document.getElementById(`response-text-${emailId}`).value;

    if (!responseText.trim()) {
        alert("Response text cannot be empty!");
        return;
    }

    try {
        const data = await apiCall("/api/respond-email", "POST", {
            email_id: emailId,
            response_text: responseText,
        });

        alert(`Response sent to ${userEmail}: ${data.message}`);
        // Reload the unresponded emails after sending a response
        fetchUnrespondedEmails();
    } catch (error) {
        alert(`Failed to send response: ${error.message}`);
    }
}

// Attach Event Listeners
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("stop-auction-form").addEventListener("submit", handleStopAuction);
    document.getElementById("remove-block-user-form").addEventListener("submit", handleRemoveBlockUser);
    document.getElementById("manage-category-form").addEventListener("submit", handleManageCategory);
    document.getElementById("view-flagged-items").addEventListener("click", fetchFlaggedItems);
    document.getElementById("view-active-auctions").addEventListener("click", fetchActiveAuctions);
    document.getElementById("metrics-form").addEventListener("submit", handleMetrics);
    document.getElementById("load-unresponded-emails").addEventListener("click", fetchUnrespondedEmails);
});
