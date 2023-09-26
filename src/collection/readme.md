# Data Collection

## I. Set up a GCP service account [One time]

1. Go to the console: https://console.cloud.google.com
2. From the sidebar, select `IAM & Admin` -> `Service Accounts`
3. From the navbar, either select an existing project or create a new one
4. Back to the `Service Accounts` page, click on `Create Service Account`
5. Give it a name: `hisolver-data-collection`
6. Use default settings
7. Once you've created the service account, open it, go to the `KEYS` tab, create a new key of the JSON type.
8. Download the JSON file, rename it to `hisolver-data-collection-secrets.json`
9. Move it to this location of the repo: `src/collection/secrets/` (you might need to create a `secrets` folder)

## II. Set up a GCP cloud storage bucket [One time]

1. Go to the console: https://console.cloud.google.com
2. From the sidebar, select `Cloud Storage` -> `Buckets`
3. Make sure to select the project you just created a service account for
4. On the `Buckets` page, click `Create`
5. Name the bucket `hisolver-data-collection`; if the name's taken, just add a `-1` or something
6. Use default settings
7. Finish creating the bucket
8. Copy the name of your bucket and paste it in a file called `gcs_bucket_name.txt`; the file should live in the previous `secrets` folder; make sure the file exists within this path of the repo: `src/collection/secrets/gcs_bucket_name.txt`
9. Go back to `Service Accounts` page, open up the service account you just created (you named it `hisolver-data-collection`)
10. Under the `DETAILS` tab, find the service account's email. It should look something like `hisolver-data-collection@[your-project-name].iam.gserviceaccount.com`. Copy the email.
11. Go back to `Buckets` page, find the bucket you just created (you named it `hisolver-data-collection`)
12. Go to the `PERMISSIONS` tab
13. Select `VIEW BY PRINCIPALS` -> `GRANT ACCESS`
14. Paste the service account email you just copied to the `New principals` field
15. In the `Assign roles` section, select a role `Cloud Storage` -> `Storage Admin`. This should give your service account full access to the bucket.

## III. Set up a GitHub Personal Access Token (PAT) [One time]

1. Go to your settings page of [GitHub](https://github.com), look for `Developer settings` on the sidebar
2. Select `Personal access tokens` -> `Tokens (classic)` (following this link should also bring you to this page: https://github.com/settings/tokens)
3. Select `Generate new token` -> `Generate new token (classic)`
4. Give it any name; set expiration to "No expiration"; generate token
5. Make sure to copy the token string immediately; this is the only time you'll see it
6. Paste it in a file named `pat.txt` in the previous `secrets` folder (make sure the file lives in `src/collection/secrets/path.txt` within the repo)

## IV. Run data collection script in a docker contianer

1. Traverse to the correct directory: `src/collection/`

2. Remove all containers built from this image if such containers exist

`docker ps -a --filter "ancestor=github-scraper" -q | xargs docker stop && docker ps -a --filter "ancestor=github-scraper" -q | xargs docker rm`

3. Remove image if it exists

`docker images | grep -q "github-scraper" && docker rmi github-scraper`

4. Build docker image

`docker build -t github-scraper .`

5. Run collection script in container

`docker run -v ./secrets/hisolver-data-collection-secrets.json:/secrets/service-account-key.json -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/service-account-key.json -e GITHUB_PAT=$(cat secrets/pat.txt) github-scraper -e GCS_BUCKET_NAME=$(cat secrets/gcs_bucket_name.txt)`

6. The collection script should be running; if you go to your bucket page again on GCP, you should see the bucket being populated with scraped python files

7. In case you need to rebuild the container, just rerun steps 2-4
