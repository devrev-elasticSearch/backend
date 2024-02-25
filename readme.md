# This backend consists of four main parts, as described in the runner.py file

## Denoiser Loop

This loop fetches raw data published to a sqs queue and filters it.
The filtering process involves translating to english, using criteria based on non english characters, spelling errors and number of words to filter the icoming data, the data is passed to another queue if it is not dropped

## DataModelCreator Loop

This loop fetches the processed reviews from 