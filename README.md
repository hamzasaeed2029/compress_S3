# compress_S3
this is a project to check how to compress s3 contents using SAM and Lambda function.

PRE-REQUISITES:
1) Suppose the name of s3 bucket is: highqbucket
2) this bucket is growing in size with json files.

TASK-1:

PROCEDURE:
	
3) create sam environment and create "sam" folder in ubuntu.
4) in sam folder, create sam template file "lambda.yml" and lambda function "lambda_function.py" under folder mylambda.
5) run commands to test and validate:
	$sam validate -t lambda.yml
	$sam package -t lambda.yml --output-template-file template.yml --s3-bucket highqbucket
	  the output of above commands will be successful like:
		
        Uploading to 0fe201fc9be67184616fde028b7117f3  568 / 568  (100.00%)
		Successfully packaged artifacts and wrote output template to file lambda-pkg.yml.
		Execute the following command to deploy the packaged template
		sam deploy --template-file /var/www/sam/sam_project/template.yml --stack-name <YOUR STACK NAME>


		
TASK-2:

1) Double check by running this command, AWS CLI will read the CloudFormation template from the specified file, check its syntax and structure, and then provide feedback on whether the template is valid or if there are any errors or issues that need to be addressed. 
	$aws cloudformation validate-template --template-body file://template.yml
2) deploy above in cloudformation stack using command: 
	$sam deploy --template-file /var/www/sam/sam_project/template.yml --stack-name sam-stack --capabilities CAPABILITY_IAM --region eu-west-1
OR

2) The configuration template.yml use the zip file of lambda_function.py to be placed in highqbucket bucket. You can place the template.yml inside highqbucket.
 2.1) go to cloudformation and create stack.
 2.2) enter template.yml s3 url or upload by clicking "Upload a template file"
 2.3) stack will be up in some time.
 2.4) test the stack by inserting files in newly created s3 bucket "my-incoming-files-bucket"

TASK-3:
1) wrote as per best practices along with testing and code comments.
2) each task has its own branch.
3) each commit message is descriptive in order to be understandable.
4) kept the readme file up-to-date along with procedure.


TASK-4


To calculate the monthly cost for this scenario, we need to consider several factors:

1) Storage cost for both the original files and the compressed files in the S3 bucket (Region: eu-west-1)
2) Number of PUT requests (uploading the original files).
3) Number of COPY requests (copying the compressed files within the S3 bucket).
4) Number of DELETE requests (deleting the original files).
5) Lambda function invocation cost for compressing the files.
6) Suppose original file stays in the S3 bucket for approx 1 second before being processed by the Lambda function.
7) Suppose the compressed file size is of average 3MB.
8) suppose Lambda execution duration: 10 seconds.

Given:

