# Fivetran - AWS Lambda function for Retently

## Purpose
At the time this code was written, Fivetran did not support [Retently](https://www.retently.com) through a native connector.

This Python code was written to extract responses from NPS campaigns, and replicate them to a data warehouse through a [Fivetran cloud function](https://fivetran.com/docs/functions/aws-lambda).

## Requirements
This is meant to be hosted on AWS Lambda and to be orchestrated by Fivetran.

## Notes
This code is shared as an example of a cloud function for Fivetran. It has worked for us without issues, but it's probably not perfect, it is not actively maintained, and no support is offered.

You may use this at your own risk.