from django.contrib import admin

# The text to put at the top of each admin page, as an <h1> (a string). By default, this is “Django administration”.
admin.site.site_header = 'CameraHub'

# The text to put at the end of each admin page’s <title> (a string). By default, this is “Django site admin”.
admin.site.site_title = 'CameraHub'

# The text to put at the top of the admin index page (a string). By default, this is “Site administration”.
admin.site.index_title = 'CameraHub'

# The URL for the “View site” link at the top of each admin page. By default, site_url is /. Set it to None to remove the link.
admin.site.site_url = None

# Import all models that need admin pages
from schema.models import Accessory, Archive, Battery, BulkFilm, Camera, CameraModel, Developer, Enlarger, FilmStock, Filter
from schema.models import Flash, FlashProtocol, Format, Lens, LensModel, Manufacturer
from schema.models import Mount, MountAdapter, NegativeSize, Order, PaperStock, Person, Print, Toning
from schema.models import Process, Repair, Scan, Negative, Film, Series, ShutterSpeed, Teleconverter, Toner

# django-export-import
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class CameraModelResource(resources.ModelResource):
    class Meta:
        model = CameraModel

# Define inlines that can be embedded into other admin pages
class CameraInline(admin.TabularInline):
  model = Camera
  extra = 0

class CameraModelInline(admin.TabularInline):
  model = CameraModel
  extra = 0

class LensInline(admin.TabularInline):
  model = Lens
  extra = 0

class NegativeInline(admin.TabularInline):
  model = Negative
  extra = 0

class PrintInline(admin.TabularInline):
  model = Print
  extra = 0

class ScanInline(admin.TabularInline):
  model = Scan
  extra = 0

class ToningInline(admin.TabularInline):
  model = Print.toner.through
  verbose_name = "toner"
  verbose_name_plural = "toners"
  extra = 0

# Now register the admin pages, customising where necessary
class AccessoryAdmin(admin.ModelAdmin):
  filter_horizontal = ('camera_model_compatibility', 'lens_model_compatibility')
  exclude = ('owner',)
admin.site.register(Accessory, AccessoryAdmin)

class ArchiveAdmin(admin.ModelAdmin):
  exclude = ('owner',)
admin.site.register(Archive, ArchiveAdmin)

admin.site.register(Battery)

class BulkFilmAdmin(admin.ModelAdmin):
  exclude = ('owner',)
admin.site.register(BulkFilm, BulkFilmAdmin)

class CameraAdmin(admin.ModelAdmin):
  exclude = ('owner',)
admin.site.register(Camera, CameraAdmin)

class CameraModelAdmin(ImportExportModelAdmin):
  resource_class = CameraModelResource
  fieldsets = (
    (None, {
      'fields': ('manufacturer', 'model', 'mount', 'format', 'body_type', 'weight', ('introduced', 'discontinued'), 'negative_size', 'cable_release', 'viewfinder_coverage', ('power_drive', 'continuous_fps'), 'fixed_mount', 'lensmodel', ('battery_qty', 'battery_type'), 'notes', 'tripod', 'series'),
      'description': 'Enter information about this camera model',
    }),
    ('Metering', {
      'fields': ('metering', 'metering_type', 'coupled_metering', ('min_iso', 'max_iso'), ('meter_min_ev', 'meter_max_ev'), 'metering_modes', 'exposure_programs')
    }),
    ('Flash', {
      'fields': ('int_flash', 'int_flash_gn', 'ext_flash', 'flash_metering', 'pc_sync', 'hotshoe', 'coldshoe')
    }),
    ('Focus', {
      'fields': ('focus_type', 'af_points', 'dof_preview')
    }),
    ('Shutter', {
      'fields': ('shutter_type', 'shutter_model', 'shutter_speeds', 'bulb', 'time'),
    }),
  )
  inlines = [
    CameraInline,
  ]
  filter_horizontal = ('metering_modes', 'exposure_programs', 'series', 'shutter_speeds')
  search_fields = ['manufacturer__name', 'model', 'notes']
  list_display = ('__str__', 'mount', 'format', 'body_type', 'introduced')
  list_filter = ('manufacturer__name', 'mount', 'format', 'body_type', 'series')
admin.site.register(CameraModel, CameraModelAdmin)

admin.site.register(Developer)

class EnlargerAdmin(admin.ModelAdmin):
  exclude = ('owner',)
admin.site.register(Enlarger, EnlargerAdmin)

admin.site.register(FilmStock)

class FilterAdmin(admin.ModelAdmin):
  exclude = ('owner',)
admin.site.register(Filter, FilterAdmin)

class FlashAdmin(admin.ModelAdmin):
  exclude = ('owner',)
admin.site.register(Flash, FlashAdmin)

admin.site.register(FlashProtocol)

admin.site.register(Format)

class LensAdmin(admin.ModelAdmin):
  exclude = ('owner',)
admin.site.register(Lens, LensAdmin)

