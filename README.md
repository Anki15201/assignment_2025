###### Task 1 AWS Project Description


    "This project demonstrates deploying a static website on AWS S3, hosting a web server on EC2, setting up a Lambda function triggered by S3 events, automating infrastructure with Terraform, scripting AWS interactions with Python (boto3), and implementing a basic CI/CD pipeline using jenkins"


## 1.1 Create an S3 Bucket Steps:

1. Go to the AWS Console > S3.

2. Click Create Bucket.

3. Give a unique name (example: my-static-site-bucket-2025).

4. Select your nearest region(e.g., us-east-1).

5. Uncheck "Block all public access" under permissions.

6. Acknowledge that the bucket will be public.

7. After creating, Go to Properties > Static website hosting.

8. Enable Static website hosting:

        - Choose "Host a static website"

        - Provide index document: index.html

9. Upload an index.html file.

10. Make it public:

    - Go to Permissions > Bucket Policy and add:

   ```json 
    {
        "Id": "Policy1745740347032",
        "Version": "2012-10-17",
        "Statement": [
            {
            "Sid": "Stmt1745740344940",
            "Action": [
                "s3:GetObject"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:s3:::my-static-site-bucket-2025/*",
            "Principal": "*"
            }
        ]
    }

#  1.2 Set up an EC2 Instance Steps:

1. Go to AWS Console > EC2 > Launch instance.

2. Choose Amazon Linux 2 AMI.

3. Instance type: t2.micro (free tier).

4. Create a new key pair or use existing.

5. In Security Group:

    - Allow HTTP (port 80).

    - Allow SSH (port 22) only from your IP.

6. After launching, connect via SSH:

    ssh -i mykeypair.pem ec2-user@<EC2-PUBLIC-IP>

7. install nginx

    sudo yum update -y
    sudo amazon-linux-extras install nginx1 -y
    sudo systemctl start nginx
    sudo systemctl enable nginx

8. Host a Simple HTML Page:

    echo "<h1>Welcome to Nginx on EC2!</h1>" | sudo tee /usr/share/nginx/html/index.html

9. Verify:
    
    http://your-public-ip



# 1.3 Modify the EC2 Security Group Rules

1. Go to EC2 Console → Instances → select your EC2 instance.

2. In the Description tab below, find the Security Group and click on its name.

3. In the Security Group page:

    - Click Inbound rules → Edit inbound rules.

4. Add Rule for HTTP:

    - Type: HTTP

    - Protocol: TCP 

    - Port Range: 80

    - Source: My IP(Example: 132.20.32.11)


# 1.4 AWS Lambda Function (Python)

    
    ```python
    import json
    import logging

    def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
            
    logger.info("Event Details: %s", json.dumps(event))
            
    return {
        'statusCode': 200,
        'body': json.dumps('Event logged successfully!')
    }
    


## Task 2: Scripting 

# (2.5) Python Scripts

1.  List S3 Buckets:

    ```python
    import boto3

    s3 = boto3.client('s3')

    def list_buckets():
        response = s3.list_buckets()
        for bucket in response['Buckets']:
            print(f'Bucket Name: {bucket["Name"]}')

    list_buckets()

  

2.  Count Objects in an S3 Bucket:

    ```python
    def get_object_count(bucket_name):
    response = s3.list_objects_v2(Bucket=bucket_name)
    if 'Contents' in response:
        return len(response['Contents'])
    else:
        return 0

    bucket_name = 'your-bucket-name'
    print(f"Total objects in {bucket_name}: {get_object_count(bucket_name)}")


3. CSV Analysis Script:

    ```python
    import csv

    def analyze_csv(file_path, threshold):
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['name']
                grade = float(row['grade'])
                if grade > threshold:
                    print(name)

    analyze_csv('students.csv', 75)



# (2.6) AWS SDK Documentation Links

1. Boto3 S3 Client Documentation
    - `https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html`

2. Boto3 Resource Documentation
    - `https://boto3.amazonaws.com/v1/documentation/api/latest/guide/resources.html`

3. AWS Lambda Python Docs
    - `https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html`


## Task 3: CI/CD Basics

