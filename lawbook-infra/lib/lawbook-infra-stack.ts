import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda'
import * as fs from 'fs'
import * as dotenv from 'dotenv'

export class LawbookInfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const envConfig = dotenv.parse(fs.readFileSync(".env"));

    const LawbookDockerFunc = new lambda.DockerImageFunction(this, "LawbookDockerFunc", {
      code: lambda.DockerImageCode.fromImageAsset("../api"),
      memorySize: 1024,
      timeout: cdk.Duration.seconds(60),
      environment: envConfig,
    })

    const functionUrl = LawbookDockerFunc.addFunctionUrl({
      authType: lambda.FunctionUrlAuthType.NONE,
      cors: {
        allowedMethods: [lambda.HttpMethod.ALL],
        allowedHeaders: ["*"],
        allowedOrigins: ["*"],
      },
    })

    new cdk.CfnOutput(this, "FunctionUrlValue", {
      value: functionUrl.url,
    });
  }
}
