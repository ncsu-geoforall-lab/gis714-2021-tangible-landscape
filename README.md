# NCSU GIS 714 Spring 2021: Tangible Landscape

![CI](https://github.com/ncsu-geoforall-lab/gis714-2021-tangible-landscape/workflows/CI/badge.svg)

## How to add a new activity

To add a new activity to this project, you need to fork this repository, create a branch, create a pull request,
and of course develop your new activity. The following sections go over the specific steps.
A later section discusses how to modify an action later on using another pull request.

### Set up your repository

To be able to create pull request (PR), you will need to set up a fork
and a local repository on your computer
(to make changes and to test code locally):

1. Fork this repository on GitHub.
   * In the web interface, there is a *Fork* button.
1. Clone your fork on your computer.
   * For example, in the command line, use the `git clone` command:
     `git clone {url-of-the-repo}`

### Develop new analysis

1. Create a new Python script according to the template.
   * There is a template called `activity_template.py` in the `activities` directory
     which gives information about the specific conventions.
   * Use a unique filename, for example your name or your unique algorithm name.
   * You can use the Simple Python Editor in GRASS GIS
     which will make it simple to executed Python code in GRASS GIS
     without additional setup.
1. Develop a new analysis and write it as a function in the file.
1. Test your analysis locally on your computer by executing the script.
   * Use the NC SPM sample location for GRASS GIS.
   * If you are using the Simple Python Editor, just run it from there.

### Configure an activity

1. Create a new JSON configuration file according to the template.
   * There is a template called `config_template.json` in the `activities` directory
     which provides an example of a minimal activity configuration.
   * Again, use a unique filename.
1. Set value for the `analyses` key to the filename of your Python script.
1. Change `title` of the task and modify `layers` to fit your needs.

### Create a pull request

Once you have your new files ready, you can do all the Git related steps
(you could do them as your are working, too).
We will use Git in command line here and for creating the PR with GitHub web interface,
but you can use any Git desktop tool including GitHub Desktop.
(You can also do all through the GitHub web interface.
On the other hand, if you want to do everything in command line, you can add GitHub CLI to the mix.)

Create a new branch for your changes and switch to it.
Here, we will call the new branch `add-awesome-activity`.
In command line, do:

```sh
git switch -c add-awesome-activity
```

Add Python script with your Python file and your JSON file to the repository
as new files:

```sh
git add activities/awesome-activity.py
git add activities/awesome-activity.json
```

Record the changes:

```sh
git commit -am "Add awesome activity"
```

Publish the changes into your fork
(`origin` is how Git refers to the remote repository you cloned from,
`add-awesome-activity` is the name you have picked earlier for your branch):

```sh
git push origin add-awesome-activity
```

This will give your URL to create pull request on GitHub
or simply go to GitHub and it will suggest you to open a PR.

## How to modify your activity

When your PR is merged, the main, original repository is updated.
Here, we will refer to this repository as the *upstream repository*.
What was updated in the upstream repository was the `main` branch
which will be important in a moment.

Because the changes from the PR are now in the `main` branch
of the upstream repository, modifying your Tangible Landscape activity
now requires that you update your fork first.

### Update your fork

To update your fork, first, you need to add the upstream repository as another
*remote repository* to the clone on your local machine.

So, add the upstream repository as another remote repository called `upstream`.
In command line, using:

```sh
git remote add upstream https://github.com/ncsu-geoforall-lab/gis714-2021-tangible-landscape
```

Second, switch to the `main` branch of your repository
(the `main` branch should have no changes in it since you used a separate branch
to make the changes for your first PR):

```sh
git switch main
```

Third, update the `main` branch of your local repository to match
the `main` branch from the upstream repository.
This can be done with the two following commands:

```sh
git fetch upstream
git rebase upstream/main
```

Optionally, you can push the update to your fork on GitHub
(this has no effect on your later PRs):

```sh
git push
```

### Make and publish changes

Now when your local `main` branch is up to date with the `main` branch
of the upstream repository,
you can just follow the instructions above for creating a new activity,
in short, you need to:

1. create a new branch (you can do it also after you make the changes),
2. make changes,
3. make commits,
4. publish (push) the changes online, and
5. create a pull request.
