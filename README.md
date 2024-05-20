# AWS Policy Modules

## Adding a Principal

``` 
statement_to_modify = bucket_policy.select_statement('test-bucket-policy')

new_user_arn = 'arn:aws:iam::079704260000:user/ib1234'

statement_to_modify.Principal['AWS'].append(new_user_arn)

statement_to_modify.content

{'Sid': 'test-bucket-policy', 'Effect': 'Allow', 'Principal': {'AWS': ['arn:aws:iam::079704260000:user/rg12345678', 'arn:aws:iam::079704260000:user/ib1234']}, 'Action': ['s3:GetObject', 's3:PutObject'], 'Resource': 'arn:aws:s3:::mnop1234/*'}

statement_to_modify.save()
True

statement_to_modify.source_policy.save()

{'ResponseMetadata': {'RequestId': 'TZX787KJ3SF54XJQ', 'HostId': '5ejcGDH8J/2kaDxkQoR84jSEs8j9+HsYwlKXfYrgK3Gn851A9kCobf8nvmXb06+4J171hm/BH2g=', 'HTTPStatusCode': 204, 'HTTPHeaders': {'x-amz-id-2': '5ejcGDH8J/2kaDxkQoR84jSEs8j9+HsYwlKXfYrgK3Gn851A9kCobf8nvmXb06+4J171hm/BH2g=', 'x-amz-request-id': 'TZX787KJ3SF54XJQ', 'date': 'Sun, 19 May 2024 23:50:17 GMT', 'server': 'AmazonS3'}, 'RetryAttempts': 0}}
```

## Removing a Principal from the list

As an example:

  ```
mysid = bucket_policy.select_statement('test-bucket-policy')


mysid.content
{'Sid': 'test-bucket-policy', 'Effect': 'Allow', 'Principal': {'AWS': ['arn:aws:iam::079704260000:user/ib1234', 'arn:aws:iam::079704260000:user/rg12345678', 'arn:aws:iam::079704260000:user/dsi123']}, 'Action': ['s3:GetObject', 's3:PutObject'], 'Resource': 'arn:aws:s3:::mnop1234/*'}

mysid.Principal['AWS']
['arn:aws:iam::079704260000:user/ib1234', 'arn:aws:iam::079704260000:user/rg12345678', 'arn:aws:iam::079704260000:user/ds1234']

mysid.Principal['AWS'].remove('arn:aws:iam::079704260000:user/ds1234')

mysid.Principal['AWS']
['arn:aws:iam::079704260000:user/ib1234', 'arn:aws:iam::079704260000:user/rg12345678']

mysid.save()
True


mysid.source_policy.save()
{'ResponseMetadata': {'RequestId': 'XC6Y0PPC9RN440NY', 'HostId': 'VpS1B2ikkRz/DQieNGAqLHmtP4AFfltdcW7VMG+Nu1FNQwINUM0IfpgAv9ZCMFHnj6GmL5Lv3GY=', 'HTTPStatusCode': 204, 'HTTPHeaders': {'x-amz-id-2': 'VpS1B2ikkRz/DQieNGAqLHmtP4AFfltdcW7VMG+Nu1FNQwINUM0IfpgAv9ZCMFHnj6GmL5Lv3GY=', 'x-amz-request-id': 'XC6Y0PPC9RN440NY', 'date': 'Sun, 19 May 2024 23:32:59 GMT', 'server': 'AmazonS3'}, 'RetryAttempts': 0}}
  ```

##  going from one principle to two 
or from two principals to one...

I started with a single principal... editing the policy on the console, I attempted to add [ and ] around the principle for a list of one...

after saving and going back to the editor in the console, the square brackets had been removed by AWS editor...

this is only a problem because, when trying to add the second principal, the square brackets are no longer present - what should be as simple as adding an element to a list doesn't work on this edge case...

## Items of Note

In no particular order... well, perhaps as I run into them?

- I don't know if I could 'force' this from the cli or by creating the policy documents directly (instead of using edit in the console) 
but if you have only one principal, AWS will not let you create a single element list.  I created a list (of one) saved it and 
AWS factors this out.  I need to test adding the 2nd principal to a policy where this is just one... I think it should work... but...


