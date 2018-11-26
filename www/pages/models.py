from django.db import models

# Create your models here.


class Page(models.Model):
    name = models.TextField(
        name="name",
        default="UNNAMED",
        max_length=20,
        unique=True,
        help_text="Just a name for your page configuration"
    )
    url = models.TextField(
        name="url",
        max_length=1024,
        default="about:blank",
        help_text="Url for your page configuration, by default='about:blank'"
    )
    locator = models.TextField(
        name="locator",
        max_length=25,
        default="css selector",
        help_text="Selenium selectors strategy"
    )
    go_url = models.BooleanField(
        name="go_url",
        default=False,
        help_text="Allows to go to page url before load elements"
    )
    wait_url = models.IntegerField(
        name="wait_url",
        default=0,
        help_text="Wait for and url before starting to search elements"
    )
    maximize = models.BooleanField(
        name="maximize",
        default=False,
        help_text="Allows to maximize browser window"
    )

    def __str__(self):
        return self.name

class ControlInstance(models.Model):
    name = models.TextField(
        name="name",
        default="ControlBase",
        max_length=20,
        unique=True,
        help_text="Name type for this control"
    )

    def __str__(self):
        return self.name

class Control(models.Model):
    name = models.TextField(
        name="name",
        default="UNNAMED",
        max_length=20,
        unique=True,
        help_text="Just a name for your control configuration"
    )
    selector = models.TextField(
        name="selector",
        null=True,
        max_length=1024,
        help_text="Just a selector to use for obtain some web element"
    )
    instance = models.ForeignKey(ControlInstance, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
