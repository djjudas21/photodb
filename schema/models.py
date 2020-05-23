from datetime import datetime
from math import sqrt
import re
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.urls import reverse
from djmoney.models.fields import MoneyField
from djchoices import DjangoChoices, ChoiceItem
from django_currentuser.db.models import CurrentUserField
from autosequence.fields import AutoSequenceField
from slugify import Slugify, UniqueSlugify
from taggit.managers import TaggableManager


def cameramodel_check(text, uids):
    if text in uids:
        return False
    return not CameraModel.objects.filter(slug=text).exists()


def lensmodel_check(text, uids):
    if text in uids:
        return False
    return not LensModel.objects.filter(slug=text).exists()


def toner_check(text, uids):
    if text in uids:
        return False
    return not Toner.objects.filter(slug=text).exists()


def filmstock_check(text, uids):
    if text in uids:
        return False
    return not FilmStock.objects.filter(slug=text).exists()


def developer_check(text, uids):
    if text in uids:
        return False
    return not Developer.objects.filter(slug=text).exists()

# Create your models here.


class Manufacturer(models.Model):
    name = models.CharField(
        help_text='Name of the manufacturer', max_length=45, blank=True, unique=True)
    city = models.CharField(
        help_text='City in which the manufacturer is based', max_length=45, blank=True, null=True)
    country = models.CharField(
        help_text='Country in which the manufacturer is based', max_length=45, blank=True, null=True)
    url = models.URLField(
        verbose_name='URL', help_text='URL to the manufacturers main website', max_length=45, blank=True, null=True)
    founded = models.PositiveIntegerField(
        help_text='Year in which the manufacturer was founded', blank=True, null=True)
    dissolved = models.PositiveIntegerField(
        help_text='Year in which the manufacturer was dissolved', blank=True, null=True)
    slug = models.SlugField(editable=False, null=True, unique=True)
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, editable=False)
    created_by = CurrentUserField(
        editable=False, related_name='manufacturer_created_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, editable=False)
    updated_by = CurrentUserField(
        on_update=True, editable=False, related_name='manufacturer_updated_by')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "manufacturers"

    def save(self, *args, **kwargs):
        custom_slugify_unique = Slugify(to_lower=True)
        self.slug = custom_slugify_unique(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        # City/country
        if self.country is None and self.city is not None:
            raise ValidationError({
                'country': ValidationError(('Must specify country if city is given')),
            })
        # Founded/dissolved
        if self.founded is not None and self.dissolved is not None and self.founded > self.dissolved:
            raise ValidationError({
                'founded': ValidationError(('Founded date must be earlier than dissolved date')),
                'dissolved': ValidationError(('Dissolved date must be later than founded date')),
            })
        if self.founded is not None and self.founded > datetime.now().year:
            raise ValidationError({
                'founded': ValidationError(('Founded date must be in the past')),
            })
        if self.dissolved is not None and self.dissolved > datetime.now().year:
            raise ValidationError({
                'dissolved': ValidationError(('Dissolved date must be in the past')),
            })

    def get_absolute_url(self):
        return reverse('manufacturer-detail', kwargs={'slug': self.slug})

    @classmethod
    def description(cls):
        return 'Manufacturers are any maker or brand of camera, lenses or other photographic accessories or consumables'

    class Moderator:
        visible_until_rejected = True
        keep_history = True

# Table to list all archives that exist for storing physical media


class Archive(models.Model):
    # Choices for archive types
    class ArchiveType(DjangoChoices):
        Negative = ChoiceItem()
        Slide = ChoiceItem()
        Print = ChoiceItem()

    # Choices for archive storage
    class ArchiveStorage(DjangoChoices):
        Ringbinder = ChoiceItem()
        Folder = ChoiceItem()
        Box = ChoiceItem()
        Portfolio = ChoiceItem()
        Slide_tray = ChoiceItem()

    type = models.CharField(max_length=8, choices=ArchiveType.choices,
                            help_text='What is stored in this archive?')
    name = models.CharField(
        help_text='Name of this archive', max_length=45, unique=True)
    max_width = models.PositiveIntegerField(
        help_text='Maximum width of media that this archive can store', blank=True, null=True)
    max_height = models.PositiveIntegerField(
        help_text='Maximum height of media that this archive can store', blank=True, null=True)
    location = models.CharField(
        help_text='Location of this archive', max_length=45, blank=True, null=True)
    storage = models.CharField(choices=ArchiveStorage.choices,
                               help_text='The type of storage used for this archive', max_length=45, blank=True, null=True)
    sealed = models.BooleanField(
        help_text='Whether or not this archive is sealed (closed to new additions)', default=0)
    owner = CurrentUserField(editable=False)
    id_owner = AutoSequenceField(unique_with='owner', editable=False, verbose_name='ID')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "archives"

    def get_absolute_url(self):
        return reverse('archive-detail', kwargs={'id_owner': self.id_owner})

    @classmethod
    def description(cls):
        return 'Archives are places where prints, negatives, or slides are stored'

# Table to catalog of types of battery


class Battery(models.Model):
    class Chemistry(DjangoChoices):
        Alkaline = ChoiceItem()
        Nickel_cadmium = ChoiceItem()
        Nickel_metal_hydride = ChoiceItem()
        Carbon_zinc = ChoiceItem()
        Lithium = ChoiceItem()
        Lithium_ion = ChoiceItem()
        Lithium_polymer = ChoiceItem()
        Mercury = ChoiceItem()
        Zinc_air = ChoiceItem()
        Silver_oxide = ChoiceItem()

    name = models.CharField(
        help_text='Common name of the battery', max_length=45, unique=True)
    voltage = models.DecimalField(help_text='Nominal voltage of the battery',
                                  max_digits=5, decimal_places=2, blank=True, null=True)
    chemistry = models.CharField(help_text='Battery chemistry',
                                 choices=Chemistry.choices, max_length=45, blank=True, null=True)
    compatible_with = models.ManyToManyField(
        'Battery', blank=True, help_text='Batteries that are compatible with this one')
    slug = models.SlugField(editable=False, null=True, unique=True)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, editable=False)
    created_by = CurrentUserField(
        editable=False, related_name='battery_created_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, editable=False)
    updated_by = CurrentUserField(
        on_update=True, editable=False, related_name='battery_updated_by')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "batteries"

    def save(self, *args, **kwargs):
        custom_slugify_unique = Slugify(to_lower=True)
        self.slug = custom_slugify_unique(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('battery-detail', kwargs={'slug': self.slug})

    @classmethod
    def description(cls):
        return 'Batteries are used to power cameras, flashes and other accessories'

    class Moderator:
        visible_until_rejected = True
        keep_history = True

# Table to list of physical condition descriptions that can be used to evaluate equipment


class Condition(models.Model):
    code = models.CharField(
        help_text='Condition shortcode (e.g. EXC)', max_length=6)
    name = models.CharField(
        help_text='Full name of condition (e.g. Excellent)', max_length=45)
    min_rating = models.PositiveIntegerField(help_text='The lowest percentage rating that encompasses this condition',
                                             validators=[MinValueValidator(0), MaxValueValidator(100)])
    max_rating = models.PositiveIntegerField(help_text='The highest percentage rating that encompasses this condition',
                                             validators=[MinValueValidator(0), MaxValueValidator(100)])
    description = models.CharField(
        help_text='Longer description of condition', max_length=300)

    def __str__(self):
        return "%s - %s" % (self.name, self.description)

    class Meta:
        verbose_name_plural = "conditions"

# Exposure programs as defined by EXIF tag ExposureProgram


class ExposureProgram(models.Model):
    name = models.CharField(
        help_text='Name of exposure program as defined by EXIF tag ExposureProgram', max_length=45)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "exposure programs"

# Table to catalog different protocols used to communicate with flashes


class FlashProtocol(models.Model):
    name = models.CharField(
        help_text='Name of the flash protocol', max_length=45)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE,
                                     blank=True, null=True, help_text='Manufacturer who owns this flash protocol')
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, editable=False)
    created_by = CurrentUserField(
        editable=False, related_name='flashprotocol_created_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, editable=False)
    updated_by = CurrentUserField(
        on_update=True, editable=False, related_name='flashprotocol_updated_by')

    def __str__(self):
        if self.manufacturer is not None:
            mystr = "%s %s" % (self.manufacturer.name, self.name)
        else:
            mystr = self.name
        return mystr

    class Meta:
        ordering = ['name']
        verbose_name_plural = "flash protocols"

    def get_absolute_url(self):
        return reverse('flashprotocol-detail', kwargs={'pk': self.pk})

    @classmethod
    def description(cls):
        return 'Flash protocols are systems that cameras use to communicate with flash systems'

# Table to catalog filters


class Filter(models.Model):
    type = models.CharField(
        help_text='Filter type (e.g. Red, Circular polariser, Ultraviolet)', max_length=45)
    shortname = models.CharField(
        help_text='Filter type shortname (e.g. Red, CPL, UV)', max_length=45, blank=True, null=True)
    attenuation = models.DecimalField(
        help_text='Attenuation of this filter in decimal stops', max_digits=3, decimal_places=1, blank=True, null=True)

    def __str__(self):
        return self.type

    class Meta:
        ordering = ['type']
        verbose_name_plural = "filters"

    def get_absolute_url(self):
        return reverse('filter-detail', kwargs={'pk': self.pk})

    @classmethod
    def description(cls):
        return 'Filters are glass or gelatin attachments for lenses which affect the image in some way'

# Table to catalog different negative sizes available. Negtives sizes are distinct from film formats.


class NegativeSize(models.Model):
    name = models.CharField(
        help_text='Common name of the negative size (e.g. 35mm, 6x7, etc)', max_length=45, unique=True)
    width = models.DecimalField(help_text='Width of the negative size in mm',
                                max_digits=4, decimal_places=1, blank=True, null=True)
    height = models.DecimalField(help_text='Height of the negative size in mm',
                                 max_digits=4, decimal_places=1, blank=True, null=True)
    crop_factor = models.DecimalField(help_text='Crop factor of this negative size',
                                      max_digits=4, decimal_places=2, blank=True, null=True, editable=False)
    area = models.PositiveIntegerField(
        help_text='Area of this negative size in sq. mm', blank=True, null=True, editable=False)
    aspect_ratio = models.DecimalField(help_text='Aspect ratio of this negative size, expressed as a single decimal (e.g. 3:2 is expressed as 1.5)',
                                       max_digits=4, decimal_places=2, blank=True, null=True, editable=False)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, editable=False)
    created_by = CurrentUserField(
        editable=False, related_name='negativesize_created_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, editable=False)
    updated_by = CurrentUserField(
        on_update=True, editable=False, related_name='negativesize_updated_by')

    def __str__(self):
        return self.name
    # Override save method to calculate some fields

    def save(self, *args, **kwargs):
        if self.width is not None and self.height is not None:
            self.aspect_ratio = self.width/self.height
            self.area = self.width*self.height
            diag = sqrt(self.width**2 + self.height**2)
            diag35mm = 43.2666
            self.crop_factor = diag35mm/diag
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['area']
        verbose_name_plural = "negative sizes"

    def get_absolute_url(self):
        return reverse('negativesize-detail', kwargs={'pk': self.pk})

    @classmethod
    def description(cls):
        return 'Negative size is the dimensions of an image taken by a camera. It is different from film format as one film format can be used for various different negative sizes.'

# Table to catalogue different film formats. These are distinct from negative sizes.


class Format(models.Model):
    format = models.CharField(
        help_text='The name of this film/sensor format', max_length=45, unique=True)
    negative_size = models.ManyToManyField(NegativeSize, blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, editable=False)
    created_by = CurrentUserField(
        editable=False, related_name='format_created_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, editable=False)
    updated_by = CurrentUserField(
        on_update=True, editable=False, related_name='format_updated_by')

    def __str__(self):
        return self.format

    class Meta:
        ordering = ['format']
        verbose_name_plural = "formats"

    def get_absolute_url(self):
        return reverse('format-detail', kwargs={'pk': self.pk})

    @classmethod
    def description(cls):
        return 'Format is the type of film a camera uses. It is a bit different from negative size as one film format can be used for various different negative sizes.'

# Table to catalog flashes, flashguns and speedlights


class Flash(models.Model):
    model = models.CharField(
        help_text='Model name/number of the flash', max_length=45)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE,
                                     blank=True, null=True, help_text='Manufacturer of this flash')
    guide_number = models.PositiveIntegerField(
        help_text='Guide number of the flash', blank=True, null=True)
    gn_info = models.CharField(verbose_name='Guide number info',
                               help_text='Extra freeform info about how the guide number was measured', max_length=45, blank=True, null=True)
    battery_powered = models.BooleanField(
        help_text='Whether this flash takes batteries', blank=True, null=True)
    pc_sync = models.BooleanField(
        verbose_name='PC sync', help_text='Whether the flash has a PC sync socket', blank=True, null=True)
    hot_shoe = models.BooleanField(
        help_text='Whether the flash has a hot shoe connection', blank=True, null=True)
    light_stand = models.BooleanField(
        help_text='Whether the flash can be used on a light stand', blank=True, null=True)
    battery_type = models.ForeignKey(Battery, on_delete=models.CASCADE, blank=True,
                                     null=True, help_text='Type of battery required by this flash')
    battery_qty = models.PositiveIntegerField(
        help_text='Quantity of batteries needed in this flash', blank=True, null=True)
    manual_control = models.BooleanField(
        help_text='Whether this flash offers manual power control', blank=True, null=True)
    swivel_head = models.BooleanField(
        help_text='Whether this flash has a horizontal swivel head', blank=True, null=True)
    tilt_head = models.BooleanField(
        help_text='Whether this flash has a vertical tilt head', blank=True, null=True)
    zoom = models.BooleanField(
        help_text='Whether this flash can zoom', blank=True, null=True)
    ttl = models.BooleanField(
        verbose_name='TTL', help_text='Whether this flash supports TTL metering', blank=True, null=True)
    flash_protocol = models.ForeignKey(FlashProtocol, on_delete=models.CASCADE,
                                       blank=True, null=True, help_text='Flash protocol used by this flash')
    trigger_voltage = models.DecimalField(
        help_text='Trigger voltage of the flash, in Volts', max_digits=5, decimal_places=1, blank=True, null=True)
    own = models.BooleanField(
        help_text='Whether we currently own this flash', blank=True, null=True)
    acquired = models.DateField(
        help_text='Date this flash was acquired', blank=True, null=True)
    cost = MoneyField(help_text='Purchase cost of this flash', max_digits=12,
                      decimal_places=2, blank=True, null=True, default_currency='GBP')
    owner = CurrentUserField(editable=False)
    id_owner = AutoSequenceField(unique_with='owner', editable=False, verbose_name='ID')

    def __str__(self):
        if self.manufacturer is not None:
            mystr = "%s %s" % (self.manufacturer.name, self.model)
        else:
            mystr = self.model
        return mystr

    class Meta:
        ordering = ['manufacturer', 'model']
        verbose_name_plural = "flashes"

    def clean(self):
        # if battery_type is set, need to supply battery_qty
        if self.battery_type is not None and self.battery_qty is None:
            raise ValidationError({
                'battery_qty': ValidationError(('Must specify number of batteries')),
            })

    def get_absolute_url(self):
        return reverse('flash-detail', kwargs={'id_owner': self.id_owner})

    @classmethod
    def description(cls):
        return 'Flashes are any kind of external device to provide light. This includes battery-powered and mains-powered flashes.'

# Table to list enlargers


class Enlarger(models.Model):

    class EnlargerType(DjangoChoices):
        Diffusion = ChoiceItem()
        Condenser = ChoiceItem()

    class LightSource(DjangoChoices):
        Incandescent = ChoiceItem()
        Cold_cathode = ChoiceItem()
        LED = ChoiceItem()

    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE,
                                     blank=True, null=True, help_text='Manufacturer of this enlarger')
    model = models.CharField(
        help_text='Name/model of the enlarger', max_length=45)
    negative_size = models.ForeignKey(NegativeSize, on_delete=models.CASCADE, blank=True,
                                      null=True, help_text='Largest negative size that this enlarger can accept')
    type = models.CharField(choices=EnlargerType.choices,
                            help_text='The type of optical system in the enlarger', max_length=15, blank=True, null=True)
    light_source = models.CharField(
        choices=LightSource.choices, help_text='The type of light source used in the enlarger', max_length=15, blank=True, null=True)
    acquired = models.DateField(
        help_text='Date on which the enlarger was acquired', blank=True, null=True)
    lost = models.DateField(
        help_text='Date on which the enlarger was lost/sold', blank=True, null=True)
    introduced = models.PositiveIntegerField(
        help_text='Year in which the enlarger was introduced', blank=True, null=True)
    discontinued = models.PositiveIntegerField(
        help_text='Year in which the enlarger was discontinued', blank=True, null=True)
    cost = MoneyField(help_text='Purchase cost of this enlarger', max_digits=12,
                      decimal_places=2, blank=True, null=True, default_currency='GBP')
    lost_price = MoneyField(help_text='Sale price of the enlarger', max_digits=12,
                            decimal_places=2, blank=True, null=True, default_currency='GBP')
    owner = CurrentUserField(editable=False)
    id_owner = AutoSequenceField(unique_with='owner', editable=False, verbose_name='ID')

    def __str__(self):
        if self.manufacturer is not None:
            mystr = "%s %s" % (self.manufacturer.name, self.model)
        else:
            mystr = self.model
        return mystr

    class Meta:
        ordering = ['manufacturer', 'model']
        verbose_name_plural = "enlargers"

    def clean(self):
        # Acquired/lost
        if self.acquired is not None and self.lost is not None and self.acquired > self.lost:
            raise ValidationError({
                'acquired': ValidationError(('Acquired date must be earlier than lost date')),
                'lost': ValidationError(('Lost date must be later than acquired date')),
            })
        if self.acquired is not None and self.acquired > datetime.date(datetime.now()):
            raise ValidationError({
                'acquired': ValidationError(('Acquired date must be in the past')),
            })
        if self.lost is not None and self.lost > datetime.date(datetime.now()):
            raise ValidationError({
                'lost': ValidationError(('Lost date must be in the past')),
            })
        # Introduced/discontinued
        if self.introduced is not None and self.discontinued is not None and self.introduced > self.discontinued:
            raise ValidationError({
                'introduced': ValidationError(('Introduced date must be earlier than discontinued date')),
                'discontinued': ValidationError(('Discontinued date must be later than introduced date')),
            })
        if self.introduced is not None and self.introduced > datetime.now().year:
            raise ValidationError({
                'introduced': ValidationError(('Introduced date must be in the past')),
            })
        if self.discontinued is not None and self.discontinued > datetime.now().year:
            raise ValidationError({
                'discontinued': ValidationError(('Discontinued date must be in the past')),
            })

    def get_absolute_url(self):
        return reverse('enlarger-detail', kwargs={'id_owner': self.id_owner})

    @classmethod
    def description(cls):
        return 'Enlargers are devices used to create prints from negatives.'

# Metering modes as defined by EXIF tag MeteringMode


class MeteringMode(models.Model):
    name = models.CharField(
        help_text='Name of metering mode as defined by EXIF tag MeteringMode', max_length=45)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "metering modes"

# Table to catalog different lens mount standards. This is mostly used for camera lens mounts, but can also be used for enlarger and projector lenses.


class Mount(models.Model):

    # Choices for mount types
    class MountType(DjangoChoices):
        Bayonet = ChoiceItem()
        Breech_lock = ChoiceItem()
        Screw = ChoiceItem()
        Friction = ChoiceItem()
        Lens_board = ChoiceItem()

    # Choices for mount purposes
    class Purpose(DjangoChoices):
        Camera = ChoiceItem()
        Enlarger = ChoiceItem()
        Projector = ChoiceItem()
        Telescope = ChoiceItem()
        Microscope = ChoiceItem()

    mount = models.CharField(
        help_text='Name of this lens mount (e.g. Canon FD)', max_length=45, unique=True)
    shutter_in_lens = models.BooleanField(
        help_text='Whether this lens mount system incorporates the shutter into the lens', default=0, blank=True, null=True)
    type = models.CharField(help_text='The physical mount type of this lens mount',
                            choices=MountType.choices, max_length=15, blank=True, null=True)
    purpose = models.CharField(help_text='The intended purpose of this lens mount',
                               choices=Purpose.choices, max_length=15, blank=True, null=True)
    notes = models.CharField(
        help_text='Freeform notes field', max_length=100, blank=True, null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE,
                                     blank=True, null=True, help_text='Manufacturer who owns this lens mount')
    slug = models.SlugField(editable=False, null=True, unique=True)
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, editable=False)
    created_by = CurrentUserField(
        editable=False, related_name='mount_created_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, editable=False)
    updated_by = CurrentUserField(
        on_update=True, editable=False, related_name='mount_updated_by')

    def __str__(self):
        return self.mount

    def save(self, *args, **kwargs):
        custom_slugify_unique = Slugify(to_lower=True)
        self.slug = custom_slugify_unique(self.mount)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['mount']
        verbose_name_plural = "mounts"

    def get_absolute_url(self):
        return reverse('mount-detail', kwargs={'slug': self.slug})

    @classmethod
    def description(cls):
        return 'Mounts are physical systems used to attach lenses to cameras (or enlargers, or projectors).'

# Table to catalog different paper stocks available


class PaperStock(models.Model):
    # Choices for mount purposes
    class Finish(DjangoChoices):
        Matt = ChoiceItem()
        Gloss = ChoiceItem()
        Satin = ChoiceItem()
        Semi_gloss = ChoiceItem()
        Pearl = ChoiceItem()
        Lustre = ChoiceItem()

    name = models.CharField(
        help_text='Name of this paper stock', max_length=45)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE,
                                     blank=True, null=True, help_text='Manufacturer of this paper stock')
    resin_coated = models.BooleanField(
        help_text='Whether the paper is resin-coated', blank=True, null=True)
    colour = models.BooleanField(
        help_text='Whether this is a colour paper', blank=True, null=True)
    finish = models.CharField(help_text='The finish of the paper surface',
                              choices=Finish.choices, max_length=25, blank=True, null=True)
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, editable=False)
    created_by = CurrentUserField(
        editable=False, related_name='paperstock_created_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, editable=False)
    updated_by = CurrentUserField(
        on_update=True, editable=False, related_name='paperstock_updated_by')

    def __str__(self):
        mystr = self.name
        if self.manufacturer is not None:
            mystr = str(self.manufacturer) + ' ' + mystr
        if self.finish is not None:
            mystr = mystr + ' [' + self.finish + ']'
        return mystr

    class Meta:
        ordering = ['manufacturer', 'name']
        verbose_name_plural = "paper stocks"

    def get_absolute_url(self):
        return reverse('paperstock-detail', kwargs={'pk': self.pk})

    @classmethod
    def description(cls):
        return 'Paper stocks are types of paper available for printing with'

# Table to catalog photographers


class Person(models.Model):
    name = models.CharField(
        help_text='Name of the photographer', max_length=45, unique=True)
    owner = CurrentUserField(editable=False)
    id_owner = AutoSequenceField(unique_with='owner', editable=False, verbose_name='ID')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "people"

    def get_absolute_url(self):
        return reverse('person-detail', kwargs={'id_owner': self.id_owner})

    @classmethod
    def description(cls):
        return 'People listed here can be selected as photographers, developers or printers.'

# Table to catalog chemical processes that can be used to develop film and paper


class Process(models.Model):
    name = models.CharField(
        help_text='Name of this developmenmt process (e.g. C-41, E-6)', max_length=25, unique=True)
    colour = models.BooleanField(
        help_text='Whether this is a colour process', blank=True, null=True)
    positive = models.BooleanField(
        help_text='Whether this is a positive/reversal process', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "processes"

    def get_absolute_url(self):
        return reverse('process-detail', kwargs={'pk': self.pk})

    @classmethod
    def description(cls):
        return 'Processes are methods of developing film or prints'

# Table to catalog teleconverters (multipliers)


class Teleconverter(models.Model):
    model = models.CharField(
        help_text='Model name of this teleconverter', max_length=45)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE,
                                     blank=True, null=True, help_text='Manufacturer of this teleconverter')
    mount = models.ForeignKey(Mount, on_delete=models.CASCADE, blank=True, null=True,
                              help_text='Lens mount used by this teleconverter', limit_choices_to={'purpose': 'Camera'})
    factor = models.DecimalField(help_text='Magnification factor of this teleconverter (numerical part only, e.g. 1.4)',
                                 max_digits=4, decimal_places=2, blank=True, null=True)
    elements = models.PositiveIntegerField(
        help_text='Number of optical elements used in this teleconverter', blank=True, null=True)
    groups = models.PositiveIntegerField(
        help_text='Number of optical groups used in this teleconverter', blank=True, null=True)
    multicoated = models.BooleanField(
        help_text='Whether this teleconverter is multi-coated', blank=True, null=True)
    owner = CurrentUserField(editable=False)
    id_owner = AutoSequenceField(unique_with='owner', editable=False, verbose_name='ID')

    def __str__(self):
        if self.manufacturer is not None:
            mystr = "%s %s" % (self.manufacturer.name, self.model)
        else:
            mystr = self.model
        return mystr

    class Meta:
        ordering = ['manufacturer', 'model']
        verbose_name_plural = "teleconverters"

    def clean(self):
        # Groups/elements
        if self.groups is not None and self.elements is not None and self.groups > self.elements:
            raise ValidationError({
                'groups': ValidationError(('Cannot have more groups than elements')),
                'elements': ValidationError(('Cannot have fewer elements than groups')),
            })

    def get_absolute_url(self):
        return reverse('teleconverter-detail', kwargs={'id_owner': self.id_owner})

    @classmethod
    def description(cls):
        return 'Teleconverters are extra lenses that can be used to increase the focal length of a lens. They are sometimes known as doublers.'

# Table to catalog paper toners that can be used during the printing process


class Toner(models.Model):
    name = models.CharField(help_text='Name of the toner', max_length=45)
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, help_text='Manufacturer of this toner')
    formulation = models.CharField(
        help_text='Chemical formulation of the toner', max_length=45, blank=True, null=True)
    stock_dilution = models.CharField(
        help_text='Stock dilution of the toner', max_length=10, blank=True, null=True)
    slug = models.SlugField(editable=False, null=True, unique=True)
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, editable=False)
    created_by = CurrentUserField(
        editable=False, related_name='toner_created_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, editable=False)
    updated_by = CurrentUserField(
        on_update=True, editable=False, related_name='toner_updated_by')

    def __str__(self):
        if self.manufacturer is not None:
            mystr = "%s %s" % (self.manufacturer.name, self.name)
        else:
            mystr = self.name
        return mystr

    class Meta:
        ordering = ['manufacturer', 'name']
        verbose_name_plural = "toners"
        constraints = [
            models.UniqueConstraint(
                fields=['manufacturer', 'name'], name='toner_unique_name')
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            custom_slugify_unique = UniqueSlugify(
                unique_check=toner_check, to_lower=True)
            self.slug = custom_slugify_unique(
                "{} {}".format(self.manufacturer.name, self.name))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('toner-detail', kwargs={'slug': self.slug})

    @classmethod
    def description(cls):
        return 'Toners are chemicals used to change the colour or appearance of a print.'

# Table to list different brands of film stock


class FilmStock(models.Model):
    name = models.CharField(help_text='Name of the filmstock', max_length=45)
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, help_text='Manufacturer of this film')
    iso = models.PositiveIntegerField(
        verbose_name='ISO', help_text='Nominal ISO speed of the film', blank=True, null=True)
    colour = models.BooleanField(
        help_text='Whether the film is colour', blank=True, null=True)
    panchromatic = models.BooleanField(
        help_text='Whether this film is panchromatic', blank=True, null=True)
    process = models.ForeignKey(Process, on_delete=models.CASCADE, blank=True,
                                null=True, help_text='Development process required by this film')
    slug = models.SlugField(editable=False, null=True, unique=True)
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, editable=False)
    created_by = CurrentUserField(
        editable=False, related_name='filmstock_created_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, editable=False)
    updated_by = CurrentUserField(
        on_update=True, editable=False, related_name='filmstock_updated_by')

    def __str__(self):
        if self.manufacturer is not None:
            mystr = "%s %s" % (self.manufacturer.name, self.name)
        else:
            mystr = self.name
        return mystr

    class Meta:
        ordering = ['manufacturer', 'name']
        verbose_name_plural = "film stocks"
        constraints = [
            models.UniqueConstraint(
                fields=['manufacturer', 'name'], name='filmstock_unique_name')
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            custom_slugify_unique = UniqueSlugify(
                unique_check=filmstock_check, to_lower=True)
            self.slug = custom_slugify_unique(
                "{} {}".format(self.manufacturer.name, self.name))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('filmstock-detail', kwargs={'slug': self.slug})

    @classmethod
    def description(cls):
        return 'Film stocks are types of film that can be exposed in a camera. They may also be known as emulsions.'

# Table to record bulk film stock, from which individual films can be cut


class BulkFilm(models.Model):
    format = models.ForeignKey(
        Format, on_delete=models.CASCADE, help_text='Film format of this bulk film')
    filmstock = models.ForeignKey(
        FilmStock, on_delete=models.CASCADE, help_text='Filmstock of this bulk film')
    purchase_date = models.DateField(
        help_text='Purchase date of this bulk roll', blank=True, null=True)
    cost = MoneyField(help_text='Purchase cost of this bulk roll', max_digits=12,
                      decimal_places=2, blank=True, null=True, default_currency='GBP')
    source = models.CharField(
        help_text='Place where this bulk roll was bought from', max_length=45, blank=True, null=True)
    batch = models.CharField(
        help_text='Batch code of this bulk roll', max_length=45, blank=True, null=True)
    expiry = models.DateField(
        help_text='Expiry date of this bulk roll', blank=True, null=True)
    owner = CurrentUserField(editable=False)
    id_owner = AutoSequenceField(unique_with='owner', editable=False, verbose_name='ID')

    def __str__(self):
        return "#%s %s %s" % (self.id_owner, self.filmstock.manufacturer.name, self.filmstock.name)

    class Meta:
        verbose_name_plural = "bulk films"

    def get_absolute_url(self):
        return reverse('bulkfilm-detail', kwargs={'id_owner': self.id_owner})

    @classmethod
    def description(cls):
        return 'Bulk films are large reels of film stock that can be cut up to make individual films.'

# Table to catalog adapters to mount lenses on other cameras


class MountAdapter(models.Model):
    camera_mount = models.ForeignKey(
        Mount, on_delete=models.CASCADE, help_text='Mount used to attach a camera', related_name="camera_mount")
    lens_mount = models.ForeignKey(Mount, on_delete=models.CASCADE,
                                   help_text='Mount used to attach a lens', related_name="lens_mount")
    has_optics = models.BooleanField(
        help_text='Whether this adapter includes optical elements', blank=True, null=True)
    infinity_focus = models.BooleanField(
        help_text='Whether this adapter allows infinity focus', blank=True, null=True)
    notes = models.CharField(help_text='Freeform notes',
                             max_length=100, blank=True, null=True)
    owner = CurrentUserField(editable=False)
    id_owner = AutoSequenceField(unique_with='owner', editable=False, verbose_name='ID')

    def __str__(self):
        return "%s - %s" % (self.camera_mount, self.lens_mount)

    class Meta:
        ordering = ['camera_mount', 'lens_mount']
        verbose_name_plural = "mount adapters"

    def get_absolute_url(self):
        return reverse('mountadapter-detail', kwargs={'id_owner': self.id_owner})

    @classmethod
    def description(cls):
        return 'Mount adapters can be used to convert the mount used on a camera or lens.'

# Table to list all possible shutter speeds


class ShutterSpeed(models.Model):
    shutter_speed = models.CharField(
        help_text='Shutter speed in fractional notation, e.g. 1/250', max_length=10, primary_key=True)
    # field validation: like 1/500 or 2
    duration = models.DecimalField(
        help_text='Shutter speed in decimal notation, e.g. 0.04', max_digits=9, decimal_places=5, editable=False)

    def __str__(self):
        return self.shutter_speed

    def save(self, *args, **kwargs):
        # Test if format is 1/125
        fractional = re.match(r'^(\d{1})/(\d+)$', self.shutter_speed)
        # Test if format is 1 or 1"
        integer = re.match(r'^(\d+)"?$', self.shutter_speed)
        if fractional:
            self.duration = int(fractional.group(1)) / int(fractional.group(2))
        elif integer:
            self.duration = integer.group(1)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['duration']
        verbose_name_plural = "shutter speeds"

# Table to list film and paper developers


class Developer(models.Model):
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, help_text='Manufacturer of this developer')
    name = models.CharField(help_text='Name of the developer', max_length=45)
    for_paper = models.BooleanField(
        help_text='Whether this developer can be used with paper', blank=True, null=True)
    for_film = models.BooleanField(
        help_text='Whether this developer can be used with film', blank=True, null=True)
    chemistry = models.CharField(
        help_text='The key chemistry on which this developer is based (e.g. phenidone)', max_length=45, blank=True, null=True)
    slug = models.SlugField(editable=False, null=True, unique=True)
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, editable=False)
    created_by = CurrentUserField(
        editable=False, related_name='developer_created_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, editable=False)
    updated_by = CurrentUserField(
        on_update=True, editable=False, related_name='developer_updated_by')

    def __str__(self):
        if self.manufacturer is not None:
            mystr = "%s %s" % (self.manufacturer.name, self.name)
        else:
            mystr = self.name
        return mystr

    class Meta:
        ordering = ['manufacturer', 'name']
        verbose_name_plural = "developers"
        constraints = [
            models.UniqueConstraint(
                fields=['manufacturer', 'name'], name='developer_unique_name')
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            custom_slugify_unique = UniqueSlugify(
                unique_check=developer_check, to_lower=True)
            self.slug = custom_slugify_unique(
                "{} {}".format(self.manufacturer.name, self.name))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('developer-detail', kwargs={'slug': self.slug})

    @classmethod
    def description(cls):
        return 'Developers are chemicals that are used to process films or prints.'

# Table to catalog lens models


class LensModel(models.Model):
    # Choices for focus type
    class CoatingType(DjangoChoices):
        Uncoated = ChoiceItem()
        Single_coated = ChoiceItem()
        Multi_coated = ChoiceItem()

    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, help_text='Manufacturer of this lens model')
    model = models.CharField(
        help_text='Model name of this lens', max_length=45)
    disambiguation = models.CharField(
        help_text='Distinguishing notes for lens models with the same name', max_length=45, blank=True, null=True)
    mount = models.ForeignKey(Mount, on_delete=models.CASCADE, blank=True,
                              null=True, help_text='Mount used by this lens model')
    zoom = models.BooleanField(
        help_text='Whether this is a zoom lens', blank=True, null=True)
    min_focal_length = models.PositiveIntegerField(
        help_text='Shortest focal length of this lens, in mm', blank=True, null=True)
    max_focal_length = models.PositiveIntegerField(
        help_text='Longest focal length of this lens, in mm', blank=True, null=True)
    closest_focus = models.PositiveIntegerField(
        help_text='The closest focus possible with this lens, in cm', blank=True, null=True)
    max_aperture = models.DecimalField(
        help_text='Maximum (widest) aperture available on this lens (numerical part only, e.g. 2.8)', max_digits=4, decimal_places=1, blank=True, null=True)
    min_aperture = models.DecimalField(
        help_text='Minimum (narrowest) aperture available on this lens (numerical part only, e.g. 22)', max_digits=4, decimal_places=1, blank=True, null=True)
    elements = models.PositiveIntegerField(
        help_text='Number of optical lens elements', blank=True, null=True)
    groups = models.PositiveIntegerField(
        help_text='Number of optical groups', blank=True, null=True)
    weight = models.PositiveIntegerField(
        help_text='Weight of this lens, in grammes (g)', blank=True, null=True)
    nominal_min_angle_diag = models.PositiveIntegerField(
        verbose_name='Min angle of view', help_text='Nominal minimum diagonal field of view from manufacturer specs', blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(360)])
    nominal_max_angle_diag = models.PositiveIntegerField(
        verbose_name='Max angle of view', help_text='Nominal maximum diagonal field of view from manufacturer specs', blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(360)])
    aperture_blades = models.PositiveIntegerField(
        help_text='Number of aperture blades', blank=True, null=True)
    autofocus = models.BooleanField(
        help_text='Whether this lens has autofocus capability', blank=True, null=True)
    filter_thread = models.DecimalField(
        help_text='Diameter of lens filter thread, in mm', max_digits=4, decimal_places=1, blank=True, null=True)
    magnification = models.DecimalField(
        help_text='Maximum magnification ratio of the lens, expressed like 0.765', max_digits=5, decimal_places=3, blank=True, null=True)
    url = models.URLField(
        verbose_name='URL', help_text='URL to more information about this lens', blank=True, null=True)
    introduced = models.PositiveIntegerField(
        help_text='Year in which this lens model was introduced', blank=True, null=True)
    discontinued = models.PositiveIntegerField(
        help_text='Year in which this lens model was discontinued', blank=True, null=True)
    negative_size = models.ForeignKey(NegativeSize, on_delete=models.CASCADE, blank=True,
                                      null=True, help_text='Largest negative size that this lens is designed for')
    notes = models.CharField(
        help_text='Freeform notes field', max_length=100, blank=True, null=True)
    coating = models.CharField(choices=CoatingType.choices,
                               help_text='Type of lens coating', max_length=15, blank=True, null=True)
    hood = models.CharField(
        help_text='Model number of the compatible lens hood', max_length=45, blank=True, null=True)
    rectilinear = models.BooleanField(
        help_text='Whether this is a rectilinear lens', default=1, blank=True, null=True)
    length = models.PositiveIntegerField(
        help_text='Length of lens in mm', blank=True, null=True)
    diameter = models.PositiveIntegerField(
        help_text='Width of lens in mm', blank=True, null=True)
    image_circle = models.PositiveIntegerField(
        help_text='Diameter of image circle projected by lens, in mm', blank=True, null=True)
    shutter_model = models.CharField(
        help_text='Name of the integrated shutter, if any', max_length=45, blank=True, null=True)
    slug = models.SlugField(editable=False, null=True, unique=True)
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, editable=False)
    created_by = CurrentUserField(
        editable=False, related_name='lensmodel_created_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, editable=False)
    updated_by = CurrentUserField(
        on_update=True, editable=False, related_name='lensmodel_updated_by')

    def __str__(self):
        mystr = self.model
        if self.manufacturer is not None:
            mystr = str(self.manufacturer) + ' ' + mystr
        if self.disambiguation is not None:
            mystr = mystr + ' [' + self.disambiguation + ']'
        return mystr

    class Meta:
        ordering = ['manufacturer', 'model']
        verbose_name_plural = "lens models"
        constraints = [
            models.UniqueConstraint(
                fields=['manufacturer', 'model', 'disambiguation'], name='lensmodel_unique_name')
        ]

    def get_absolute_url(self):
        return reverse('lensmodel-detail', kwargs={'slug': self.slug})

    @classmethod
    def description(cls):
        return 'Lens models are any interchangeable lens that has been marketed'

    def clean(self):
        # Check focal length
        if self.min_focal_length is not None and self.max_focal_length is not None and self.min_focal_length > self.max_focal_length:
            raise ValidationError({
                'min_focal_length': ValidationError(('Min focal length must be smaller than max focal length')),
                'max_focal_length': ValidationError(('Max focal length must be larger than min focal length')),
            })

        # Angle of view
        if self.nominal_min_angle_diag is not None and self.nominal_max_angle_diag is not None and self.nominal_min_angle_diag > self.nominal_max_angle_diag:
            raise ValidationError({
                'nominal_min_angle_diag': ValidationError(('Min angle of view must be smaller than max angle of view')),
                'nominal_max_angle_diag': ValidationError(('Max angle of view must be larger than min angle of view')),
            })

        # Introduced/discontinued
        if self.introduced is not None and self.discontinued is not None and self.introduced > self.discontinued:
            raise ValidationError({
                'introduced': ValidationError(('Introduced date must be earlier than discontinued date')),
                'discontinued': ValidationError(('Discontinued date must be later than introduced date')),
            })
        if self.introduced is not None and self.introduced > datetime.now().year:
            raise ValidationError({
                'introduced': ValidationError(('Introduced date must be in the past')),
            })
        if self.discontinued is not None and self.discontinued > datetime.now().year:
            raise ValidationError({
                'discontinued': ValidationError(('Discontinued date must be in the past')),
            })

        # Groups and elements
        if self.groups is not None and self.elements is not None and self.elements < self.groups:
            raise ValidationError({
                'elements': ValidationError(("Can't have more groups than elements")),
                'groups': ValidationError(("Can't have more groups than elements")),
            })

        # Zoom lenses
        if self.zoom is False and self.min_focal_length and self.max_focal_length and self.min_focal_length != self.max_focal_length:
            raise ValidationError({
                'min_focal_length': ValidationError(('Min and max focal lengths must be equal for non-zoom lenses')),
                'max_focal_length': ValidationError(('Min and max focal lengths must be equal for non-zoom lenses')),
            })

        # Aperture range
        if self.max_aperture is not None and self.min_aperture is not None and self.max_aperture > self.min_aperture:
            raise ValidationError({
                'max_aperture': ValidationError(('Max aperture must be smaller than min aperture')),
                'min_aperture': ValidationError(('Max aperture must be smaller than min aperture')),
            })

    def save(self, *args, **kwargs):
        # Auto-populate focal length
        if self.zoom is False and self.min_focal_length is not None:
            self.max_focal_length = self.min_focal_length
        if not self.slug:
            custom_slugify_unique = UniqueSlugify(
                unique_check=lensmodel_check, to_lower=True)
            self.slug = custom_slugify_unique("{} {} {}".format(
                self.manufacturer.name, self.model, str(self.disambiguation or '')))
        super().save(*args, **kwargs)

# Table to catalog camera models - both cameras with fixed and interchangeable lenses


class CameraModel(models.Model):
    # Choices for body types
    class BodyType(DjangoChoices):
        Box_camera = ChoiceItem()
        Folding_camera = ChoiceItem()
        Compact_camera = ChoiceItem()
        SLR = ChoiceItem()
        TLR = ChoiceItem()
        Bridge_camera = ChoiceItem()
        View_camera = ChoiceItem()
        Pistol_grip_camera = ChoiceItem()
        Miniature_camera = ChoiceItem()

    # Choices for focus type
    class FocusType(DjangoChoices):
        Autofocus = ChoiceItem()
        Fixed_focus = ChoiceItem()
        Zone_focus = ChoiceItem()
        Rangefinder = ChoiceItem()
        SLR = ChoiceItem()
        TLR = ChoiceItem()
        View_camera = ChoiceItem()

    # Choices for shutter type
    class ShutterType(DjangoChoices):
        Focal_plane_cloth = ChoiceItem()
        Focal_plane_metal = ChoiceItem()
        Leaf = ChoiceItem()
        Rotary = ChoiceItem()
        Sliding = ChoiceItem()
        Electronic = ChoiceItem()

    # Choices for metering type
    class MeteringType(DjangoChoices):
        Cadmium_sulphide_CdS = ChoiceItem()
        Selenium = ChoiceItem()
        Silicon = ChoiceItem()

    # Choices for shoe type
    class ShoeType(DjangoChoices):
        No_shoe = ChoiceItem()
        Hot_shoe = ChoiceItem()
        Cold_shoe = ChoiceItem()

    # Choices for focus type
    class CoatingType(DjangoChoices):
        Uncoated = ChoiceItem()
        Single_coated = ChoiceItem()
        Multi_coated = ChoiceItem()

    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE, help_text='Manufacturer of this camera model')
    model = models.CharField(
        help_text='The model name of the camera', max_length=45)
    disambiguation = models.CharField(
        help_text='Distinguishing notes for camera models with the same name', max_length=45, blank=True, null=True)
    mount = models.ForeignKey(Mount, on_delete=models.CASCADE, blank=True, null=True,
                              help_text='Lens mount used by this camera model', limit_choices_to={'purpose': 'Camera'})
    format = models.ForeignKey(Format, on_delete=models.CASCADE, blank=True,
                               null=True, help_text='Film format used by this camera model')
    focus_type = models.CharField(choices=FocusType.choices, max_length=25,
                                  blank=True, null=True, help_text='Focus type used on this camera model')
    metering = models.BooleanField(
        help_text='Whether the camera has built-in metering', blank=True, null=True)
    metering_type = models.CharField(choices=MeteringType.choices, max_length=25,
                                     blank=True, null=True, help_text='Metering type used on this camera model')
    introduced = models.PositiveIntegerField(
        help_text='Year in which the camera model was introduced', blank=True, null=True)
    discontinued = models.PositiveIntegerField(
        help_text='Year in which the camera model was discontinued', blank=True, null=True)
    body_type = models.CharField(choices=BodyType.choices, max_length=25,
                                 blank=True, null=True, help_text='Body type of this camera model')
    weight = models.PositiveIntegerField(
        help_text='Weight of the camera body (without lens or batteries) in grammes (g)', blank=True, null=True)
    negative_size = models.ForeignKey(NegativeSize, on_delete=models.CASCADE,
                                      blank=True, null=True, help_text='Size of negative created by this camera')
    shutter_type = models.CharField(choices=ShutterType.choices, max_length=25,
                                    blank=True, null=True, help_text='Type of shutter used on this camera model')
    shutter_model = models.CharField(
        help_text='Model of shutter', max_length=45, blank=True, null=True)
    cable_release = models.BooleanField(
        help_text='Whether the camera has the facility for a remote cable release', blank=True, null=True)
    viewfinder_coverage = models.PositiveIntegerField(help_text='Percentage coverage of the viewfinder. Mostly applicable to SLRs.', blank=True, null=True,
                                                      validators=[MinValueValidator(0), MaxValueValidator(100)])
    power_drive = models.BooleanField(
        help_text='Whether the camera has integrated motor drive', blank=True, null=True)
    continuous_fps = models.DecimalField(
        help_text='The maximum rate at which the camera can shoot, in frames per second', max_digits=4, decimal_places=1, blank=True, null=True)
    battery_qty = models.PositiveIntegerField(
        help_text='Quantity of batteries needed', blank=True, null=True)
    battery_type = models.ForeignKey(Battery, on_delete=models.CASCADE, blank=True,
                                     null=True, help_text='Battery type that this camera model needs')
    notes = models.CharField(
        help_text='Freeform text field for extra notes', max_length=100, blank=True, null=True)
    bulb = models.BooleanField(
        help_text='Whether the camera supports bulb (B) exposure', blank=True, null=True)
    time = models.BooleanField(
        help_text='Whether the camera supports time (T) exposure', blank=True, null=True)
    min_iso = models.PositiveIntegerField(
        verbose_name='Min ISO', help_text='Minimum ISO the camera will accept for metering', blank=True, null=True)
    max_iso = models.PositiveIntegerField(
        verbose_name='Max ISO', help_text='Maximum ISO the camera will accept for metering', blank=True, null=True)
    af_points = models.PositiveIntegerField(
        verbose_name='Autofocus points', help_text='Number of autofocus points', blank=True, null=True)
    int_flash = models.BooleanField(
        verbose_name='Internal flash', help_text='Whether the camera has an integrated flash', blank=True, null=True)
    int_flash_gn = models.PositiveIntegerField(
        verbose_name='Internal flash guide number', help_text='Guide number of internal flash', blank=True, null=True)
    ext_flash = models.BooleanField(
        verbose_name='External flash', help_text='Whether the camera supports an external flash', blank=True, null=True)
    flash_metering = models.ForeignKey(FlashProtocol, on_delete=models.CASCADE, blank=True,
                                       null=True, help_text='Whether this camera model supports flash metering')
    pc_sync = models.BooleanField(
        verbose_name='PC sync', help_text='Whether the camera has a PC sync socket for flash', blank=True, null=True)
    shoe = models.CharField(choices=ShoeType.choices, max_length=9, blank=True,
                            null=True, help_text='Type of flash/accessory shoe used on this camera model')
    x_sync = models.ForeignKey(ShutterSpeed, on_delete=models.CASCADE, blank=True,
                               null=True, help_text='Flash X-sync speed', related_name='x_sync')
    meter_min_ev = models.IntegerField(
        verbose_name='Min EV', help_text='Lowest EV/LV the built-in meter supports', blank=True, null=True)
    meter_max_ev = models.PositiveIntegerField(
        verbose_name='Max EV', help_text='Highest EV/LV the built-in meter supports', blank=True, null=True)
    dof_preview = models.BooleanField(
        verbose_name='DoF preview', help_text='Whether the camera has depth of field preview', blank=True, null=True)
    mirror_lockup = models.BooleanField(
        verbose_name='Mirror lock-up', help_text='Whether the camera has mirror lock-up', blank=True, null=True)
    tripod = models.BooleanField(
        help_text='Whether the camera has a tripod bush', blank=True, null=True)
    shutter_speeds = models.ManyToManyField(ShutterSpeed, blank=True)
    metering_modes = models.ManyToManyField(MeteringMode, blank=True)
    exposure_programs = models.ManyToManyField(ExposureProgram, blank=True)
    slug = models.SlugField(editable=False, null=True, unique=True)
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, editable=False)
    created_by = CurrentUserField(
        editable=False, related_name='cameramodel_created_by')
    updated_at = models.DateTimeField(auto_now=True, null=True, editable=False)
    updated_by = CurrentUserField(
        on_update=True, editable=False, related_name='cameramodel_updated_by')
    tags = TaggableManager(blank=True)
    url = models.URLField(
        verbose_name='URL', help_text='URL to more information about this camera model', blank=True, null=True)

    # Fixed lens fields
    lens_manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE,
                                          help_text='Manufacturer of this lens model', blank=True, null=True, related_name='lens_manufacturer')
    lens_model_name = models.CharField(
        help_text='Model name of this lens', max_length=45, blank=True, null=True)
    zoom = models.BooleanField(
        help_text='Whether this is a zoom lens', blank=True, null=True)
    min_focal_length = models.PositiveIntegerField(
        help_text='Shortest focal length of this lens, in mm', blank=True, null=True)
    max_focal_length = models.PositiveIntegerField(
        help_text='Longest focal length of this lens, in mm', blank=True, null=True)
    closest_focus = models.PositiveIntegerField(
        help_text='The closest focus possible with this lens, in cm', blank=True, null=True)
    max_aperture = models.DecimalField(
        help_text='Maximum (widest) aperture available on this lens (numerical part only, e.g. 2.8)', max_digits=4, decimal_places=1, blank=True, null=True)
    min_aperture = models.DecimalField(
        help_text='Minimum (narrowest) aperture available on this lens (numerical part only, e.g. 22)', max_digits=4, decimal_places=1, blank=True, null=True)
    elements = models.PositiveIntegerField(
        help_text='Number of optical lens elements', blank=True, null=True)
    groups = models.PositiveIntegerField(
        help_text='Number of optical groups', blank=True, null=True)
    nominal_min_angle_diag = models.PositiveIntegerField(
        verbose_name='Min angle of view', help_text='Nominal minimum diagonal field of view from manufacturer specs', blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(360)])
    nominal_max_angle_diag = models.PositiveIntegerField(
        verbose_name='Max angle of view', help_text='Nominal maximum diagonal field of view from manufacturer specs', blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(360)])
    aperture_blades = models.PositiveIntegerField(
        help_text='Number of aperture blades', blank=True, null=True)
    filter_thread = models.DecimalField(
        help_text='Diameter of lens filter thread, in mm', max_digits=4, decimal_places=1, blank=True, null=True)
    magnification = models.DecimalField(
        help_text='Maximum magnification ratio of the lens, expressed like 0.765', max_digits=5, decimal_places=3, blank=True, null=True)
    coating = models.CharField(choices=CoatingType.choices,
                               help_text='Type of lens coating', max_length=15, blank=True, null=True)
    hood = models.CharField(
        help_text='Model number of the compatible lens hood', max_length=45, blank=True, null=True)
    rectilinear = models.BooleanField(
        help_text='Whether this is a rectilinear lens', default=1, blank=True, null=True)
    image_circle = models.PositiveIntegerField(
        help_text='Diameter of image circle projected by lens, in mm', blank=True, null=True)

    def __str__(self):
        mystr = self.model
        if self.manufacturer is not None:
            mystr = str(self.manufacturer) + ' ' + mystr
        if self.disambiguation is not None:
            mystr = mystr + ' [' + self.disambiguation + ']'
        return mystr

    class Meta:
        ordering = ['manufacturer', 'model']
        verbose_name_plural = "camera models"
        constraints = [
            models.UniqueConstraint(
                fields=['manufacturer', 'model', 'disambiguation'], name='cameramodel_unique_name')
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            custom_slugify_unique = UniqueSlugify(
                unique_check=cameramodel_check, to_lower=True)
            self.slug = custom_slugify_unique("{} {} {}".format(
                self.manufacturer.name, self.model, str(self.disambiguation or '')))
        super().save(*args, **kwargs)

    def clean(self):
        # Enforce either fixed or interchangeable lens
        if self.mount is not None and (self.lens_manufacturer is not None or self.lens_manufacturer is not None):
            raise ValidationError({
                'mount': ValidationError(('Choose either Fixed or Interchangeable lens, not both')),
                'lens_model_name': ValidationError(('Choose either Fixed or Interchangeable lens, not both')),
            })

        # ISO
        if self.min_iso is not None and self.max_iso is not None and self.min_iso > self.max_iso:
            raise ValidationError({
                'min_iso': ValidationError(('Min ISO must be smaller than max ISO')),
                'max_iso': ValidationError(('Max ISO must be larger than min ISO')),
            })
        # EV
        if self.meter_min_ev is not None and self.meter_max_ev is not None and self.meter_min_ev > self.meter_max_ev:
            raise ValidationError({
                'meter_min_ev': ValidationError(('Min EV must be smaller than max EV')),
                'meter_max_ev': ValidationError(('Max EV must be larger than min EV')),
            })
        # Introduced/discontinued
        if self.introduced is not None and self.discontinued is not None and self.introduced > self.discontinued:
            raise ValidationError({
                'introduced': ValidationError(('Introduced date must be earlier than discontinued date')),
                'discontinued': ValidationError(('Discontinued date must be later than introduced date')),
            })
        if self.introduced is not None and self.introduced > datetime.now().year:
            raise ValidationError({
                'introduced': ValidationError(('Introduced date must be in the past')),
            })
        if self.discontinued is not None and self.discontinued > datetime.now().year:
            raise ValidationError({
                'discontinued': ValidationError(('Discontinued date must be in the past')),
            })
        # Metering bools
        if self.metering is not None and self.metering is False:
            if self.metering_type is True:
                raise ValidationError({
                    'discontinued': ValidationError(('Cannot set metering type if camera model has no metering')),
                })
            if self.metering_modes is True:
                raise ValidationError({
                    'discontinued': ValidationError(('Cannot set metering modes if camera model has no metering')),
                })
        # int_flash_gn
        if self.int_flash is False and self.int_flash_gn is not None:
            raise ValidationError({
                'int_flash_gn': ValidationError(('Cannot set internal flash guide number if camera model has no internal flash')),
            })

            # Check focal length
        if self.min_focal_length is not None and self.max_focal_length is not None and self.min_focal_length > self.max_focal_length:
            raise ValidationError({
                'min_focal_length': ValidationError(('Min focal length must be smaller than max focal length')),
                'max_focal_length': ValidationError(('Max focal length must be larger than min focal length')),
            })

        # Angle of view
        if self.nominal_min_angle_diag is not None and self.nominal_max_angle_diag is not None and self.nominal_min_angle_diag > self.nominal_max_angle_diag:
            raise ValidationError({
                'nominal_min_angle_diag': ValidationError(('Min angle of view must be smaller than max angle of view')),
                'nominal_max_angle_diag': ValidationError(('Max angle of view must be larger than min angle of view')),
            })

        # Groups and elements
        if self.groups is not None and self.elements is not None and self.elements < self.groups:
            raise ValidationError({
                'elements': ValidationError(("Can't have more groups than elements")),
                'groups': ValidationError(("Can't have more groups than elements")),
            })

        # Zoom lenses
        if self.zoom is False and self.min_focal_length and self.max_focal_length and self.min_focal_length != self.max_focal_length:
            raise ValidationError({
                'min_focal_length': ValidationError(('Min and max focal lengths must be equal for non-zoom lenses')),
                'max_focal_length': ValidationError(('Min and max focal lengths must be equal for non-zoom lenses')),
            })

        # Aperture range
        if self.max_aperture is not None and self.min_aperture is not None and self.max_aperture > self.min_aperture:
            raise ValidationError({
                'max_aperture': ValidationError(('Max aperture must be smaller than min aperture')),
                'min_aperture': ValidationError(('Max aperture must be smaller than min aperture')),
            })

    def get_absolute_url(self):
        return reverse('cameramodel-detail', kwargs={'slug': self.slug})

    @classmethod
    def description(cls):
        return 'Camera models are any camera that has been marketed'

# Table to catalog accessories that are not tracked in more specific tables


class Accessory(models.Model):
    # Choices for accessory types
    class AccessoryType(DjangoChoices):
        Battery_grip = ChoiceItem()
        Case = ChoiceItem()
        Film_back = ChoiceItem()
        Focusing_screen = ChoiceItem()
        Lens_hood = ChoiceItem()
        Lens_cap = ChoiceItem()
        Power_winder = ChoiceItem()
        Viewfinder = ChoiceItem()
        Rangefinder = ChoiceItem()
        Projector = ChoiceItem()
        Light_meter = ChoiceItem()

    type = models.CharField(choices=AccessoryType.choices,
                            help_text='Type of accessory', max_length=15)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE,
                                     blank=True, null=True, help_text='Manufacturer of this accessory')
    model = models.CharField(help_text='Model of the accessory', max_length=45)
    acquired = models.DateField(
        help_text='Date that this accessory was acquired', blank=True, null=True)
    cost = MoneyField(help_text='Purchase cost of the accessory', max_digits=12,
                      decimal_places=2, blank=True, null=True, default_currency='GBP')
    lost = models.DateField(
        help_text='Date that this accessory was lost', blank=True, null=True)
    lost_price = MoneyField(help_text='Sale price of the accessory', max_digits=12,
                            decimal_places=2, blank=True, null=True, default_currency='GBP')
    camera_model_compatibility = models.ManyToManyField(
        CameraModel, blank=True)
    lens_model_compatibility = models.ManyToManyField(LensModel, blank=True)
    owner = CurrentUserField(editable=False)
    id_owner = AutoSequenceField(unique_with='owner', editable=False, verbose_name='ID')

    def __str__(self):
        if self.manufacturer is not None:
            mystr = "%s %s" % (self.manufacturer.name, self.model)
        else:
            mystr = self.model
        return mystr

    class Meta:
        ordering = ['manufacturer', 'model']
        verbose_name_plural = "accessories"

    def clean(self):
        # Acquired/lost
        if self.acquired is not None and self.lost is not None and self.acquired > self.lost:
            raise ValidationError({
                'acquired': ValidationError(('Acquired date must be earlier than lost date')),
                'lost': ValidationError(('Lost date must be later than acquired date')),
            })
        if self.acquired is not None and self.acquired > datetime.date(datetime.now()):
            raise ValidationError({
                'acquired': ValidationError(('Acquired date must be in the past')),
            })
        if self.lost is not None and self.lost > datetime.date(datetime.now()):
            raise ValidationError({
                'lost': ValidationError(('Lost date must be in the past')),
            })

    def get_absolute_url(self):
        return reverse('accessory-detail', kwargs={'id_owner': self.id_owner})

    @classmethod
    def description(cls):
        return 'Accessories include most photographic items which may be used with cameras or lenses. Exceptions are filters, flashes and teleconverters, which are tracked separately.'

