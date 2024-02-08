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
