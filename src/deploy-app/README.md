# Deploy App to GCP

## I. Prep

1. grant permissions to the service account you've been using in the IAM tab of GCP console:

- Compute Admin
- Compute OS Login
- Container Registry Service Agent
- Kubernetes Engine Admin
- Service Account User
- Storage Admin
- Storage Object Viewer

2. set up docker container: run docker-shell.sh

```shell
./docker-shell.sh
```

Execute everything after this in the docker container shell prompt...

3. Configuring OS Login for service account

```shell
gcloud compute project-info add-metadata --project $(cat /secrets/gcp_project_id.txt) --metadata enable-oslogin=TRUE
```

4. Create SSH key for service account

```shell
cd /secrets
ssh-keygen -f ssh-key-deployment
cd /app
```

5. Providing public SSH keys to instances

```shell
gcloud compute os-login ssh-keys add --key-file=/secrets/ssh-key-deployment.pub
```

Note the field "username" in the output of the command above; this is your ansible username.

6. edit inventory.yml

- ansible_user
- gcp_service_account_email
- gcp_project

7. Build and Push Docker Containers to GCR (Google Container Registry)

```shell
ansible-playbook deploy-docker-images.yml -i inventory.yml
```

## II. Without Kubernetes

1. Create Compute Instance (VM) Server in GCP

```shell
ansible-playbook deploy-create-instance.yml -i inventory.yml --extra-vars cluster_state=present
```

Once the command runs successfully get the IP address of the compute instance from GCP Console (Compute Engine -> VM instances) and update the `appserver > hosts` in inventory.yml file

2. Provision Compute Instance in GCP

Install and setup all the required things for deployment.

```shell
ansible-playbook deploy-provision-instance.yml -i inventory.yml
```

3. Setup Docker Containers in the Compute Instance

```shell
ansible-playbook deploy-setup-containers.yml -i inventory.yml
```

You can SSH into the server from the GCP console and see status of containers

```shell
sudo docker container ls
sudo docker container logs api-service -f
```

To get into a container run:

```shell
sudo docker exec -it api-service /bin/bash
```

4. Setup Webserver on the Compute Instance

```shell
ansible-playbook deploy-setup-webserver.yml -i inventory.yml
```

Once the command runs go to `http://<External IP>/`

5. [Optional] Delete the Compute Instance / Persistent disk

```shell
ansible-playbook deploy-create-instance.yml -i inventory.yml --extra-vars cluster_state=absent
```

## III. With Kubernetes

1. Enable these API's on GCP console

- Compute Engine API
- Service Usage API
- Cloud Resource Manager API
- Google Container Registry API
- Kubernetes Engine API

2. Follow all the steps in **I. Prep**

3. Edit GCS_BUCKET_NAME field in deploy-k8s-cluster.yml to match the bucket name you've been using

4. Create & deploy cluster

```shell
ansible-playbook deploy-k8s-cluster.yml -i inventory.yml --extra-vars cluster_state=present
```

5. View the app:

- Copy the nginx_ingress_ip from the terminal from the create cluster command
- Go to http://<YOUR INGRESS IP>.sslip.io

6. [Optional] Manage on GCP console: Kubernetes Engine -> Clusters

7. [Optional] Delete the cluster

```shell
ansible-playbook deploy-k8s-cluster.yml -i inventory.yml --extra-vars cluster_state=absent
```
