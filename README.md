# Smart Healthcare Symptom Triage and Resource Allocator

AWS Lambda-based solution for automating patient triage in Kenyan hospitals, built for the AWS Lambda Hackathon. Uses Kenya MOH triage rules (chest pain = 10, fever = 8, cough = 3) at $0 cost within AWS Free Tier.

## AWS Setup (Week 1, Step 1, June 7, 2025)
- **Free Tier Account**: Active, PDF invoices and Free Tier alerts enabled (root user email).
- **IAM**:
  - User: `AWSCLIUser` (programmatic access).
  - Group: `LambdaHackathonGroup` with policies: `AWSLambda_FullAccess`, `AmazonAPIGatewayAdministrator`, `AmazonDynamoDBFullAccess`.
  - CLI: Configured with `aws configure` (us-east-1, JSON output).
- **Billing Alerts**:
  - CloudWatch: `FreeTierCostAlert` (`> $0.01`, `BillingAlerts` SNS topic, email confirmed).
  - Usage Log: `June 7, 0 Lambda requests, 0 API calls, 0 DynamoDB GB`.
- **Tools**: AWS CLI, Serverless Framework, Python 3.9, Node.js, Git (Windows).

# TriageAI Staff Frontend

## Features

- **Animated Landing Page:** Modern UI with GSAP-powered hero, statistics, and section transitions.
- **Interactive Service Cards:** Each service card in the "Services" section has a "Learn More" button that opens a dynamic, animated modal with tabbed content.
- **Dynamic Modal System:** Full-screen modal overlays with smooth GSAP animations, keyboard accessibility (ESC to close), and tab navigation.
- **Tabbed Modal Content:** Each modal contains user-friendly, non-technical explanations of the service's workflow and impact.
- **Research Section:** Tabbed storytelling based on real-world hospital research.
- **Interactive Triage:** Symptom analyzer with text, voice, and body-map input.
- **Live Dashboard Demo:** D3.js-powered queue chart and staff heatmap for professionals.
- **Accessibility:** Modal can be closed by clicking outside or pressing ESC. Buttons have ripple effects.

## How to Use

1. **Open the Project:** Open `page.html` in your browser.
2. **Explore Services:** Click "Learn More" on any service card to open the modal. Use the tabs to explore details.
3. **Try Triage:** Use the interactive triage form (text, voice, or body map).
4. **View Dashboard:** Scroll to "For Professionals" for live queue and staff heatmap demo.

## Key Implementation Notes

- **Modal System:**  
  - Only one modal can be open at a time.  
  - Modal opens instantly on a single click, even if clicked rapidly.  
  - Modal closes on ESC, close button, or clicking the overlay.
  - Modal content and tabs are dynamically generated from a JS object.
  - Modal animations are handled with GSAP for smoothness and reliability.

- **Performance:**  
  - All animations are optimized for smoothness.
  - Modal logic prevents double/triple clicks and race conditions.

- **Accessibility:**  
  - Keyboard navigation and ESC support for modals.
  - Focus is not trapped, but modal disables background scroll.

## Customization

- **To update modal content:**  
  Edit the `modalData` object in `page.html` to change tab names or content for each service.

- **To add a new service card:**  
  1. Add a new card in the Services section with a unique `data-service` attribute.
  2. Add a corresponding entry in the `modalData` object.

## Dependencies

- [TailwindCSS](https://tailwindcss.com/)
- [GSAP](https://greensock.com/gsap/)
- [D3.js](https://d3js.org/)
- [Poppins Font](https://fonts.google.com/specimen/Poppins)

## Development Notes

- All main initialization functions (`initLoader`, `initMagneticButtons`, `initScrollAnimations`, `initInteractiveElements`, `initModal`) must be called in the app entry point.
- The modal system uses an `isModalAnimating` flag to prevent race conditions and ensure reliable open/close behavior.
- The code is structured for clarity and maintainability, with each section's logic in its own function.

## License

Demo code for AWS Lambda Hackathon. See project root for license details.