class LensModelAdmin(admin.ModelAdmin):
  fieldsets = (
    (None, {
      'fields': ('manufacturer', 'model', 'fixed_mount', 'mount'),
      'description': 'Enter information about this camera model',
    }),
    ('Optics', {
      'fields': ('zoom', ('min_focal_length', 'max_focal_length'), 'closest_focus', ('max_aperture', 'min_aperture'), ('elements', 'groups'), ('nominal_min_angle_diag', 'nominal_max_angle_diag'), 'magnification'),
    }),
    ('Physical', {
      'fields': ('length', 'diameter', 'weight'),
    }),
    ('Other', {
      'fields': ('aperture_blades', 'autofocus', 'filter_thread', 'url', 'introduced', 'discontinued', 'negative_size', 'notes', 'coating', 'hood', 'exif_lenstype', 'rectilinear', 'image_circle', 'formula', 'shutter_model', 'series'),
    })
  )
  inlines = [
    LensInline,
  ]
  filter_horizontal = ('series',)
  search_fields = ['manufacturer__name', 'model', 'notes']
  list_display = ('__str__', 'mount', 'min_focal_length', 'max_aperture', 'introduced')
  list_filter = ('manufacturer__name', 'mount')
admin.site.register(LensModel, LensModelAdmin)

admin.site.register(Manufacturer)

admin.site.register(Mount)

class MountAdapterAdmin(admin.ModelAdmin):
  exclude = ('owner',)
admin.site.register(MountAdapter, MountAdapterAdmin)

class NegativeSizeAdmin(admin.ModelAdmin):
  readonly_fields = ('area', 'crop_factor', 'aspect_ratio')
admin.site.register(NegativeSize, NegativeSizeAdmin)

class OrderAdmin(admin.ModelAdmin):
  exclude = ('owner',)
admin.site.register(Order, OrderAdmin)

admin.site.register(PaperStock)

class PersonAdmin(admin.ModelAdmin):
  exclude = ('owner',)
admin.site.register(Person, PersonAdmin)

class PrintAdmin(admin.ModelAdmin):
  fieldsets = (
    (None, {
      'fields': ('negative', 'date', 'notes', 'own', 'location', 'sold_price', 'fine', 'archive', 'printer', ),
    }),
    ('Paper', {
      'fields': ('paper_stock', 'height', 'width', ),
    }),
    ('Exposure', {
      'fields': ('aperture', 'exposure_time', 'filtration_grade', 'enlarger', 'lens',),
    }),
    ('Development', {
      'fields': ('developer', 'development_time',),
    }),
  )
  inlines = [
    ToningInline,
  ]
  exclude = ('owner',)
  search_fields = ['negative__caption', 'notes']
  list_display = ('__str__', 'date', 'negative')
  list_filter = ('paper_stock', 'developer', 'fine')
admin.site.register(Print, PrintAdmin)

admin.site.register(Process)

class RepairAdmin(admin.ModelAdmin):
  exclude = ('owner',)
admin.site.register(Repair, RepairAdmin)

class ScanAdmin(admin.ModelAdmin):
  exclude = ('owner',)
admin.site.register(Scan, ScanAdmin)

class NegativeAdmin(admin.ModelAdmin):
  fieldsets = (
    (None, {
      'fields': (('film', 'frame'), 'caption', 'date', 'notes', 'photographer'),
      'description': 'Enter information about this camera model',
    }),
    ('Exposure', {
      'fields': ('lens', 'mount_adapter', 'shutter_speed', 'aperture', 'filter', 'teleconverter', 'focal_length', 'flash', 'metering_mode', 'exposure_program', 'copy_of'),
    }),
    ('Location', {
      'fields': (('latitude', 'longitude'),),
    }),
  )
  search_fields = ['caption', 'notes']
  list_display = ('__str__', 'caption', 'date',)
  list_filter = ('film', 'photographer')
  inlines = [
    ScanInline,
    PrintInline,
  ]
  exclude = ('owner',)
admin.site.register(Negative, NegativeAdmin)

class FilmAdmin(admin.ModelAdmin):
  fieldsets = (
    (None, {
      'fields': ('format', 'title', 'filmstock', 'film_batch', 'expiry_date', 'purchase_date', 'price', 'frames'),
    }),
    ('Bulk film', {
      'fields': ('bulk_film', 'bulk_film_loaded'),
    }),
    ('Exposure', {
      'fields': ('exposed_at', 'camera', 'date_loaded'),
    }),
    ('Development', {
      'fields': ('developer', 'dev_uses', 'dev_time', 'dev_temp', 'dev_n', 'development_notes', 'processed_by', 'date_processed'),
    }),
    ('Archive', {
      'fields': ('directory', 'archive'),
    })
  )
  inlines = [
    NegativeInline,
  ]
  exclude = ('owner',)
admin.site.register(Film, FilmAdmin)

class SeriesAdmin(admin.ModelAdmin):
  exclude = ('owner',)
admin.site.register(Series, SeriesAdmin)

class ShutterSpeedAdmin(admin.ModelAdmin):
  readonly_fields = ('duration',)
admin.site.register(ShutterSpeed, ShutterSpeedAdmin)

class TeleconverterAdmin(admin.ModelAdmin):
  exclude = ('owner',)
admin.site.register(Teleconverter, TeleconverterAdmin)

admin.site.register(Toner)