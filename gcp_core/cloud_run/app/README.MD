## Deploy to cloud Run

```bash
gcloud run deploy api-flask \
--source . \
--region europe-west1 \
--platform managed \
--allow-unauthenticated \
--memory 512Mi \
--cpu 1 \
--min-instances 0 \
--max-instances 10
```
