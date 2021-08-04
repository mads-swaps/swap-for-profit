# mads-simulate-app

Model files are loaded from EFS.  To put files in EFS, first upload to S3 `model-assets-auto-sync` bucket, then run the `S3 to EFS model asset sync` task in AWS DataSync.

Should be able to put stuff in EFS directly without having to reload the Lambda docker image, as the controls are now done via DB configuration and loaded dynamically from EFS.

Simulations are configured directly in the database.

Create relevant Strategy and Environment entries, then create the Simulation entry.