TODO

I. check work for setup (same as collection)

II. run in docker container

- copy secrets folder here
- create secrets/data-labeling.env; fill out all 4 vars
- run label studio container

```shell
# Create the network if we don't have it yet
docker network inspect hisolver-data-labeling-network >/dev/null 2>&1 || docker network create hisolver-data-labeling-network

# Build the image based on the Dockerfile
docker build -t hisolver-data-label-cli --platform=linux/arm64/v8 -f Dockerfile .

# Run All Containers
docker-compose run --rm --service-ports hisolver-data-label-cli
```

- this should bring up a shell prompt from the running container
- set up label studio in UI
  - NOTE: safari will not work properly when displaying tasks... use Chrome!!!!!!!!!!
  - create annotation project
    - log in with credentials specified env file
    - create project, give it a name: HiSolver Manim Animation Labeling
    - Skip `Data Import` tab and go to `Labeling Setup`
    - select template: Natural Language Processing -> Text Summarization
    - should i configure data??? (FIXME) (might need to specify prompt for user task?)
    - oh yeah... Labeling interface should be configured... with custom html
  - configure cloud storage
    - setting - storage
    - add source storage
      - storage type: GCS
      - Manim Code Snippets, hisolver-data-collection [specific], processed, .\*
      - uncheck both
      - Sync Storage
    - Add Target Storage
      - Manim Code Snippets, hisolver-data-collection, labeled
- enable cors back in shell
- use label studio to annotate manim code snippets

- labeling interface UI:

```
<View style="white-space: pre;">
  <Header value="Read this piece of Manim code"/>
  <Text name="text" value="$code"/>
  <Header value="Provide a one sentence summary of what it does"/>
  <TextArea name="answer" toName="text" showSubmitButton="true" maxSubmissions="1" editable="true" required="true"/>
</View>
```