1. Step 1: Install Jenkins
    To install Jenkins, you can either use an EC2 instance on AWS or install it on your local machine.

    # Install OpenJDK 11
    sudo apt update
    sudo apt install openjdk-11-jdk -y

    # Add Jenkins repository key
    wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -

    # Add the Jenkins repository
    sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'

    # Install Jenkins
    sudo apt update
    sudo apt install jenkins -y

    # Start Jenkins service
    sudo systemctl start jenkins
    sudo systemctl enable jenkins

    After installing Jenkins, you can access it by going to http://<your-ec2-ip>:8080 and unlocking Jenkins using the password from:

    ```bash
    cat /var/lib/jenkins/secrets/initialAdminPassword


2. Step 2: Configure GitHub Integration in Jenkins
    To make Jenkins communicate with GitHub:

    - Install necessary plugins:

        Git Plugin: For pulling code from GitHub.

        Pipeline Plugin: For defining Jenkins pipeline as code.

    - Create a new Jenkins Job:

        Go to Jenkins Dashboard → New Item → Select Freestyle project or Pipeline.

        Choose Freestyle Project for simplicity or Pipeline for more flexibility.

    - For a Freestyle Project:
        Source Code Management: Select Git and enter the URL of your GitHub repository.

        Build Triggers: You can set up Jenkins to poll GitHub for changes, or set up a webhook in GitHub to trigger Jenkins jobs automatically when changes are made.

            To poll SCM: Set it to * * * * * (every minute) or configure a specific interval.

            For Webhook: Set up a webhook in GitHub (GitHub → Settings → Webhooks → Jenkins).

3. Create the Build Steps

    - Install Dependencies (Python & boto3)
     # Install Python3 and pip
        sudo apt update
        sudo apt install python3-pip -y

    # Install boto3 for AWS SDK
        pip3 install boto3

    -  Run the Python Scripts 
    
    cd scripts/

    # Run the Python script for S3 list
        python3 s3_list_objects.py

    # Run the Python script for CSV analysis
        python3 csv_analysis.py

4.  Create a Jenkins Pipeline

    ```groovy
    pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/your-username/your-repo.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh '''
                sudo apt update
                sudo apt install python3-pip -y
                pip3 install boto3
                '''
            }
        }
        stage('Run Python Scripts') {
            steps {
                sh '''
                cd scripts/
                python3 s3_list_objects.py
                python3 csv_analysis.py
                '''
            }
        }
    }

## Task 4 : Infrastructure as Code (IaC) with Terraform

# (4.9) Terraform Script

 1. main.tf 
    
    provider "aws" {
    region = "us-east-1"
    }

    variable "instance_type" {
    default = "t2.micro"
    }

    variable "key_name" {}
    variable "bucket_name" {}

    resource "aws_instance" "web_server" {
    ami           = "ami-0c55b159cbfafe1f0" # Amazon Linux 2
    instance_type = var.instance_type
    key_name      = var.key_name

    tags = {
        Name = "WebServer"
    }

    provisioner "remote-exec" {
        inline = [
        "sudo yum install -y httpd",
        "sudo systemctl start httpd",
        "sudo systemctl enable httpd",
        "echo 'Hello from Terraform EC2!' > /var/www/html/index.html"
        ]

        connection {
        type        = "ssh"
        user        = "ec2-user"
        private_key = file("path/to/your/key.pem")
        host        = self.public_ip
        }
    }
    }

    resource "aws_s3_bucket" "website_bucket" {
    bucket = var.bucket_name
    acl    = "public-read"

    website {
        index_document = "index.html"
    }
    }

2. variables.tf

    variable "instance_type" {}
    variable "key_name" {}
    variable "bucket_name" {}

3. terraform.tfvars

    instance_type = "t2.micro"
    key_name      = "your-key-name"
    bucket_name   = "my-static-site-bucket-2025"

# (4.10) AWS Lambda Function

    resource "aws_lambda_function" "log_s3_events" {
        function_name = "logS3Events"
        role          = aws_iam_role.lambda_exec.arn
        handler       = "lambda_function.lambda_handler"
        runtime       = "python3.9"
        filename      = "lambda.zip"
    }

    resource "aws_s3_bucket_notification" "bucket_notification" {
        bucket = aws_s3_bucket.website_bucket.id

        lambda_function {
            lambda_function_arn = aws_lambda_function.log_s3_events.arn
            events              = ["s3:ObjectCreated:*"]
        }
    }

# (4.11) Cost

    Total estimated annual cost:
    - Around $8 per year (if usage is very low and within free limits).
    - If out of free tier, EC2 alone would cost $9/month ($108/year).

