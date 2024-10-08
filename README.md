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

### Secret Management (This section is in progress, please ignore for now. It got merged with another fix)
#### Accessing Secrets locally
1. Add a `.env.local` file to the root of the project with the following contents:
``` bash
GOOGLE_CLOUD_PROJECT=your_google_client_id
GCP_SERVICE_ACCOUNT_KEY=your_gcp_service_account
```
2. Download the service account key from Google Cloud Console and save it as `service-account-key.json` in the root of the project. Go to the Google Cloud Console, navigate to `IAM & Admin` > `Service Accounts`, and create a new service account. Download the key and save it as `service-account-key.json` in the root of the project.
3. Use the get_secret function in `pulse/utils.py` to access secrets stored in Google Secret Manager. The function takes the secret name as an argument and returns the secret value.

#### Updating Secrets
To ensure they will be available in production and consistent across all environments and between developers, secrets should be stored in Google Secret Manager. To update a secret:
1. Navigate to the Google Cloud Console
2. Select the project `spark-project-pulse`
3. Navigate to `Secret Manager`
4. Select the secret you want to update
5. Click `Edit`
6. Update the secret value

### Run locally

#### Docker 
##### Running the backend
1. Make sure the Docker daemon is running (open Docker Desktop)
2. Navigate to the backend repository
3. Use this command to build and run the backend container:
   ``` bash
   docker compose up --build
   ```
4. Navigate to `http://localhost:8080/questions/getAll` to see an example of an API response

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
3. Execute the migrations (**DISCLAIMER:** this will apply changes directly to the hosted database, make sure the changes are correct)
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

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

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

### Top contributors:

<a href="https://github.com/Spark-Project-Pulse/backend/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Spark-Project-Pulse/backend" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com

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
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Django]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green
[Django-url]: https://www.djangoproject.com/