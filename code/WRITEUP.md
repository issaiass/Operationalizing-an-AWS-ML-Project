#### Training and Deployment

We selected a standard instance ml.t3.xlarge 4vCPUs, 16 GiB RAM, costing $0.20/hr.

![Sagemaker Instance](doc/p1/sm_instance1.PNG "width=80%")

The reason for the decision was that we could not download and upload files from our initial ml.t3.medium due to 4Gb of data and other files there occuping space that are important and we must hold for some time.  

For our training stage we selected an accelerated computing instance of ml.g4dn.xlarge, 4vCPUs, 16 GiB RAM costing $0.736/hr. 

![Sagemaker HPO](doc/p1/sm_hpo1.PNG "width=80%")

For the deployment part we selected an ml.m5.xlarge because we do not need more computing power for the development.

![Sagemaker Endpoint](doc/p1/sm_endpoint.PNG "width=80%")

You can see more images on *doc/p1* folder.

#### EC2 Training

We selected a t2.micro free Tier AWS EC2 Deep Learning Instance because is it has PyTorch installed and we do not need to much processing power too for training.

![Sagemaker EC2 Instance](doc/p2/ec2_instance1.PNG "width=80%")

For activatting Pytorch:
    source activate pytorch
Execute the script for start downloading files, create the folder and train the model on the EC2.
    ./script.sh

![Sagemaker script](doc/p2/ec2_script.PNG "width=80%")

![Sagemaker EC2 train1](doc/p2/ec2_instance2.PNG "width=80%")

![Sagemaker EC2 train2](doc/p2/ec2_instance3.PNG "width=80%")


Main differences bewteen the file from the notebook and the file from the EC2 instance are:
 - On *hpo.py* we log the metrics, on the EC2 not.
 - On *hpo.py* we trained for 50 epochs and on the EC2 for 5.
 - On *hpo.py* we are training for the full dataset of train, on the EC2 we are just testing if it trains using the test dataset
 - Finally the main big difference is that we enter at a __main__ inside the *hpo.py* for and request for some parameters and hyperparameters and on the EC2 not, we just load directly without any configuration and a predefined batch size of 2.

#### Lambda function setup

We setup a lambda function to ensure correct response of the deployment.  

![lambda function](doc/p3/lambda1.PNG "width=80%")

As shown above we ensured that we had all correct response type information as AWS suggests for lambdas. 


#### Security and Testing

The lambda function has an event based on one of our sagemaker buckets from oue S3.

![s3 bucket image](doc/p4/lambda2.PNG "width=80%")

The lambda response is based on a probability of all the dog classes.

![lambda event](doc/p4/lambda4.PNG "width=80%")

![lambda response](doc/p4/lambda3.PNG "width=80%")

For the endpoint invocation to work, we had to enable the sagemaker role to enable calls for it.

![iam roles](doc/p4/lambda5.PNG "width=80%")

One of the potential vulnerabilities of the IAM setup is that we have full access to AWS Sagemaker and that role in particular can launch training jobs, deploy and delete models.

Another possible issue is that we have not successfully configured correctly the specific rules to use the VPC setup for our own uses.

#### Concurrency and auto-scaling

One way to improve response time with traffic is to use autoscaling and concurrency.  

*Autoscaling* allows deployed enpoints to respond to multiple request simultaneously. We can set the maximum instance count, scale-in cool down and scale-out cool down that are the times it delays to deploy or delete those deploys.

![Autoscale For Endpoints](doc/p5/autoscale1.PNG "width=80%")

We can modify the instance count for autoscaling

![Autoscale For Instances](doc/p5/autoscale2.PNG "width=80%")

We could also ensure correct configuration of varying instance cound and the cool down in and out with the specified times.

![Autoscale For Variants](doc/p5/autoscale3.PNG "width=80%")


*Concurrency* are for lambda functions, because lambda functions process one (1) request at time, in high traffic data streams, the latency increases and we must implement this feature.  

![Concurrency](doc/p5/concurrency_configuration.PNG "width=80%")

- If the traffic is low there is no need to concurrency.  
- If you implement concurrency you have to decide to implement of *reserved concurrency* 
  - Lower cost
  - Hard maximum (it can be divided the workload between deployed endpoints)
  - The disadvantage of this approach is that if the hard maximun is reached you will experienc latency.  
- The other type of concurrency is *provisioned concurrency*
  - This covers all the disadvantages of the *reserved concurrency* but
  - Has a higher cost at a flexible maximum.  
  - This can achieve very low traffic latency on any scenario.

For concurrency of our lambda function we could first make a version of the $LATEST lambda.

![Concurrency Version](doc/p5/concurrency_version.PNG "width=80%")

Depending of the demand we could set the:

Provisioned Concurrency
![Provisioned Concurrency](doc/p5/provisioned_concurrency.PNG "width=80%")

or

Reserved Concurrency
![Reserved Concurrency](doc/p5/reserved_concurrency.PNG "width=80%")