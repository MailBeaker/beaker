
from django.db import models

from base.models import RandomIDModel


class Organization(RandomIDModel):
    """
    Represents an entire organization.  An organization can manage multiple domains under
    a single entity.
    """
    name = models.CharField(max_length=512)
    address_1 = models.CharField(max_length=512)
    address_2 = models.CharField(max_length=512, blank=True, default='', null=True)
    city = models.CharField(max_length=512)
    state = models.CharField(max_length=512)
    zip = models.CharField(max_length=512)
    phone = models.CharField(max_length=512)

    def __str__(self):
        return '%s' % (self.name)


class Domain(RandomIDModel):
    """
    Represents a single domain.  This correlates to the Google domain that we will check
    emails for.
    """
    domain_name = models.CharField(max_length=512)
    organization = models.ForeignKey('Organization')

    # True if whitelisted, False if blacklisted
    whitelisted = models.BooleanField(default=False)

    @classmethod
    def get_by_domain_name(cls, domain_name):
        return cls.objects.get(domain_name=domain_name)

    def get_whitelist(self):
        """
        Gets all of the users that are whitelisted for the domain.

        If the domain isn't currently set to whitelisted, returns None.
        """
        if not self.whitelisted:
            return []

        from authentication.models import EmailMeta
        return EmailMeta.objects.filter(domain=self).filter(whitelisted=True)

    def get_blacklist(self):
        """
        Gets all of the users that are blacklisted for the domain.

        If the domain isn't currently set to blacklisted, returns None.
        """
        if self.whitelisted:
            return []

        from authentication.models import EmailMeta
        return EmailMeta.objects.filter(domain=self).filter(blacklisted=True)

    def __str__(self):
        return '%s' % (self.domain_name)


class Rule(RandomIDModel):
    """
    Represents an rule that an account administrator creates in order to match incoming
    email against.  This gives adminsitrators the ability to block links based on custom
    rules that they create.

    actions
        0 = Pass
        1 = Warn
        2 = Block

    mods
        0 = Ignore this field for this rule
        1 = Equals the value
        2 = Does not equal the value
        3 = Contains the value
        4 = Does not contain the value
        5 = Starts with the value
        6 = Ends with the value
    """

    domain = models.ForeignKey('Domain')

    description = models.CharField(max_length=512)
    alert_admins = models.BooleanField(default=False)

    action = models.IntegerField(
        help_text="0 = pass, 1 = warn, 2 = block"
    )

    sender_mod = models.IntegerField()
    sender_value = models.CharField(
        max_length=512,
        blank=True,
        help_text="0 = ignore, 1 = equals, 2 = DNE, 3 = contains, 4 = does not contain, 5 = starts with, 6 = ends with"
    )

    receiver_mod = models.IntegerField()
    receiver_value = models.CharField(max_length=512, blank=True)

    subject_mod = models.IntegerField()
    subject_value = models.CharField(max_length=512, blank=True)

    url_mod = models.IntegerField()
    url_value = models.CharField(max_length=512, blank=True)

    body_mod = models.IntegerField()
    body_value = models.CharField(max_length=512, blank=True)

    def __str__(self):
        return '%s' % (self.description)


class Message(RandomIDModel):
    """
    Represents a single email message.
    """
    domain = models.ForeignKey('Domain')
    message_from_address = models.CharField(max_length=512, default='')
    envelope_from_address = models.CharField(max_length=512, default='')
    rcpt_to_address = models.CharField(max_length=512, default='')
    service_name = models.CharField(max_length=512, default='')
    service_message_id = models.CharField(max_length=512, default='')
    authentication_results = models.TextField(null=True, blank=True)
    dmarc_result = models.CharField(max_length=512, null=True, blank=True)
    dkim_result = models.CharField(max_length=512, null=True, blank=True)
    spf_result = models.CharField(max_length=512, null=True, blank=True)


class Link(RandomIDModel):
    """
    Represents a single link in an email.
    """

    domain = models.ForeignKey('Domain')
    message = models.ForeignKey('Message')

    redirect_url = models.TextField()
    scheme = models.TextField(blank=True, null=True)
    netloc = models.TextField(blank=True, null=True)
    path = models.TextField(blank=True, null=True)
    params = models.TextField(blank=True, null=True)
    query = models.TextField(blank=True, null=True)
    fragment = models.TextField(blank=True, null=True)
    username = models.TextField(blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    hostname = models.TextField(blank=True, null=True)
    port = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s' % (self.redirect_url)

    def get_matched_rules(self):
        return RuleMatch.get_rules_by_link(self)


class Attachment(RandomIDModel):
    """
    Represents a single attachment in an email.
    """

    domain = models.ForeignKey('Domain')
    message = models.ForeignKey('Message')

    hash = models.TextField()
    name = models.TextField()
    size = models.IntegerField()

    def __str__(self):
        return '%s' % (self.name)


class RuleMatch(models.Model):
    """
    Matches a Link object to a Rule object that matches it.
    """

    link = models.ForeignKey('Link')
    rule = models.ForeignKey('Rule')

    @classmethod
    def get_rules_by_link(cls, link):
        return [x.rule for x in cls.objects.filter(link=link)]