# Table to catalog lenses


class Lens(models.Model):
    lensmodel = models.ForeignKey(
        LensModel, on_delete=models.CASCADE, help_text='Lens model of this lens')
    serial = models.CharField(
        help_text='Serial number of this lens', max_length=45, blank=True, null=True)
    date_code = models.CharField(
        help_text='Date code of this lens, if different from the serial number', max_length=45, blank=True, null=True)
    manufactured = models.PositiveIntegerField(
        help_text='Year in which this specific lens was manufactured', blank=True, null=True)
    acquired = models.DateField(
        help_text='Date on which this lens was acquired', blank=True, null=True)
    cost = MoneyField(help_text='Price paid for this lens', max_digits=12,
                      decimal_places=2, blank=True, null=True, default_currency='GBP')
    notes = models.CharField(
        help_text='Freeform notes field', max_length=45, blank=True, null=True)
    own = models.BooleanField(
        help_text='Whether we currently own this lens', blank=True, null=True)
    lost = models.DateField(
        help_text='Date on which lens was lost/sold/disposed', blank=True, null=True)
    lost_price = MoneyField(help_text='Sale price of the lens', max_digits=12,
                            decimal_places=2, blank=True, null=True, default_currency='GBP')
    source = models.CharField(
        help_text='Place where the lens was acquired from', max_length=150, blank=True, null=True)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE,
                                  blank=True, null=True, help_text='Condition of this lens')
    condition_notes = models.CharField(
        help_text='Description of condition', max_length=150, blank=True, null=True)
    owner = CurrentUserField(editable=False)
    id_owner = AutoSequenceField(unique_with='owner', editable=False, verbose_name='ID')

    def __str__(self):
        if self.serial is not None:
            mystr = "%s %s (#%s)" % (self.lensmodel.manufacturer.name, self.lensmodel.model, self.serial)
        else:
            mystr = "%s %s" % (self.lensmodel.manufacturer.name, self.lensmodel.model)
        return mystr

    class Meta:
        ordering = ['lensmodel__manufacturer', 'lensmodel__model', 'serial']
        verbose_name_plural = "lenses"
        unique_together = ['lensmodel', 'serial']

    def clean(self):
        if self.acquired is not None and self.lost is not None and self.acquired > self.lost:
            raise ValidationError({
                'acquired': ValidationError(('Acquired date must be earlier than lost date')),
                'lost': ValidationError(('Lost date must be later than acquired date')),
            })
        if self.acquired is not None and self.acquired > datetime.date(datetime.now()):
            raise ValidationError({
                'acquired': ValidationError(('Acquired date must be in the past')),
            })
        if self.lost is not None and self.lost > datetime.date(datetime.now()):
            raise ValidationError({
                'lost': ValidationError(('Lost date must be in the past')),
            })
        # Manufactured date must be in range of introduced-discontinued of the model
        if self.manufactured is not None:
            if self.lensmodel.introduced is not None and self.manufactured < self.lensmodel.introduced:
                raise ValidationError({
                    'manufactured': ValidationError(('Manufactured date cannot be earlier than the date the lens model was introduced')),
                })
            if self.lensmodel.discontinued is not None and self.manufactured > self.lensmodel.discontinued:
                raise ValidationError({
                    'manufactured': ValidationError(('Manufactured date cannot be later than the date the lens model was discontinued')),
                })

    def get_absolute_url(self):
        return reverse('lens-detail', kwargs={'id_owner': self.id_owner})

    @classmethod
    def description(cls):
        return 'Lenses are specific examples of lens models that exist in your collection'

