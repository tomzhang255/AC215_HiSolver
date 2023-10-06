# Data Versioning

This project has 3 data components: scraping and storing data from GitHub repositories, preprocessing the scraped data and storing it into a seperate folder, and creating and storing training data prompts. This document details our data versioning approach for each step to ensure reproducibility and traceability.

## I. Check work

Make sure you've followed all the steps from the data collection section `src/collection/README.md`.

## II. Create a Data Store folder in GCS Bucket

1. Go to https://console.cloud.google.com/storage/browser

2. Go to the bucket hisolver-data-collection-2 (change to your bucketname)

3. Create a folder dvc_store inside the bucket


## III. Set up Objection Versioning in GCS 

1. Navigate to Google Cloud Storage.

2. Access the "Buckets" section.

3. Locate and select your specific bucket.

4. Under "Protections", find the "Object Versioning" option.

5. Turn on Object Versioning to enable data recovery features.

6. Confirm the setup by selecting "Set".


## III. Set up DVC remote for git to track

Add your DVC remote - It's crucial to have your unique remote to avoid conflicts with others, given we 
are working with diffrent buckets, we need seperate remotes for git to be able to different the buckets
we are dvc pushing to

```shell
dvc remote add -d {NAME}_remote gs://{YOUR-BUCK-PATH}/dvc_store
```

Commit the .dvc directory to Git
```shell
git add .dvc
git commit -m "adding my remote dvc"
git push origin branch_name
```

## IV. GCS Object Versioning vs DVC 

In our project we will be using both GCS object versioning functionality and the DVC module. 

### 1. Scraping GitHub Data
We stream data directly from GitHub repositories to our designated Google Cloud Storage (GCS) bucket. As our approach focuses solely on adding new observations without altering existing data, we've opted not to implement a DVC pipeline for this step due to the associated operational overhead. This would necessitate downloading data locally, committing to .dvc, and letting git track the .dvc file or managing the process via a cloud virtual machine. Given these constraints and evaluating the utility we 
decided to use GCS object version functionality. 

### 2. Preprocessing Scraped Data
For the preprocessing stage, we download the scraped data files to a temporary local directory. Given that we're making changes to these files before uploading them back to our storage solution, we've incorporated Data Version Control (DVC) to monitor and version these modifications. By doing so, we ensure a clear lineage of our data transformations and can easily revert to previous versions if needed. 

### 3. Training Data Prompts
The creation of training data prompts is executed on our local machines. As we iterate, refine, and expand this dataset, it's essential to keep track of the various versions. Therefore, we're also using DVC for version control in this step. DVC assists us in capturing each change, understanding its context, and providing a mechanism to revert or branch out from any point in the dataset's history.

### Note:

For 2 and 3, the docker files will automatically track and add these changes to the dvc_store and the git repo. If the team member needs to manually change the data, and they can track these changes while inside the container by following these steps:

#### 1. Verify DVC Remote Configuration:
Before making any changes, ensure that you DVC remote points to your designated GCS bucket.

```shell
dvc remote list
```

This will display the list of configured remotes. Ensure the URL corresponds to your GCS bucket.

#### 2. Track Data Changes with DVC:
If you've made changes to the data in data_repo/ or added new data, track it using:

```shell
dvc add data_repo/
dvc push
```

#### 3. Commit Changes to Git:
After tracking data with DVC, you'll notice a .dvc file (e.g., new_data.dvc) reflecting the changes. Commit this to the Git repository:

```shell
git add new_data.dvc
git commit -m "Track data_repo with DVC."
```

#### 4. Push to Git Remote:
Finally, push your changes to the designated Git branch:

```shell
git push origin <branch_name>
```