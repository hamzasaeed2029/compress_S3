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