# Table to catalog cameras - both cameras with fixed lenses and cameras with interchangeable lenses


class Camera(models.Model):
    cameramodel = models.ForeignKey(
        CameraModel, on_delete=models.CASCADE, help_text='Camera model of this camera')
    acquired = models.DateField(
        help_text='Date on which the camera was acquired', blank=True, null=True)
    cost = MoneyField(help_text='Price paid for this camera', max_digits=12,
                      decimal_places=2, blank=True, null=True, default_currency='GBP')
    serial = models.CharField(
        help_text='Serial number of the camera', max_length=45, blank=True, null=True)
    datecode = models.CharField(
        help_text='Date code of the camera, if different from the serial number', max_length=45, blank=True, null=True)
    manufactured = models.PositiveIntegerField(
        help_text='Year of manufacture of the camera', blank=True, null=True)
    own = models.BooleanField(
        help_text='Whether the camera is currently owned', blank=True, null=True)
    notes = models.CharField(
        help_text='Freeform text field for extra notes', max_length=100, blank=True, null=True)
    lost = models.DateField(
        help_text='Date on which the camera was lost/sold/etc', blank=True, null=True)
    lost_price = MoneyField(help_text='Sale price of the camera', max_digits=12,
                            decimal_places=2, blank=True, null=True, default_currency='GBP')
    source = models.CharField(
        help_text='Where the camera was acquired from', max_length=150, blank=True, null=True)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE,
                                  blank=True, null=True, help_text='Condition of this camera')
    condition_notes = models.CharField(
        help_text='Description of condition', max_length=150, blank=True, null=True)
    owner = CurrentUserField(editable=False)
    id_owner = AutoSequenceField(unique_with='owner', editable=False, verbose_name='ID')

    def __str__(self):
        if self.serial is not None:
            mystr = "%s %s (#%s)" % (self.cameramodel.manufacturer.name, self.cameramodel.model, self.serial)
        else:
            mystr = "%s %s" % (self.cameramodel.manufacturer.name, self.cameramodel.model)
        return mystr

    class Meta:
        ordering = ['cameramodel__manufacturer',
                    'cameramodel__model', 'serial']
        verbose_name_plural = "cameras"
        unique_together = ['cameramodel', 'serial']

    def clean(self):
        if self.acquired is not None and self.lost is not None and self.acquired > self.lost:
            raise ValidationError({
                'acquired': ValidationError(('Acquired date must be earlier than lost date')),
                'lost': ValidationError(('Lost date must be later than acquired date')),
            })
        if self.acquired is not None and self.acquired > datetime.date(datetime.now()):
            raise ValidationError({
                'acquired': ValidationError(('Acquired date must be in the past')),
            })
        if self.lost is not None and self.lost > datetime.date(datetime.now()):
            raise ValidationError({
                'lost': ValidationError(('Lost date must be in the past')),
            })
        # Manufactured date must be in range of introduced-discontinued of the model
        if self.manufactured is not None:
            if self.cameramodel.introduced is not None and self.manufactured < self.cameramodel.introduced:
                raise ValidationError({
                    'manufactured': ValidationError(('Manufactured date cannot be earlier than the date the camera model was introduced')),
                })
            if self.cameramodel.discontinued is not None and self.manufactured > self.cameramodel.discontinued:
                raise ValidationError({
                    'manufactured': ValidationError(('Manufactured date cannot be later than the date the camera model was discontinued')),
                })

    def get_absolute_url(self):
        return reverse('camera-detail', kwargs={'id_owner': self.id_owner})

    @classmethod
    def description(cls):
        return 'Cameras are specific examples of camera models that exist in your collection'

