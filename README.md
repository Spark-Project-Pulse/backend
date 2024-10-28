# Pulse (Backend)

<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Spark-Project-Pulse/backend">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Pulse</h3>

  <p align="center">
    [Description goes here]
    <br />
    <a href="https://github.com/Spark-Project-Pulse/backend"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Spark-Project-Pulse/backend">View Demo</a>
    ·
    <a href="https://github.com/Spark-Project-Pulse/backend/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/Spark-Project-Pulse/backend/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Here's a blank template to get started: To avoid retyping too much info. Do a search and replace with your text editor for the following: `github_username`, `repo_name`, `twitter_handle`, `linkedin_username`, `email_client`, `email`, `project_title`, `project_description`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Next][Django]][Django-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

* pip

  ```sh
   python -m pip install --upgrade pip
  ```

### Installation

1. Clone the repo

   ```sh
   git clone https://github.com/Spark-Project-Pulse/backend.git

### Secret Management

#### Accessing Secrets locally

1. Go to the Google Cloud Console, navigate to `IAM & Admin` > `Service Accounts`, and and download the already existing json key from the service acount called Secret Accessor Service Account. Go to the `Keys` tab and click `Add Key` then `Create New Key` then `Create` (use json format). Your key will download as `pulse-random-letters-and-numbers.json` in the root of the project.
2. Add a `.env.local` file to the root of the project with the following contents:

``` bash
GOOGLE_CLOUD_PROJECT=google_cloud_project_id
GOOGLE_APPLICATION_CREDENTIALS=pulse-random-letters-and-numbers.json
```

3. Use the `get_secret` function in `services/secret_manager.py` to access secrets stored in Google Secret Manager locally. The function takes the secret name as an argument and returns the secret value.

#### Updating Secrets

To ensure they will be available in production and consistent across all environments and between developers, secrets should be stored in Google Secret Manager. To update a secret:

1. Navigate to the Google Cloud Console
2. Select the project `Pulse`
3. Navigate to `Secret Manager`
4. Select the secret you want to update
5. Click `Delete` to delete the secret
6. Now recreate the secret with the new value (I am aware this is kind of a pain, but I haven't researched how versions work yet)

#### Creating New Secrets

For the frontend, there are three kinds of secrets: local, local docker, and  production. When creating a new secret, make sure to add the local version by appending `_LOCAL`, the local docker version by append `_LOCAL_DOCKER` to the secret name, and the production version by appending `_PRODUCTION` to the secret name. Even if the secret is the same for all environments, it should be added for each environment to ensure that the secret is available in all environments. The get_secret function handles the logic of which secret to return based on the environment, so after adding the secret to Google Secret Manager, it should be accessible via the function.

#### Steps for creating a new secret via the Google Cloud Console UI

1. Navigate to the Google Cloud Console
2. Select the project `Pulse`
3. Navigate to `Secret Manager`
4. Select the secret you want to update
5. Click `Create Secret`
6. Enter the secret's name and value
7. Click `Create Secret`

### Run locally

#### Prequisites

In order to run the backend locally, you must ensure that you have installed the Supabase CLI and started the database:

1. Install [Supabase CLI](https://supabase.com/docs/guides/cli/getting-started)
2. Make sure the Docker daemon is running (open Docker Desktop)
3. Start supabase db

   ``` bash
   supabase start
   ```

4. Proceed to running the backend (note that all db updates will only be saved on your machine)
5. Stop supabase when finished

   ``` bash
   supabase stop
   ```

#### Docker

##### Running the backend

1. Make sure the Docker daemon is running (open Docker Desktop)
2. Navigate to the backend repository
3. Use this command to build and run the backend container:

   ``` bash
   docker compose up --build
   ```

4. Navigate to `http://localhost:8000/questions/getAll` to see an example of an API response

##### Running the frontend & backend in one command

1. Make sure the Docker daemon is running (open Docker Desktop)
2. Navigate to the backend repository
3. Make sure the backend repository is in the same directory as the frontend repository
4. Use this command to run the project locally:

   ``` bash
   docker compose --profile frontend-and-backend up --build
   ```

5. This will run the frontend and backend in separate containers

#### Django

1. **Install Pipenv** (if not already installed):

   ```bash
   pip install pipenv
2. Install the project dependencies using Pipenv:

   ``` bash
   pipenv install --dev
   ```

3. Activate the Pipenv virtual environment:

   ``` bash
   pipenv shell
   ```

4. Run the Django development server locally:

   ``` bash
   python manage.py runserver
   ```

### Working with the database

This project uses a combination of `Django`'s built in **ORM** and `supabase` to store/edit data. In order to **edit/add/remove** any database tables, be sure to follow these steps:

1. Make needed changes to `pulse/models.py`
2. Stage the migrations:

   ``` bash
   python manage.py makemigrations
   ```

3. Execute the migrations (**DISCLAIMER:** this will NOT apply changes directly to the hosted database, they will only be applied locally, and will take effect in the hosted database when your PR is merged into `main`)

   ``` bash
   python manage.py migrate
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

* [ ] Feature 1
* [ ] Feature 2
* [ ] Feature 3
  * [ ] Nested Feature

See the [open issues](https://github.com/Spark-Project-Pulse/backend/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors

<a href="https://github.com/Spark-Project-Pulse/backend/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Spark-Project-Pulse/backend" alt="contrib.rocks image" />
</a>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - <email@email_client.com>

Project Link: [https://github.com/Spark-Project-Pulse/backend](https://github.com/Spark-Project-Pulse/backend)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Spark-Project-Pulse/backend.svg?style=for-the-badge
[contributors-url]: https://github.com/Spark-Project-Pulse/backend/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Spark-Project-Pulse/backend.svg?style=for-the-badge
[forks-url]: https://github.com/Spark-Project-Pulse/backend/network/members
[stars-shield]: https://img.shields.io/github/stars/Spark-Project-Pulse/backend.svg?style=for-the-badge
[stars-url]: https://github.com/Spark-Project-Pulse/backend/stargazers
[issues-shield]: https://img.shields.io/github/issues/Spark-Project-Pulse/backend.svg?style=for-the-badge
[issues-url]: https://github.com/Spark-Project-Pulse/backend/issues
[license-shield]: https://img.shields.io/github/license/Spark-Project-Pulse/backend.svg?style=for-the-badge
[license-url]: https://github.com/Spark-Project-Pulse/backend/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.png
[Django]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green
[Django-url]: https://www.djangoproject.com/