Average file size: 10 MB
Number of files processed per hour: 1,000,000
Compressed file size: 3 MB
Original file retention time in S3: 1 second

	Storage Cost:
	Original files: 10 MB/file * 1,000,000 files * 3600 seconds/hour * 24 hours/day * 30 days = 259,200,000,000 MB-seconds
	Compressed files: 3 MB/file * 1,000,000 files * 3600 seconds/hour * 24 hours/day * 30 days = 77,760,000,000 MB-seconds
	Since S3 pricing is tiered based on the total amount of data stored per month, let's convert these MB-seconds to GB-months:
	
	Original files: 259,200,000,000 MB-seconds / (1024 MB/GB * 1024 seconds/month) = 245.85 GB-months
	Compressed files: 77,760,000,000 MB-seconds / (1024 MB/GB * 1024 seconds/month) = 73.75 GB-months
	
	PUT Requests:
	1,000,000 files/hour * 24 hours/day * 30 days = 720,000,000 PUT requests
	
	COPY Requests:
	Since every uploaded file is copied, the number of COPY requests will be equal to the number of PUT requests i.e. 720,000,000 COPY requests.
	
	DELETE Requests:
	The same as the number of PUT requests, as each original file is deleted after compression i.e. 720,000,000 DELETE requests.
	
	Storage Cost:
	Original files: 245.85 GB-months * $0.023 per GB-month = $5.66
	Compressed files: 73.75 GB-months * $0.023 per GB-month = $1.70
	
	PUT Requests:
	720,000,000 requests * $0.005 per 1,000 requests = $3,600
	
	COPY Requests:
	Same as PUT Requests: $3,600
	
	DELETE Requests:
	Same as PUT Requests: $3,600
	
	Lambda Function Invocation Cost:
	Suppose Lambda execution duration: 10 seconds. 
	Number of Lambda invocations:
	Same as the number of files processed per hour: 1,000,000 invocations/hour * 24 hours/day * 30 days = 720,000,000 invocations/month
	Total execution time:
	
	720,000,000 invocations * 10 seconds/invocation = 7,200,000,000 seconds
	Convert execution time to GB-seconds:
	
	7,200,000,000 seconds * (1 GB / 1,024 MB) = 7,031,250 GB-seconds
	Lambda pricing:
	
	$0.20 per 1 million requests
	$0.0000166667 per GB-second (0.0000166667 USD per 1 GB-second)
	Now let's calculate the Lambda cost:
	
	Lambda invocation cost:
	Since the first 1 million requests are free, we need to calculate the cost for the remaining requests: 
	(720,000,000 - 1,000,000) / 1,000,000 * $0.20 = $143.80
	
	Execution time cost:
	7,031,250 GB-seconds * $0.0000166667 per GB-second = $117.19
	
	Adding up the Lambda costs:
	Total Lambda Cost = Lambda Invocation Cost + Execution Time Cost
	= $143.80 + $117.19
	= $260.99

Adding up the costs:
Total Monthly Cost = Storage Cost + PUT Requests + COPY Requests + DELETE Requests + Total Lambda Cost
= $5.66 + $1.70 + $3,600 + $3,600 + $3,600 + $260.99
= $14,071.05/Month

Since the first 1 million requests are free and subsequent requests are charged, let's calculate the cost for the second month and onwards:

	Number of invocations beyond the free tier: 719,000,000 (720,000,000 invocations/month - 1,000,000 free invocations/month)
	
	Cost for invocations beyond the free tier:
	= (719,000,000 / 1,000,000) * $0.20
	= $143.80

Total Monthly Cost (for the second month and onwards):
= Storage Cost + PUT Requests + COPY Requests + DELETE Requests + Lambda Function Invocation Cost (beyond the free tier)
= $5.66 + $1.70 + $3,600 + $3,600 + $3,600 + $143.80
= $14,355.16

So, the estimated monthly cost for the first month is $14,071.05 and from second month and onwards is approximately $14,355.16 USD/month.


Cost Saving Suggestions:
	1) By optimizing storage class. Analyze our data access patterns and choose the appropriate storage class.
	2) Implement lifecycle policies to automatically transition objects to cheaper storage classes or delete them when they're no longer needed. If the data retention period is for few months (1-3 months) and needs instant retrieval as well, we can use S3 One Zone-IA since it offers at least 30 days minimum storage duration and is cheaper than standard type. 
	Moreover if the object retention period is for few years (1-2 years for example) and retrieval can be a possibility (say once a week) here than moving to Glacier flexible retrieval is better option in my point of view. But if we do not want any retrieval also we want it to store for a longer period (5-10 years for example) than we should be using Glacier deep archive.
	3) If our services aren't in the same region then minimize unnecessary data transfer by processing data within AWS services located in the same region.
	4) Instead of using lambda function for compression, compress the files before sending them over to S3. This will save the cost of Lambda function processing cost.
	5) If using Lambda function is a must and point 5) above isn't possible then schedule the lambda function to avoid frequent triggers and reduce number of lambda function requests per month. It should be scheduled to a sweet spot where it shouldn't jeaporadize the performance of Lmabda function by increasing the lambda function processing time.
	6) Regularly monitor our AWS usage and costs using AWS Cost Explorer or third-party tools to identify opportunities for optimization and cost savings.
	