# Table to list films which consist of one or more negatives. A film can be a roll film, one or more sheets of sheet film, one or more photographic plates, etc.


class Film(models.Model):
    filmstock = models.ForeignKey(
        FilmStock, on_delete=models.CASCADE, help_text='Filmstock that this film is')
    exposed_at = models.PositiveIntegerField(
        help_text='ISO at which the film was exposed', blank=True, null=True)
    format = models.ForeignKey(
        Format, on_delete=models.CASCADE, help_text='Film format of this film')
    date_loaded = models.DateField(
        help_text='Date when the film was loaded into a camera', blank=True, null=True)
    date_processed = models.DateField(
        help_text='Date when the film was processed', blank=True, null=True)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, blank=True,
                               null=True, help_text='Camera that this film was loaded into')
    title = models.CharField(
        help_text='Title of the film', max_length=150, blank=True, null=True)
    frames = models.PositiveIntegerField(
        help_text='Expected (not actual) number of frames from the film', blank=True, null=True)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, blank=True, null=True,
                                  help_text='Developer used to develop this film', limit_choices_to={'for_film': True})
    directory = models.CharField(
        help_text='Name of the directory that contains the scanned images from this film', max_length=100, blank=True, null=True)
    dev_uses = models.PositiveIntegerField(
        help_text='Number of previous uses of the developer', blank=True, null=True)
    dev_time = models.DurationField(
        help_text='Duration of development', blank=True, null=True)
    dev_temp = models.DecimalField(
        help_text='Temperature of development', max_digits=3, decimal_places=1, blank=True, null=True)
    dev_n = models.IntegerField(
        help_text='Number of the Push/Pull rating of the film, e.g. N+1, N-2', blank=True, null=True)
    development_notes = models.CharField(
        help_text='Extra freeform notes about the development process', max_length=200, blank=True, null=True)
    bulk_film = models.ForeignKey(BulkFilm, on_delete=models.CASCADE,
                                  blank=True, null=True, help_text='Bulk film this film was cut from')
    bulk_film_loaded = models.DateField(
        help_text='Date that this film was cut from a bulk roll', blank=True, null=True)
    film_batch = models.CharField(
        help_text='Batch number of the film', max_length=45, blank=True, null=True)
    expiry_date = models.DateField(
        help_text='Expiry date of the film', blank=True, null=True)
    purchase_date = models.DateField(
        help_text='Date this film was purchased', blank=True, null=True)
    price = MoneyField(help_text='Price paid for this film', max_digits=12,
                       decimal_places=2, blank=True, null=True, default_currency='GBP')
    processed_by = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True,
                                     null=True, help_text='Person or place that processed this film')
    archive = models.ForeignKey(Archive, on_delete=models.CASCADE, blank=True,
                                null=True, help_text='Archive that this film is stored in')
    owner = CurrentUserField(editable=False)
    id_owner = AutoSequenceField(unique_with='owner', editable=False, verbose_name='ID')

    def __str__(self):
        return "#%s %s" % (self.id_owner, self.title)

    class Meta:
        verbose_name_plural = "films"

    def clean(self):
        # Date constraints
        if self.date_loaded is not None and self.date_processed is not None and self.date_loaded > self.date_processed:
            raise ValidationError({
                'date_loaded': ValidationError(('Date loaded cannot be later than the date the film was processed')),
                'date_processed': ValidationError(('Date processed cannot be earlier than the date the film was loaded')),
            })

    def save(self, *args, **kwargs):
        # Auto-populate values from bulk films
        if self.bulk_film:
            if self.bulk_film.expiry:
                self.expiry_date = self.bulk_film.expiry
            if self.bulk_film.batch:
                self.film_batch = self.bulk_film.batch
            if self.bulk_film.purchase_date:
                self.purchase_date = self.bulk_film.purchase_date
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('film-detail', kwargs={'id_owner': self.id_owner})

    @classmethod
    def description(cls):
        return 'A film is a specific example of a film stock which exists in your collection, and contains one or more negatives. A film is generally one roll film or one sheet of sheet film.'

