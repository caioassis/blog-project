# blog-project
Blog Project built with Django Web Framework as part of an assessment.

### Project Details 

### Specifications
- Administrators can place posts on the blog.
- A post consists of a title, author, date and content (text).
- A post can have replies, which consist of a name, e-mail address and content (text).
- Posts can only be visible when they are published.
- Both posts and replies can be removed by an administrator. Make sure this is a soft-delete and do not delete the actual data.
- Every author has it's own posts and can only create new posts and edit it's own posts.
- Only authenticated author's can access the back-end interface.
- The blog has one superuser that can manage the authors and posts (CRUD).
- Allow the superuser to log in for for changes that require authorization, create a new author (that does not have superuser rights itself), create new messages and publish them, edit and (soft-)delete posts and edit and (soft-)delete replies.

### Pages
- Home: shows a list of all published messages. Only show the title, first 300 characters of the content and the number of replies. Add a link that allows a guest to click to the detail page.
- Post detail: shows the complete content of the post including all replies. Guests can leave replies using their name and e-mail address.

### Appearance
- A post is always shown with the title first, the content below and finally the author and date.
- A reply is always shown with first the content and the author and date below.
- The form to add a reply is shown on the post detail view.
- No styling is required, but can optionally be added using Bootstrap (see additional assignment).

### Hints
- It's OK to use Django's admin interface for management.
- Replies should only be created through the front-end and do not require authentication.
- You do not have to create an Author model, Django's already facilitates this (django.contrib.auth).
- Make sure you use Django forms for validation.


### Additional assignments
- When adding a reply that doesn't pass validation, an error is shown.
- Guests can only add a reply after passing a captcha. You can use Google's reCAPTCHA for this.
- Add a RSS feed that contains the 5 latest posts.
- Add a manager/queryset method that does the filtering for (un-)published posts (if not so already).
- Add CSRF protection (if not already present).
- Allow the author to upload (and display) an image with the post.
- Use Twitter's Bootstrap to add some styling.
- Add guest reply moderation (replies must be approved before they are visible).
- Add migrations for the models.
- Add unit tests that validate the assignment. You can use a coverage tool to make sure relevant code is covered with tests. Possible tests are:
    - Test the post visibility (unpublished/published/deleted).
    - Test the sorting of posts and replies.
    - Test the sorting of items in the RSS feed.
