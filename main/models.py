from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse


class UserProfile(models.Model):
    """
    Represents a single user
    Author: Aly Yakan

    """
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username


class Library(models.Model):
    """
    Represents a single Library

    Author: Aly Yakan

    """
    name = models.CharField(max_length=128, unique=True, null=False)
    location = models.CharField(max_length=128)
    owner = models.OneToOneField(User)
    slug = models.SlugField(unique=False)

    def get_absolute_url(self):
        """
        Gets absolute url of library-detail template which is used to display
        information about library entries
        Author: Aly Yakan

        """
        return reverse('library-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """
        Automatically creates a slug for each library entry saved
        Author: Aly Yakan

        """
        self.slug = slugify(self.name)
        super(Library, self).save(*args, **kwargs)


class Book(models.Model):
    name = models.CharField(max_length=128, unique=True, null=False)
    author = models.CharField(max_length=128, unique=False)
    library = models.ForeignKey(Library)
    slug = models.SlugField(unique=False)

    def get_absolute_url(self):
        """
        Gets absolute url of Book-detail template which is used to display
        information about book entries
        Author: Aly Yakan

        """
        return reverse('book-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """
        Automatically creates a slug for each book entry saved
        Author: Aly Yakan

        """
        self.slug = slugify(self.name)
        super(Book, self).save(*args, **kwargs)