# Table to catalog negatives (including positives/slides). Negatives are created by cameras, belong to films and can be used to create scans or prints.


class Negative(models.Model):
    film = models.ForeignKey(
        Film, on_delete=models.CASCADE, help_text='Film that this negative belongs to')
    frame = models.CharField(
        help_text='Frame number or code of this negative', max_length=8)
    caption = models.CharField(
        help_text='Caption of this picture', max_length=150, blank=True, null=True)
    date = models.DateTimeField(
        help_text='Date & time on which this picture was taken', blank=True, null=True)
    lens = models.ForeignKey(Lens, on_delete=models.CASCADE, blank=True,
                             null=True, help_text='Lens used to take this negative')
    shutter_speed = models.ForeignKey(ShutterSpeed, on_delete=models.CASCADE,
                                      blank=True, null=True, help_text='Shutter speed used to take this negative')
    aperture = models.DecimalField(help_text='Aperture used to take this picture (numerical part only)',
                                   max_digits=4, decimal_places=1, blank=True, null=True)
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE, blank=True,
                               null=True, help_text='Filter used when taking this negative')
    teleconverter = models.ForeignKey(Teleconverter, on_delete=models.CASCADE,
                                      blank=True, null=True, help_text='Teleconverter used when taking this negative')
    notes = models.CharField(
        help_text='Extra freeform notes about this exposure', max_length=200, blank=True, null=True)
    mount_adapter = models.ForeignKey(MountAdapter, on_delete=models.CASCADE,
                                      blank=True, null=True, help_text='Mount adapter used to mount lens')
    focal_length = models.PositiveIntegerField(
        help_text='If a zoom lens was used, specify the focal length of the lens', blank=True, null=True)
    latitude = models.DecimalField(help_text='Latitude of the location where the picture was taken', max_digits=9,
                                   decimal_places=6, blank=True, null=True, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.DecimalField(help_text='Longitude of the location where the picture was taken', max_digits=9,
                                    decimal_places=6, blank=True, null=True, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    flash = models.BooleanField(
        help_text='Whether flash was used', blank=True, null=True)
    metering_mode = models.ForeignKey(MeteringMode, on_delete=models.CASCADE,
                                      blank=True, null=True, help_text='Metering mode used when taking the image')
    exposure_program = models.ForeignKey(ExposureProgram, on_delete=models.CASCADE,
                                         blank=True, null=True, help_text='Exposure program used when taking the image')
    photographer = models.ForeignKey(Person, on_delete=models.CASCADE,
                                     blank=True, null=True, help_text='Photographer who took the negative')
    copy_of = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,
                                related_name='copy', help_text='Negative that this was duplicated from')
    owner = CurrentUserField(editable=False)
    id_owner = AutoSequenceField(unique_with='owner', editable=False, verbose_name='ID')

    def __str__(self):
        return "%s/%s %s" % (self.film.id_owner, self.frame, self.caption)

    class Meta:
        ordering = ['film', 'frame']
        verbose_name_plural = "negatives"
        unique_together = ['film', 'frame']

    def clean(self):
        # Aperture must be in range of lens model aperture
        if self.aperture is not None and self.lens is not None:
            if self.lens.lensmodel.max_aperture is not None and self.aperture < self.lens.lensmodel.max_aperture:
                raise ValidationError({
                    'aperture': ValidationError(('Aperture cannot be greater than the maximum aperture of the lens')),
                })
            if self.lens.lensmodel.min_aperture is not None and self.aperture > self.lens.lensmodel.min_aperture:
                raise ValidationError({
                    'aperture': ValidationError(('Aperture cannot be smaller than the minimum aperture of the lens')),
                })
        # Focal length must be in range of lens model fl
        if self.focal_length is not None and self.lens is not None:
            if self.lens.lensmodel.min_focal_length is not None and self.focal_length < self.lens.lensmodel.min_focal_length:
                raise ValidationError({
                    'focal_length': ValidationError(('Focal length cannot be shorter than the minimum focal length of the lens')),
                })
            if self.lens.lensmodel.max_focal_length is not None and self.focal_length > self.lens.lensmodel.max_focal_length:
                raise ValidationError({
                    'focal_length': ValidationError(('Focal length cannot be longer than the maximum focal length of the lens')),
                })

    def save(self, *args, **kwargs):
        # Auto-populate focal length
        if self.lens:
            if self.lens.lensmodel.zoom is False:
                if self.teleconverter is None:
                    self.focal_length = self.lens.lensmodel.min_focal_length
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('negative-detail', kwargs={'id_owner': self.id_owner})

    @classmethod
    def description(cls):
        return 'Negatives are exposures made on film. Exposures made on positive (slide) film are also known as negatives.'

# Table to catalog prints made from negatives


class Print(models.Model):
    negative = models.ForeignKey(
        Negative, on_delete=models.CASCADE, help_text='Negative that this print was made from')
    date = models.DateField(
        help_text='The date that the print was made', blank=True, null=True)
    paper_stock = models.ForeignKey(PaperStock, on_delete=models.CASCADE,
                                    blank=True, null=True, help_text='Paper stock that this print was made on')
    height = models.DecimalField(help_text='Height of the print in inches',
                                 max_digits=4, decimal_places=1, blank=True, null=True)
    width = models.DecimalField(help_text='Width of the print in inches',
                                max_digits=4, decimal_places=1, blank=True, null=True)
    aperture = models.DecimalField(help_text='Aperture used to make this print (numerical part only, e.g. 5.6)',
                                   max_digits=3, decimal_places=1, blank=True, null=True)
    exposure_time = models.DurationField(
        help_text='Exposure time of this print', blank=True, null=True)
    filtration_grade = models.DecimalField(help_text='Contrast grade of paper used', max_digits=2,
                                           decimal_places=1, blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(5)])
    development_time = models.DurationField(
        help_text='Development time of this print', blank=True, null=True)
    toner = models.ManyToManyField(
        'Toner', through='Toning', help_text='Toners and bleaches used to treat this print', blank=True)
    own = models.BooleanField(
        help_text='Whether we currently own this print', blank=True, null=True)
    location = models.CharField(
        help_text='The place where this print is currently', max_length=100, blank=True, null=True)
    sold_price = MoneyField(help_text='Sale price of the print', max_digits=12,
                            decimal_places=2, blank=True, null=True, default_currency='GBP')
    enlarger = models.ForeignKey(Enlarger, on_delete=models.CASCADE,
                                 blank=True, null=True, help_text='Enlarger used to make this print')
    lens = models.ForeignKey(Lens, on_delete=models.CASCADE, blank=True, null=True,
                             help_text='Enlarger lens used to make this print', limit_choices_to={'lensmodel__mount__purpose': 'Enlarger'})
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, blank=True, null=True,
                                  help_text='Developer used to develop this print', limit_choices_to={'for_paper': True})
    fine = models.BooleanField(
        help_text='Whether this is a fine print', blank=True, null=True)
    notes = models.CharField(
        help_text='Freeform notes about this print, e.g. dodging, burning & complex toning', max_length=200, blank=True, null=True)
    archive = models.ForeignKey(Archive, on_delete=models.CASCADE, blank=True,
                                null=True, help_text='Archive that this print is stored in')
    printer = models.ForeignKey(Person, on_delete=models.CASCADE,
                                blank=True, null=True, help_text='Person who made this print')
    owner = CurrentUserField(editable=False)
    id_owner = AutoSequenceField(unique_with='owner', editable=False, verbose_name='ID')

    def __str__(self):
        return "#%i" % (self.id_owner)

    class Meta:
        verbose_name_plural = "prints"

    def clean(self):
        # Aperture must be in range of lens model aperture
        if self.aperture is not None and self.lens is not None:
            if self.lens.lensmodel.max_aperture is not None and self.aperture < self.lens.lensmodel.max_aperture:
                raise ValidationError({
                    'aperture': ValidationError(('Aperture cannot be greater than the maximum aperture of the lens')),
                })
            if self.lens.lensmodel.min_aperture is not None and self.aperture > self.lens.lensmodel.min_aperture:
                raise ValidationError({
                    'aperture': ValidationError(('Aperture cannot be smaller than the minimum aperture of the lens')),
                })

    def get_absolute_url(self):
        return reverse('print-detail', kwargs={'id_owner': self.id_owner})

    @classmethod
    def description(cls):
        return 'Prints are images made on paper stock from negatives on film'

