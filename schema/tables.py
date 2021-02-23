# pylint: disable=no-member

import django_tables2 as tables
from django.utils.html import format_html
from django.urls import reverse
from schema.funcs import boolicon, colouricon

# Import all models that need admin pages
from schema.models import Accessory, Archive, Battery, BulkFilm, Camera, CameraModel, Developer, Enlarger, EnlargerModel, FilmStock, Filter
from schema.models import Flash, FlashModel, Format, Lens, LensModel, Manufacturer
from schema.models import Mount, MountAdapter, NegativeSize, Order, PaperStock, Person, Print
from schema.models import Process, Scan, Negative, Film, Teleconverter, TeleconverterModel, Toner


class AccessoryTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Accessory
        fields = ('id_owner', 'model', 'type')

    @classmethod
    def render_id_owner(cls, value):
        return format_html("<a href=\"{}\">#{}</a>", reverse('schema:accessory-detail', args=[value]), value)

    @classmethod
    def render_model(cls, value, record):
        return format_html("<a href=\"{}\">{} {}</a>", reverse('schema:accessory-detail', args=[record.id_owner]), record.manufacturer, value)


class ArchiveTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Archive
        fields = ('name', 'type', 'max_width', 'max_height', 'sealed')

    @classmethod
    def render_id_owner(cls, value):
        return format_html("<a href=\"{}\">#{}</a>", reverse('schema:archive-detail', args=[value]), value)

    @classmethod
    def render_name(cls, value, record):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:archive-detail', args=[record.id_owner]), value)

    @classmethod
    def render_sealed(cls, value):
        return format_html(boolicon(value))

    @classmethod
    def render_max_width(cls, value):
        return format_html("{}\"", value)

    @classmethod
    def render_max_height(cls, value):
        return format_html("{}\"", value)


class BatteryTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Battery
        fields = ('name', 'voltage', 'chemistry')

    @classmethod
    def render_name(cls, value, record):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:battery-detail', args=[record.slug]), value)

    @classmethod
    def render_voltage(cls, value):
        return format_html("{}V", value)


class BulkFilmTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = BulkFilm
        fields = ('id_owner', 'format', 'filmstock', 'length', 'finished')

    @classmethod
    def render_id_owner(cls, value):
        return format_html("<a href=\"{}\">#{}</a>", reverse('schema:bulkfilm-detail', args=[value]), value)

    @classmethod
    def render_finished(cls, value):
        return format_html(boolicon(value))

    @classmethod
    def render_format(cls, value):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:format-detail', args=[value.id]), value)

    @classmethod
    def render_filmstock(cls, value):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:filmstock-detail', args=[value.slug]), value)

    @classmethod
    def render_length(cls, value):
        return format_html("{}m", value)

class CameraTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Camera
        fields = ('id_owner', 'cameramodel', 'serial',
                  'manufactured', 'cameramodel__lens_model_name', 'own')

    @classmethod
    def render_id_owner(cls, value):
        return format_html("<a href=\"{}\">#{}</a>", reverse('schema:camera-detail', args=[value]), value)

    @classmethod
    def render_cameramodel(cls, value, record):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:cameramodel-detail', args=[record.cameramodel.slug]), value)

    @classmethod
    def render_serial(cls, value):
        return format_html("<code>{}</code>", value)

    @classmethod
    def render_own(cls, value):
        return format_html(boolicon(value))


class CameraModelTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = CameraModel
        fields = ('model', 'image', 'mount', 'format',
                  'introduced', 'body_type', 'negative_size', 'ratings')

    @classmethod
    def render_model(cls, value, record):
        if record.disambiguation:
            mystr = format_html("<a href=\"{}\">{} {} [{}]</a>", reverse('schema:cameramodel-detail', args=[
                record.slug]), record.manufacturer, value, record.disambiguation)
        else:
            mystr = format_html("<a href=\"{}\">{} {}</a>", reverse(
                'schema:cameramodel-detail', args=[record.slug]), record.manufacturer, value)
        if cls.request.user.is_authenticated:
            qty = Camera.objects.filter(
                owner=cls.request.user, cameramodel=record).count()
            if qty > 0:
                badge = format_html(
                    " <span class=\"badge badge-pill badge-primary\">{}</span>", qty)
            else:
                badge = format_html("")
        else:
            badge = format_html("")
        return mystr+badge

    @classmethod
    def render_image(cls, value):
        if value:
            icon = format_html(
                '<img src="/static/svg/camera.svg" width="20" height="20" alt="This camera model has a photo" title="This camera model has a photo">')
        return icon

    @classmethod
    def render_mount(cls, value):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:mount-detail', args=[value.slug]), value)

    @classmethod
    def render_format(cls, value):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:format-detail', args=[value.id]), value)

    @classmethod
    def render_negative_size(cls, value):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:negativesize-detail', args=[value.id]), value)


class DeveloperTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Developer
        fields = ('name', 'for_paper', 'for_film')

    @classmethod
    def render_name(cls, value, record):
        return format_html("<a href=\"{}\">{} {}</a>", reverse('schema:developer-detail', args=[record.slug]), record.manufacturer, value)

    @classmethod
    def render_for_paper(cls, value):
        return format_html(boolicon(value))

    @classmethod
    def render_for_film(cls, value):
        return format_html(boolicon(value))


class EnlargerModelTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = EnlargerModel
        fields = ('model', 'negative_size', 'type')

    @classmethod
    def render_model(cls, value, record):
        return format_html("<a href=\"{}\">{} {}</a>", reverse('schema:enlargermodel-detail', args=[record.slug]), record.manufacturer, value)


class EnlargerTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Enlarger
        fields = ('id_owner', 'enlargermodel')

    @classmethod
    def render_id_owner(cls, value):
        return format_html("<a href=\"{}\">#{}</a>", reverse('schema:enlarger-detail', args=[value]), value)

    @classmethod
    def render_enlargermodel(cls, value, record):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:enlargermodel-detail', args=[record.enlargermodel.slug]), value)


class FilmStockTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = FilmStock
        fields = ('name', 'iso', 'colour', 'panchromatic', 'process')

    @classmethod
    def render_name(cls, value, record):
        return format_html("<a href=\"{}\">{} {}</a>", reverse('schema:filmstock-detail', args=[record.slug]), record.manufacturer, value)

    @classmethod
    def render_colour(cls, value):
        return format_html(colouricon(value))

    @classmethod
    def render_panchromatic(cls, value):
        return format_html(boolicon(value))


class FilterTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Filter
        fields = ('type', 'shortname', 'attenuation')

    @classmethod
    def render_type(cls, value, record):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:filter-detail', args=[record.id]), value)


class FlashModelTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = FlashModel
        fields = ('model', 'guide_number', 'ttl')

    @classmethod
    def render_model(cls, value, record):
        return format_html("<a href=\"{}\">{} {}</a>", reverse('schema:flashmodel-detail', args=[record.slug]), record.manufacturer, value)

    @classmethod
    def render_ttl(cls, value):
        return format_html(boolicon(value))


class FlashTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Flash
        fields = ('id_owner', 'flashmodel')

    @classmethod
    def render_id_owner(cls, value):
        return format_html("<a href=\"{}\">#{}</a>", reverse('schema:flash-detail', args=[value]), value)

    @classmethod
    def render_flashmodel(cls, value, record):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:flashmodel-detail', args=[record.flashmodel.slug]), value)


class FormatTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Format
        fields = ('format',)

    @classmethod
    def render_format(cls, value, record):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:format-detail', args=[record.id]), value)


class LensTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Lens
        fields = ('id_owner', 'lensmodel', 'lensmodel__mount',
                  'serial', 'manufactured', 'own')

    @classmethod
    def render_id_owner(cls, value):
        return format_html("<a href=\"{}\">#{}</a>", reverse('schema:lens-detail', args=[value]), value)

    @classmethod
    def render_lensmodel(cls, value):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:lensmodel-detail', args=[value.slug]), value)

    @classmethod
    def render_lensmodel__mount(cls, value):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:mount-detail', args=[value.slug]), value)

    @classmethod
    def render_serial(cls, value):
        return format_html("<code>{}</code>", value)

    @classmethod
    def render_own(cls, value):
        return format_html(boolicon(value))


class LensModelTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = LensModel
        fields = ('model', 'image', 'mount', 'zoom', 'min_focal_length',
                  'max_aperture', 'autofocus', 'introduced')

    @classmethod
    def render_model(cls, value, record):
        if record.disambiguation:
            mystr = format_html("<a href=\"{}\">{} {} [{}]</a>", reverse('schema:lensmodel-detail', args=[
                record.slug]), record.manufacturer, value, record.disambiguation)
        else:
            mystr = format_html("<a href=\"{}\">{} {}</a>", reverse(
                'schema:lensmodel-detail', args=[record.slug]), record.manufacturer, value)
        if cls.request.user.is_authenticated:
            qty = Lens.objects.filter(
                owner=cls.request.user, lensmodel=record).count()
            if qty > 0:
                badge = format_html(
                    " <span class=\"badge badge-pill badge-primary\">{}</span>", qty)
            else:
                badge = format_html("")
        else:
            badge = format_html("")
        return mystr+badge

    @classmethod
    def render_image(cls, value):
        if value:
            icon = format_html(
                '<img src="/static/svg/camera.svg" width="20" height="20" alt="This lens model has a photo" title="This lens model has a photo">')
        return icon

    @classmethod
    def render_mount(cls, value):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:mount-detail', args=[value.slug]), value)

    @classmethod
    def render_max_aperture(cls, value):
        return format_html("<em>f</em>/{}", value)

    @classmethod
    def render_min_focal_length(cls, record):
        if record.zoom is True:
            mystr = format_html(
                "{}-{}mm", record.min_focal_length, record.max_focal_length)
        elif record.zoom is False:
            mystr = format_html("{}mm", record.min_focal_length)
        else:
            mystr = format_html("?")
        return mystr

    @classmethod
    def render_zoom(cls, value):
        return format_html(boolicon(value))

    @classmethod
    def render_autofocus(cls, value):
        return format_html(boolicon(value))


class ManufacturerTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Manufacturer
        fields = ('name', 'city', 'country', 'founded', 'dissolved')

    @classmethod
    def render_name(cls, value, record):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:manufacturer-detail', args=[record.slug]), value)

    @classmethod
    def render_country(cls, record):
        return format_html("{} <img src=\"{}\">", record.country.name, record.country.flag)


class MountTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Mount
        fields = ('mount', 'shutter_in_lens', 'type', 'purpose')

    @classmethod
    def render_mount(cls, value, record):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:mount-detail', args=[record.slug]), value)

    @classmethod
    def render_shutter_in_lens(cls, value):
        return format_html(boolicon(value))


class MountAdapterTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = MountAdapter
        fields = ('id_owner', 'camera_mount', 'lens_mount',
                  'has_optics', 'infinity_focus')

    @classmethod
    def render_id_owner(cls, value):
        return format_html("<a href=\"{}\">#{}</a>", reverse('schema:mountadapter-detail', args=[value]), value)

    @classmethod
    def render_camera_mount(cls, value):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:mount-detail', args=[value.slug]), value)

    @classmethod
    def render_lens_mount(cls, value):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:mount-detail', args=[value.slug]), value)


class NegativeSizeTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = NegativeSize
        fields = ('name', 'width', 'height',
                  'crop_factor', 'area', 'aspect_ratio')

    @classmethod
    def render_name(cls, value, record):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:negativesize-detail', args=[record.id]), value)

    @classmethod
    def render_width(cls, value):
        return format_html("{}mm", value)

    @classmethod
    def render_height(cls, value):
        return format_html("{}mm", value)

    @classmethod
    def render_crop_factor(cls, value):
        return format_html("{}&times;", value)

    @classmethod
    def render_area(cls, value):
        return format_html("{}mm&sup2;", value)

    @classmethod
    def render_aspect_ratio(cls, value):
        return format_html("{}&times;", value)


class OrderTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Order
        fields = ('id_owner', 'negative', 'width', 'height',
                  'added', 'printed', 'print', 'recipient')

    @classmethod
    def render_id_owner(cls, value):
        return format_html("<a href=\"{}\">#{}</a>", reverse('schema:order-detail', args=[value]), value)


class PaperStockTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = PaperStock
        fields = ('name', 'resin_coated', 'colour', 'finish')

    @classmethod
    def render_name(cls, value, record):
        return format_html("<a href=\"{}\">{} {}</a>", reverse('schema:paperstock-detail', args=[record.id]), record.manufacturer, value)

    @classmethod
    def render_resin_coated(cls, value):
        return format_html(boolicon(value))

    @classmethod
    def render_colour(cls, value):
        return format_html(boolicon(value))


class PersonTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Person
        fields = ('id_owner', 'name')

    @classmethod
    def render_id_owner(cls, value):
        return format_html("<a href=\"{}\">#{}</a>", reverse('schema:person-detail', args=[value]), value)

    @classmethod
    def render_name(cls, value, record):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:person-detail', args=[record.id_owner]), value)


class PrintTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Print
        fields = ('id_owner', 'negative', 'date', 'paper_stock',
                  'width', 'height', 'location', 'archive')

    @classmethod
    def render_id_owner(cls, value):
        return format_html("<a href=\"{}\">#{}</a>", reverse('schema:print-detail', args=[value]), value)

    @classmethod
    def render_negative(cls, value):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:negative-detail', args=[value.slug]), value)


class ProcessTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Process
        fields = ('name', 'colour', 'positive')

    @classmethod
    def render_name(cls, value, record):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:process-detail', args=[record.id]), value)

    @classmethod
    def render_colour(cls, value):
        return format_html(boolicon(value))

    @classmethod
    def render_positive(cls, value):
        return format_html(boolicon(value))


class ScanTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Scan
        fields = ('uuid', 'negative', 'print', 'filename', 'date')

    @classmethod
    def render_uuid(cls, value):
        return format_html("<code><a href=\"{}\">{}</a></code>", reverse('schema:scan-detail', args=[value]), value)

    @classmethod
    def render_negative(cls, value):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:negative-detail', args=[value.slug]), value)

    @classmethod
    def render_print(cls, value):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:print-detail', args=[value.id_owner]), value)

    @classmethod
    def render_filename(cls, value):
        return format_html("<code>{}</code>", value)


class NegativeTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Negative
        fields = ('slug', 'film', 'date', 'lens', 'shutter_speed', 'aperture')

    @classmethod
    def render_slug(cls, value, record):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:negative-detail', args=[value]), record)

    @classmethod
    def render_aperture(cls, value):
        return format_html("<em>f</em>/{}", value)

    @classmethod
    def render_film(cls, value):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:film-detail', args=[value.id_owner]), value)

    @classmethod
    def render_lens(cls, value):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:lens-detail', args=[value.id_owner]), value)

class FilmTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Film
        fields = ('id_owner', 'filmstock', 'format',
                  'status', 'date_processed', 'camera')

    @classmethod
    def render_id_owner(cls, value, record):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:film-detail', args=[value]), record)

    @classmethod
    def render_filmstock(cls, value):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:filmstock-detail', args=[value.slug]), value)

    @classmethod
    def render_format(cls, value):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:format-detail', args=[value.id]), value)

    @classmethod
    def render_camera(cls, value):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:camera-detail', args=[value.id_owner]), value)


class TeleconverterTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Teleconverter
        fields = ('id_owner', 'teleconvertermodel',)

    @classmethod
    def render_id_owner(cls, value):
        return format_html("<a href=\"{}\">#{}</a>", reverse('schema:teleconverter-detail', args=[value]), value)

    @classmethod
    def render_teleconvertermodel(cls, value, record):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:teleconvertermodel-detail', args=[record.teleconvertermodel.slug]), value)


class TeleconverterModelTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = TeleconverterModel
        fields = ('model', 'mount', 'factor')

    @classmethod
    def render_model(cls, value, record):
        if record.manufacturer is not None:
            mystr = format_html("<a href=\"{}\">{} {}</a>", reverse(
                'schema:teleconvertermodel-detail', args=[record.slug]), record.manufacturer, value)
        else:
            mystr = format_html(
                "<a href=\"{}\">{}</a>", reverse('schema:teleconvertermodel-detail', args=[record.slug]), value)
        return mystr

    @classmethod
    def render_factor(cls, value):
        return format_html("{}&times;", value)

    @classmethod
    def render_mount(cls, value):
        return format_html("<a href=\"{}\">{}</a>", reverse('schema:mount-detail', args=[value.slug]), value)

class TonerTable(tables.Table):
    class Meta:
        attrs = {"class": "table table-hover"}
        model = Toner
        fields = ('name', 'formulation', 'stock_dilution')

    @classmethod
    def render_name(cls, value, record):
        return format_html("<a href=\"{}\">{} {}</a>", reverse('schema:toner-detail', args=[record.slug]), record.manufacturer, value)
