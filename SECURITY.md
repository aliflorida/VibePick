# Security Policy

## Supported Versions

🔒 VibePick Security Policy
Last Updated: April 2025
🔐 Data Security
Firebase Access: We use Firebase Realtime Database to store session-level group planning data. All access is authenticated through a secure service account key stored in a protected, non-public environment.

Read/Write Access: Only the server (app backend) has permission to read/write Firebase data. End-users have no direct access to the database.

No Sensitive Data Stored: VibePick does not store passwords, financial information, or personal identifiers like SSNs. All data collected is limited to group planning inputs (e.g. first name, preferences, location, availability).

🔑 API Key Management
All API keys (e.g., OpenAI, Foursquare, MailerSend) are stored in secured environment variables or external key files.

These credentials are never committed to the codebase or shared publicly.

Access is restricted to read-only or scoped API calls whenever possible.

📡 Data Transmission
All communication between the app and external services is encrypted via HTTPS.

Emails sent using MailerSend are dispatched via secure endpoints using verified sender identity.

🔐 Authentication & Authorization
No user login is currently required. All group sessions are anonymous unless users explicitly choose to share their name or email for notifications.

Firebase session data is sandboxed per session ID and not cross-accessible.

🛡️ Development Practices
All dependencies are kept up-to-date and monitored for known vulnerabilities using pip and GitHub dependabot alerts.

Code reviews are conducted prior to major feature releases.

API usage is rate-limited to prevent abuse and ensure fair access.

🚨 Incident Response
In case of suspected data breach or vulnerability discovery, please contact the developer team immediately

We commit to investigating and mitigating any report within 48 hours.