# Table to track which toners were used on which print


class Toning(models.Model):
    toner = models.ForeignKey(
        Toner, on_delete=models.CASCADE, help_text='Toner used on this print')
    print = models.ForeignKey(
        Print, on_delete=models.CASCADE, help_text='Print that was toned')
    dilution = models.CharField(
        help_text='Dilution of the toner', max_length=8, blank=True, null=True)
    duration = models.DurationField(
        help_text='Duration of the toning', blank=True, null=True)
    order = models.PositiveIntegerField(
        help_text='Order in which this toner was applied', blank=True, null=True)

    class Meta:
        ordering = ['order']
        unique_together = ['print', 'order']

# Table to catalog all repairs and servicing undertaken on cameras and lenses in the collection


class Repair(models.Model):
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE,
                               blank=True, null=True, help_text='Camera that was repaired')
    lens = models.ForeignKey(Lens, on_delete=models.CASCADE,
                             blank=True, null=True, help_text='Lens that was repaired')
    date = models.DateField(
        help_text='The date of the repair', blank=True, null=True)
    summary = models.CharField(
        help_text='Brief summary of the repair', max_length=100)
    detail = models.CharField(
        help_text='Longer description of the repair', max_length=500, blank=True, null=True)
    owner = CurrentUserField(editable=False)
    id_owner = AutoSequenceField(unique_with='owner', editable=False, verbose_name='ID')

    def __str__(self):
        return "#%i" % (self.id_owner)

    class Meta:
        ordering = ['date']
        verbose_name_plural = "repairs"

    def get_absolute_url(self):
        return reverse('repair-detail', kwargs={'id_owner': self.id_owner})

    @classmethod
    def description(cls):
        return 'Repairs are any maintenance work performed on cameras or lenses'

