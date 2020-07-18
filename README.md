# Note:

- You can access the website at this [link](https://mysuperdjangoapp.herokuapp.com/)

# Outline:

- The project is a Django based blog website where users can register accounts, add, edit and delete blog posts, manage their profile, search for specific posts etc! It follows a clean and minimal look achieved from using Bootstrap and CSS. The files are handled by AWS and the website has been deployed using Heroku. A more detailed description lies below.

# Purpose:

- The backend of web development has always fascinated me and since I am extremely familiar with python, I thought I could try out Django and ultimately learn how to be a full-stack developer. Following along Corey Schafer's wonderful Django tutorial series, that can be found [here,](https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p) I built this blog application - adding in my own features such as a search bar, a 'Feeling Lucky' sidebar, footers etc.
- These additions helped me understand the framework a lot better as they forced me to sift through the documentation and scour stackoverflow for certain errors. I thoroughly enjoyed using Django and will be making a lot more database centric websites soon.

# Description:

- UPDATE: Since deploying the website, I felt that it was desperately missing a dark mode option - and so using localStorage and some basic JS, I added a toggle option where the user can choose which mode they would want to use and it reflects in all the different pages!
- This blog website houses 2 main apps - blog and users.
- The blog app is used to control the posts and the process of adding, updating and deleting posts based on Django's MVT framework.
- The templates extend on a base template and use the inbuilt class-based views in order to achieve their purpose - mostly by overloading the get_query and get_context_data methods.
- The crispy form module is also used in order to beautify the forms and maintain the aesthetic across the website.
- The users app handles the profiles, login, logout etc using the inbuilt user model and creating a new profile model which accepts the user profile picture.
- Moreover, django-storages and boto3 are used to set-up the AWS S3 portion of the profiles and the heroku deployment is made a lot easier by watching [this video](https://www.youtube.com/watch?v=6DI_7Zja8Zc) by Corey Schafer!
