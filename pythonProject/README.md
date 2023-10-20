gcloud builds submit --tag gcr.io/tfgtwitter/tfg-example  --project=tfgtwitter

gcloud run deploy --image gcr.io/tfgtwitter/tfg-example --platform managed  
--project=tfgtwitter --allow-unauthenticated