# Table to record all the images that have been scanned digitally


class Scan(models.Model):
    negative = models.ForeignKey(Negative, on_delete=models.CASCADE, blank=True,
                                 null=True, help_text='Negative that this scan was made from')
    print = models.ForeignKey(Print, on_delete=models.CASCADE, blank=True,
                              null=True, help_text='Print that this scan was made from')
    filename = models.CharField(
        help_text='Filename of the scan', max_length=128)
    date = models.DateField(
        help_text='Date that this scan was made', blank=True, null=True)
    colour = models.BooleanField(
        help_text='Whether this is a colour image', blank=True, null=True)
    width = models.PositiveIntegerField(
        help_text='Width of the scanned image in pixels', blank=True, null=True)
    height = models.PositiveIntegerField(
        help_text='Height of the scanned image in pixels', blank=True, null=True)
    owner = CurrentUserField(editable=False)
    id_owner = AutoSequenceField(unique_with='owner', editable=False, verbose_name='ID')

    def __str__(self):
        return self.filename

    def clean(self):
        # Check print source
        if self.negative is not None and self.print is not None:
            raise ValidationError({
                'negative': ValidationError(('Choose either negative or print')),
                'print': ValidationError(('Choose either negative or print')),
            })

    class Meta:
        verbose_name_plural = "scans"

    def get_absolute_url(self):
        return reverse('scan-detail', kwargs={'id_owner': self.id_owner})

    @classmethod
    def description(cls):
        return 'Scans are digital recreations of negatives or prints'

