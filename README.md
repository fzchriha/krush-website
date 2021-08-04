# krush-website

A web application to help users better understand what their ideal romantic partner looks like based on their crush’s history

# Usage

  Visit https://kruush.herokuapp.com/ and create an account using your email or your Google account, then create your crush's profile (it will be only visible to you), based on the tags you assign to them (or as I like to call them *traits*) you can view what attracts you the most by visiting **analytics**.

# Demo

![alt text](https://github.com/fzchriha/krush-website/blob/clean_code/overview.jpeg?raw=true)

# Problems faced while building this project:

* **Visualizing Post Tags in Django**

  For more than 8 days I have been struggling to find an API, a library (anything!) to graph my user tags data.

  The problem was like this, users assign tags to their posts ( I used django-taggit for this task) then I will generate for them this beautiful graph based on their tags use. Simple right! Yet, I couldn't find a single post to help me achieve this.

  (Spoiler,I made that blog, skip the story and check the article below)
  https://medium.com/@fatimazahrachriha/combine-django-taggit-and-chartjs-85de844de30c

# Future Work:
  * **August 4, 2021** Security issues, the current application no longer supports https, it's now http which is conflicting with the Google authentification
  * Create a layout for Friends page
  * Have notifications icon pop when a user gets a new notification
  * Create a messaging system for friends
  
 
# Contribute to this project:

  * Fork this github repository
  * Clone this github repository
  
  `pip install -r requirements.txt`

