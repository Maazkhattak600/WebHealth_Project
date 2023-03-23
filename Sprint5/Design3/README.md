
# Welcome to Design-3!

## Problem Statement :
 1) How would you automate deployment (e-g on AWS) for a system that has 
  (i)  source code in a repo.
  ii)  How do we generate an artifact from the repo that gets published and later is used in some services?
  iii) Are there more than one solutions?

 2) Design: Deploy, maintain and rollback pipeline for an artifact deployment e-g lambda package, docker image etc.
       i)If the latest deployment is failing, why do you think that is?
       ii) How will you rollback?
       iii)How do you reduce such failures so there is less need to rollback?

## Answers:

### (1) (i)
To automate a deployment for a system having a source code in repo can be done by AWS Codepipeline. Actually, Aws Codepipelie orchestrates the whole process which takes the code from GitHub repo, builds it on the build servers and then deploy it using deployment groups on different Application servers.

![Code_1](https://user-images.githubusercontent.com/112099093/207010694-779dee39-1424-4502-b61b-89c7a8842528.png)

### (1) (ii)
CodePipeline automatically generates this S3 bucket in the AWS region. It stores artifacts for all pipelines in that region in this bucket.
At the first stage in its workflow, CodePipeline obtains source code, configuration, data, and other resources from a source provider.
It stores a zipped version of the artifacts in the Artifact Store.

### (1) (iii)

Yes , there are more than one solution.

There are many tools available that can help automate the deployment process. Some popular examples include Jenkins, Travis CI, and DeployBot. These tools can handle tasks such as building and testing code, managing infrastructure, and deploying applications.

Configuration management tools such as Ansible, Chef, and Puppet can be used to automate the deployment of applications and infrastructure. These tools allow you to define your infrastructure as code, which can then be versioned and deployed automatically.


### (2) (i)
If the latest deployment is failing, there could be a number of reasons for this. Some possible causes could include:

1) The artifact is not compatible with the target environment
2) There are bugs or issues in the code that are causing the deployment to fail
3) There are issues with the configuration of the deployment environment
4) There are network or connectivity issues preventing the deployment from completing
5) The artifact is too large to be deployed within the allotted time

### (2) (ii)

There are several steps that can be taken to rollback an artifact deployment:

1) Identify the previous version of the artifact that you want to rollback to. This could be a specific version number, commit ID, or timestamp.

2) Depending on the tool being used, you may need to manually trigger the rollback process. For example, in AWS CodePipeline, you can use the "Rerun" action to deploy a previous version of an artifact.

3) If the rollback process involves replacing the current version of the artifact with a previous version, you will need to ensure that any necessary resources are available to support the rollback. For example, if you are rolling back a Docker image, you will need to ensure that there is enough space in the container to accommodate the previous image.

4) Monitor the rollback process to ensure that it is successful and that the previous version of the artifact is functioning as expected.

5) If the rollback process is not successful, you may need to debug the issue and take corrective action. This could involve reviewing logs and monitoring data, as well as comparing the current deployment with previous deployments to identify any differences that could be causing the failure.

### (2) (iii)

There are several steps that can be taken to reduce the need for rollbacks in an artifact deployment pipeline:

1) Implement robust testing practices: Make sure to test the artifact thoroughly before deploying it to production. This could include unit tests, integration tests, and end-to-end tests to ensure that the artifact is functioning as expected.

2) Use staging environments: Set up a staging environment where you can test the artifact before deploying it to production. This can help identify any issues before the artifact is deployed to production, reducing the risk of a deployment failure.

3) Monitor the deployment: Use monitoring tools to track the performance of the artifact in production. This can help identify any issues as soon as they arise, allowing you to take corrective action before the issue becomes a problem.

4) Use a canary deployment strategy: With a canary deployment, you can test a new version of the artifact in a small portion of your production environment before rolling it out to the entire environment. This can help identify any issues with the new version before it is deployed to the entire environment, reducing the risk of a rollback.

5) Use feature flags: Use feature flags to roll out new features gradually, allowing you to test them in production before making them available to all users. This can help identify any issues with the new feature before it is fully rolled out, reducing the risk of a rollback.

6) By implementing these practices, you can reduce the risk of deployment failures and minimize the need for rollbacks in your artifact deployment pipeline.

