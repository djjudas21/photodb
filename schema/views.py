from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from django_tables2 import SingleTableView, RequestConfig
from django_tables2.views import SingleTableMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView

from schema.models import Accessory, Archive, Battery, BulkFilm, Camera, CameraModel, Developer, Enlarger, FilmStock, Filter
from schema.models import Flash, FlashProtocol, Format, Lens, LensModel, Manufacturer
from schema.models import Mount, MountAdapter, NegativeSize, Order, PaperStock, Person, Print, Toning
from schema.models import Process, Repair, Scan, Negative, Film, Series, ShutterSpeed, Teleconverter, Toner

from schema.tables import AccessoryTable, ArchiveTable, BatteryTable, BulkFilmTable, CameraTable, CameraModelTable, DeveloperTable, EnlargerTable, FilmStockTable, FilterTable
from schema.tables import FlashTable, FlashProtocolTable, FormatTable, LensTable, LensModelTable, ManufacturerTable
from schema.tables import MountTable, MountAdapterTable, NegativeSizeTable, OrderTable, PaperStockTable, PersonTable, PrintTable
from schema.tables import ProcessTable, RepairTable, ScanTable, NegativeTable, FilmTable, SeriesTable, TeleconverterTable, TonerTable

from schema.forms import AccessoryForm, ArchiveForm, BatteryForm, BulkFilmForm, CameraForm, CameraModelForm, DeveloperForm, EnlargerForm, FilmStockForm, FilterForm
from schema.forms import FlashForm, FlashProtocolForm, FormatForm, LensForm, LensModelForm, ManufacturerForm
from schema.forms import MountForm, MountAdapterForm, NegativeSizeForm, OrderForm, PaperStockForm, PersonForm, PrintForm
from schema.forms import ProcessForm, RepairForm, ScanForm, NegativeForm, FilmForm, SeriesForm, TeleconverterForm, TonerForm

from schema.filters import AccessoryFilter, BatteryFilter, BulkFilmFilter, CameraFilter, CameraModelFilter, DeveloperFilter
from schema.filters import EnlargerFilter, FilmFilter, FilmStockFilter, FlashFilter, LensFilter, LensModelFilter
from schema.filters import MountAdapterFilter, MountFilter, NegativeFilter, OrderFilter, PaperStockFilter, PrintFilter
from schema.filters import RepairFilter, TeleconverterFilter, TonerFilter

from schema.formhelpers import AccessoryFormHelper, BatteryFormHelper, BulkFilmFormHelper, CameraFormHelper, CameraModelFormHelper
from schema.formhelpers import DeveloperFormHelper, EnlargerFormHelper, FilmFormHelper, FilmStockFormHelper, FlashFormHelper
from schema.formhelpers import LensFormHelper, LensModelFormHelper, MountAdapterFormHelper, MountFormHelper, NegativeFormHelper
from schema.formhelpers import OrderFormHelper, PaperStockFormHelper, PrintFormHelper, RepairFormHelper, TeleconverterFormHelper, TonerFormHelper

from redis_metrics import metric

# Increment the metric by one as a test
metric('new-user-signup')

# Custom class for filtered list views in table format


