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