# Table to record orders for prints


class Order(models.Model):
    negative = models.ForeignKey(
        Negative, on_delete=models.CASCADE, help_text='Negative that needs to be printed')
    width = models.PositiveIntegerField(
        help_text='Width of print to be made', blank=True, null=True)
    height = models.PositiveIntegerField(
        help_text='Height of print to be made', blank=True, null=True)
    added = models.DateField(
        help_text='Date that the order was placed', blank=True, null=True)
    printed = models.BooleanField(
        help_text='Whether the print has been made', blank=True, null=True)
    print = models.ForeignKey(Print, on_delete=models.CASCADE, blank=True,
                              null=True, help_text='Print that was made to fulfil this order')
    recipient = models.ForeignKey(Person, on_delete=models.CASCADE,
                                  help_text='Person who placed this order', blank=True, null=True)
    owner = CurrentUserField(editable=False)
    id_owner = AutoSequenceField(unique_with='owner', editable=False, verbose_name='ID')

    def __str__(self):
        return "#%i" % (self.id_owner)

    class Meta:
        ordering = ['added']
        verbose_name_plural = "orders"

    def get_absolute_url(self):
        return reverse('order-detail', kwargs={'id_owner': self.id_owner})

    @classmethod
    def description(cls):
        return 'Orders are a to-do list of images to print'