class PagedFilteredTableView(SingleTableMixin, FilterView):
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'
    form_method = 'POST'
    template_name = 'list.html'
    paginate_by = 25

    def get_queryset(self, **kwargs):
        qs = super(PagedFilteredTableView, self).get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs

 #   def get_table(self, **kwargs):
 #       table = super(PagedFilteredTableView, self).get_table()
 #       RequestConfig(self.request, paginate={'page': self.kwargs['page'],
 #                           "per_page": self.paginate_by}).configure(table)
 #       return table

    def get_context_data(self, **kwargs):
        context = super(PagedFilteredTableView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        return context

# Custom class for displaying a list view in table format


class SingleTableListView(SingleTableView):
    template_name = 'list.html'


class AccessoryList(LoginRequiredMixin, PagedFilteredTableView):
    model = Accessory
    table_class = AccessoryTable
    filter_class = AccessoryFilter
    formhelper_class = AccessoryFormHelper


class AccessoryDetail(LoginRequiredMixin, generic.DetailView):
    model = Accessory


class AccessoryCreate(LoginRequiredMixin, CreateView):
    model = Accessory
    form_class = AccessoryForm
    template_name = 'create.html'


class AccessoryUpdate(LoginRequiredMixin, UpdateView):
    model = Accessory
    form_class = AccessoryForm
    template_name = 'update.html'


class ArchiveList(LoginRequiredMixin, SingleTableListView):
    model = Archive
    table_class = ArchiveTable


class ArchiveDetail(LoginRequiredMixin, generic.DetailView):
    model = Archive


class ArchiveCreate(LoginRequiredMixin, CreateView):
    model = Archive
    form_class = ArchiveForm
    template_name = 'create.html'


class ArchiveUpdate(LoginRequiredMixin, UpdateView):
    model = Archive
    form_class = ArchiveForm
    template_name = 'update.html'


class BatteryList(PagedFilteredTableView):
    model = Battery
    table_class = BatteryTable
    filter_class = BatteryFilter
    formhelper_class = BatteryFormHelper


class BatteryDetail(generic.DetailView):
    model = Battery


class BatteryCreate(LoginRequiredMixin, CreateView):
    model = Battery
    form_class = BatteryForm
    template_name = 'create.html'


class BatteryUpdate(LoginRequiredMixin, UpdateView):
    model = Battery
    form_class = BatteryForm
    template_name = 'update.html'


class BulkFilmList(LoginRequiredMixin, PagedFilteredTableView):
    model = BulkFilm
    table_class = BulkFilmTable
    filter_class = BulkFilmFilter
    formhelper_class = BulkFilmFormHelper


class BulkFilmDetail(LoginRequiredMixin, generic.DetailView):
    model = BulkFilm


class BulkFilmCreate(LoginRequiredMixin, CreateView):
    model = BulkFilm
    form_class = BulkFilmForm
    template_name = 'create.html'


class BulkFilmUpdate(LoginRequiredMixin, UpdateView):
    model = BulkFilm
    form_class = BulkFilmForm
    template_name = 'update.html'


class CameraList(LoginRequiredMixin, PagedFilteredTableView):
    model = Camera
    table_class = CameraTable
    filter_class = CameraFilter
    formhelper_class = CameraFormHelper


class CameraDetail(LoginRequiredMixin, generic.DetailView):
    model = Camera


class CameraCreate(LoginRequiredMixin, CreateView):
    model = Camera
    form_class = CameraForm
    template_name = 'create.html'


class CameraUpdate(LoginRequiredMixin, UpdateView):
    model = Camera
    form_class = CameraForm
    template_name = 'update.html'


class CameraModelList(PagedFilteredTableView):
    model = CameraModel
    table_class = CameraModelTable
    filter_class = CameraModelFilter
    formhelper_class = CameraModelFormHelper


class CameraModelDetail(generic.DetailView):
    model = CameraModel


class CameraModelCreate(LoginRequiredMixin, CreateView):
    model = CameraModel
    form_class = CameraModelForm
    template_name = 'create.html'


class CameraModelUpdate(LoginRequiredMixin, UpdateView):
    model = CameraModel
    form_class = CameraModelForm
    template_name = 'update.html'


class DeveloperList(PagedFilteredTableView):
    model = Developer
    table_class = DeveloperTable
    filter_class = DeveloperFilter
    formhelper_class = DeveloperFormHelper


class DeveloperDetail(generic.DetailView):
    model = Developer


class DeveloperCreate(LoginRequiredMixin, CreateView):
    model = Developer
    form_class = DeveloperForm
    template_name = 'create.html'


class DeveloperUpdate(LoginRequiredMixin, UpdateView):
    model = Developer
    form_class = DeveloperForm
    template_name = 'update.html'


class EnlargerList(LoginRequiredMixin, PagedFilteredTableView):
    model = Enlarger
    table_class = EnlargerTable
    filter_class = EnlargerFilter
    formhelper_class = EnlargerFormHelper


class EnlargerDetail(LoginRequiredMixin, generic.DetailView):
    model = Enlarger


class EnlargerCreate(LoginRequiredMixin, CreateView):
    model = Enlarger
    form_class = EnlargerForm
    template_name = 'create.html'


class EnlargerUpdate(LoginRequiredMixin, UpdateView):
    model = Enlarger
    form_class = EnlargerForm
    template_name = 'update.html'


class FilmStockList(PagedFilteredTableView):
    model = FilmStock
    table_class = FilmStockTable
    filter_class = FilmStockFilter
    formhelper_class = FilmStockFormHelper


class FilmStockDetail(generic.DetailView):
    model = FilmStock


class FilmStockCreate(LoginRequiredMixin, CreateView):
    model = FilmStock
    form_class = FilmStockForm
    template_name = 'create.html'


class FilmStockUpdate(LoginRequiredMixin, UpdateView):
    model = FilmStock
    form_class = FilmStockForm
    template_name = 'update.html'


class FilterList(SingleTableListView):
    model = Filter
    table_class = FilterTable


class FilterDetail(generic.DetailView):
    model = Filter


class FilterCreate(LoginRequiredMixin, CreateView):
    model = Filter
    form_class = FilterForm
    template_name = 'create.html'


class FilterUpdate(LoginRequiredMixin, UpdateView):
    model = Filter
    form_class = FilterForm
    template_name = 'update.html'


class FlashList(LoginRequiredMixin, PagedFilteredTableView):
    model = Flash
    table_class = FlashTable
    filter_class = FlashFilter
    formhelper_class = FlashFormHelper


class FlashDetail(LoginRequiredMixin, generic.DetailView):
    model = Flash


class FlashCreate(LoginRequiredMixin, CreateView):
    model = Flash
    form_class = FlashForm
    template_name = 'create.html'


class FlashUpdate(LoginRequiredMixin, UpdateView):
    model = Flash
    form_class = FlashForm
    template_name = 'update.html'


class FlashProtocolList(SingleTableListView):
    model = FlashProtocol
    table_class = FlashProtocolTable


class FlashProtocolDetail(generic.DetailView):
    model = FlashProtocol


class FlashProtocolCreate(LoginRequiredMixin, CreateView):
    model = FlashProtocol
    form_class = FlashProtocolForm
    template_name = 'create.html'


class FlashProtocolUpdate(LoginRequiredMixin, UpdateView):
    model = FlashProtocol
    form_class = FlashProtocolForm
    template_name = 'update.html'


class FormatList(SingleTableListView):
    model = Format
    table_class = FormatTable


class FormatDetail(generic.DetailView):
    model = Format


class FormatCreate(LoginRequiredMixin, CreateView):
    model = Format
    form_class = FormatForm
    template_name = 'create.html'


class FormatUpdate(LoginRequiredMixin, UpdateView):
    model = Format
    form_class = FormatForm
    template_name = 'update.html'


class LensList(LoginRequiredMixin, PagedFilteredTableView):
    model = Lens
    table_class = LensTable
    filter_class = LensFilter
    formhelper_class = LensFormHelper


class LensDetail(LoginRequiredMixin, generic.DetailView):
    model = Lens


class LensCreate(LoginRequiredMixin, CreateView):
    model = Lens
    form_class = LensForm
    template_name = 'create.html'


class LensUpdate(LoginRequiredMixin, UpdateView):
    model = Lens
    form_class = LensForm
    template_name = 'update.html'


class LensModelList(PagedFilteredTableView):
    model = LensModel
    table_class = LensModelTable
    filter_class = LensModelFilter
    formhelper_class = LensModelFormHelper


class LensModelDetail(generic.DetailView):
    model = LensModel


class LensModelCreate(LoginRequiredMixin, CreateView):
    model = LensModel
    form_class = LensModelForm
    template_name = 'create.html'


class LensModelUpdate(LoginRequiredMixin, UpdateView):
    model = LensModel
    form_class = LensModelForm
    template_name = 'update.html'


class ManufacturerList(SingleTableListView):
    model = Manufacturer
    table_class = ManufacturerTable


class ManufacturerDetail(generic.DetailView):
    model = Manufacturer


class ManufacturerCreate(LoginRequiredMixin, CreateView):
    model = Manufacturer
    form_class = ManufacturerForm
    template_name = 'create.html'


class ManufacturerUpdate(LoginRequiredMixin, UpdateView):
    model = Manufacturer
    form_class = ManufacturerForm
    template_name = 'update.html'


class MountList(PagedFilteredTableView):
    model = Mount
    table_class = MountTable
    filter_class = MountFilter
    formhelper_class = MountFormHelper


class MountDetail(generic.DetailView):
    model = Mount


class MountCreate(LoginRequiredMixin, CreateView):
    model = Mount
    form_class = MountForm
    template_name = 'create.html'


class MountUpdate(LoginRequiredMixin, UpdateView):
    model = Mount
    form_class = MountForm
    template_name = 'update.html'


class MountAdapterList(LoginRequiredMixin, PagedFilteredTableView):
    model = MountAdapter
    table_class = MountAdapterTable
    filter_class = MountAdapterFilter
    formhelper_class = MountAdapterFormHelper


class MountAdapterDetail(LoginRequiredMixin, generic.DetailView):
    model = MountAdapter


class MountAdapterCreate(LoginRequiredMixin, CreateView):
    model = MountAdapter
    form_class = MountAdapterForm
    template_name = 'create.html'


class MountAdapterUpdate(LoginRequiredMixin, UpdateView):
    model = MountAdapter
    form_class = MountAdapterForm
    template_name = 'update.html'


class NegativeSizeList(SingleTableListView):
    model = NegativeSize
    table_class = NegativeSizeTable


class NegativeSizeDetail(generic.DetailView):
    model = NegativeSize


class NegativeSizeCreate(LoginRequiredMixin, CreateView):
    model = NegativeSize
    form_class = NegativeSizeForm
    template_name = 'create.html'


class NegativeSizeUpdate(LoginRequiredMixin, UpdateView):
    model = NegativeSize
    form_class = NegativeSizeForm
    template_name = 'update.html'


class OrderList(LoginRequiredMixin, PagedFilteredTableView):
    model = Order
    table_class = OrderTable
    filter_class = OrderFilter
    formhelper_class = OrderFormHelper


class OrderDetail(LoginRequiredMixin, generic.DetailView):
    model = Order


class OrderCreate(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'create.html'


class OrderUpdate(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'update.html'


class PaperStockList(PagedFilteredTableView):
    model = PaperStock
    table_class = PaperStockTable
    filter_class = PaperStockFilter
    formhelper_class = PaperStockFormHelper


class PaperStockDetail(generic.DetailView):
    model = PaperStock


class PaperStockCreate(LoginRequiredMixin, CreateView):
    model = PaperStock
    form_class = PaperStockForm
    template_name = 'create.html'


class PaperStockUpdate(LoginRequiredMixin, UpdateView):
    model = PaperStock
    form_class = PaperStockForm
    template_name = 'update.html'


class PersonList(LoginRequiredMixin, SingleTableListView):
    model = Person
    table_class = PersonTable

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Person.objects.filter(owner=self.request.user)
        else:
            return Person.objects.none()


class PersonDetail(LoginRequiredMixin, generic.DetailView):
    model = Person


class PersonCreate(LoginRequiredMixin, CreateView):
    model = Person
    form_class = PersonForm
    template_name = 'create.html'


class PersonUpdate(LoginRequiredMixin, UpdateView):
    model = Person
    form_class = PersonForm
    template_name = 'update.html'


class PrintList(LoginRequiredMixin, PagedFilteredTableView):
    model = Print
    table_class = PrintTable
    filter_class = PrintFilter
    formhelper_class = PrintFormHelper


class PrintDetail(LoginRequiredMixin, generic.DetailView):
    model = Print


class PrintCreate(LoginRequiredMixin, CreateView):
    model = Print
    form_class = PrintForm
    template_name = 'create.html'


class PrintUpdate(LoginRequiredMixin, UpdateView):
    model = Print
    form_class = PrintForm
    template_name = 'update.html'


class ProcessList(SingleTableListView):
    model = Process
    table_class = ProcessTable


class ProcessDetail(generic.DetailView):
    model = Process


class ProcessCreate(LoginRequiredMixin, CreateView):
    model = Process
    form_class = ProcessForm
    template_name = 'create.html'


class ProcessUpdate(LoginRequiredMixin, UpdateView):
    model = Process
    form_class = ProcessForm
    template_name = 'update.html'


class RepairList(LoginRequiredMixin, PagedFilteredTableView):
    model = Repair
    table_class = RepairTable
    filter_class = RepairFilter
    formhelper_class = RepairFormHelper


class RepairDetail(LoginRequiredMixin, generic.DetailView):
    model = Repair


class RepairCreate(LoginRequiredMixin, CreateView):
    model = Repair
    form_class = RepairForm
    template_name = 'create.html'


class RepairUpdate(LoginRequiredMixin, UpdateView):
    model = Repair
    form_class = RepairForm
    template_name = 'update.html'


class ScanList(LoginRequiredMixin, SingleTableListView):
    model = Scan
    table_class = ScanTable

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Scan.objects.filter(owner=self.request.user)
        else:
            return Scan.objects.none()


class ScanDetail(LoginRequiredMixin, generic.DetailView):
    model = Scan


class ScanCreate(LoginRequiredMixin, CreateView):
    model = Scan
    form_class = ScanForm
    template_name = 'create.html'


class ScanUpdate(LoginRequiredMixin, UpdateView):
    model = Scan
    form_class = ScanForm
    template_name = 'update.html'


class NegativeList(LoginRequiredMixin, PagedFilteredTableView):
    model = Negative
    table_class = NegativeTable
    filter_class = NegativeFilter
    formhelper_class = NegativeFormHelper


class NegativeDetail(LoginRequiredMixin, generic.DetailView):
    model = Negative


class NegativeCreate(LoginRequiredMixin, CreateView):
    model = Negative
    form_class = NegativeForm
    template_name = 'create.html'


class NegativeUpdate(LoginRequiredMixin, UpdateView):
    model = Negative
    form_class = NegativeForm
    template_name = 'update.html'


class FilmList(LoginRequiredMixin, PagedFilteredTableView):
    model = Film
    table_class = FilmTable
    filter_class = FilmFilter
    formhelper_class = FilmFormHelper


class FilmDetail(LoginRequiredMixin, generic.DetailView):
    model = Film


class FilmCreate(LoginRequiredMixin, CreateView):
    model = Film
    form_class = FilmForm
    template_name = 'create.html'


class FilmUpdate(LoginRequiredMixin, UpdateView):
    model = Film
    form_class = FilmForm
    template_name = 'update.html'


class SeriesList(LoginRequiredMixin, SingleTableListView):
    model = Series
    table_class = SeriesTable

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Series.objects.filter(owner=self.request.user)
        else:
            return Series.objects.none()


class SeriesDetail(LoginRequiredMixin, generic.DetailView):
    model = Series


class SeriesCreate(LoginRequiredMixin, CreateView):
    model = Series
    form_class = SeriesForm
    template_name = 'create.html'


class SeriesUpdate(LoginRequiredMixin, UpdateView):
    model = Series
    form_class = SeriesForm
    template_name = 'update.html'


class TeleconverterList(LoginRequiredMixin, PagedFilteredTableView):
    model = Teleconverter
    table_class = TeleconverterTable
    filter_class = TeleconverterFilter
    formhelper_class = TeleconverterFormHelper


class TeleconverterDetail(LoginRequiredMixin, generic.DetailView):
    model = Teleconverter


class TeleconverterCreate(LoginRequiredMixin, CreateView):
    model = Teleconverter
    form_class = TeleconverterForm
    template_name = 'create.html'


class TeleconverterUpdate(LoginRequiredMixin, UpdateView):
    model = Teleconverter
    form_class = TeleconverterForm
    template_name = 'update.html'


class TonerList(PagedFilteredTableView):
    model = Toner
    table_class = TonerTable
    filter_class = TonerFilter
    formhelper_class = TonerFormHelper


class TonerDetail(generic.DetailView):
    model = Toner


class TonerCreate(LoginRequiredMixin, CreateView):
    model = Toner
    form_class = TonerForm
    template_name = 'create.html'


class TonerUpdate(LoginRequiredMixin, UpdateView):
    model = Toner
    form_class = TonerForm
    template_name = 'update.html'


class StatsView(TemplateView):
    template_name = "stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_camera_models'] = CameraModel.objects.count
        context['num_lens_models'] = LensModel.objects.count
        context['num_filmstocks'] = FilmStock.objects.count
        return context
