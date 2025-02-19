const { createApp } = Vue;

// Initialize Showdown Converter
const converter = new showdown.Converter();

createApp({
    data() {
        return {
            emails: [],
            selectedEmail: null,
            inboxSummary: null, // Store the inbox summary
            loading: false, // Manage loading state
        };
    },
    mounted() {
        fetch("/api/emails")
            .then((r) => r.json())
            .then((data) => {
                this.emails = data;
            });
    },
    methods: {
        selectEmail(email) {
            this.selectedEmail = email;
        },
        summarizeInbox() {
            // Start loading state
            this.loading = true;

            // Extract email bodies as an array of raw documents
            const documents = this.emails.map((email) => email.body);

            // Send the array of documents to the summarize endpoint
            fetch("/api/summarize", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ documents }), // Send documents array
            })
                .then((r) => r.json())
                .then((data) => {
                    this.inboxSummary = data.summary; // Display the summary
                })
                .finally(() => {
                    this.loading = false; // Stop loading state
                });
        },
        renderMarkdown(markdownText) {
            try {
                // Convert Markdown to HTML
                const html = typeof markdownText === "string" ? converter.makeHtml(markdownText) : "";
                // Ensure new lines render properly
                return html.replace(/\n/g, "<br>");
            } catch (error) {
                console.error("Error rendering Markdown:", error);
                return "";
            }
        },

    },
}).mount("#app");
