# Generated by Django 2.1.10 on 2019-08-13 14:11

from django.db import migrations

def forwards_func(apps, schema_editor):
  # We get the model from the versioned app registry;
  # if we directly import it, it'll be the wrong version
  db_alias = schema_editor.connection.alias

  AccessoryType = apps.get_model("schema", "AccessoryType")
  AccessoryType.objects.using(db_alias).bulk_create([
    AccessoryType(type="Power winder"),
    AccessoryType(type="Battery grip"),
    AccessoryType(type="Viewfinder"),
    AccessoryType(type="Focusing screen"),
    AccessoryType(type="Film back"),
    AccessoryType(type="Lens hood"),
    AccessoryType(type="Case"),
    AccessoryType(type="Lens cap"),
  ])

  ArchiveType = apps.get_model("schema", "ArchiveType")
  ArchiveType.objects.using(db_alias).bulk_create([
    ArchiveType(type="Film"),
    ArchiveType(type="Slide"),
    ArchiveType(type="Print"),
  ])

  BodyType = apps.get_model("schema", "BodyType")
  BodyType.objects.using(db_alias).bulk_create([
    BodyType(type="Box camera"),
    BodyType(type="Compact camera"),
    BodyType(type="Folding camera"),
    BodyType(type="SLR"),
    BodyType(type="TLR"),
    BodyType(type="Bridge camera"),
    BodyType(type="View camera"),
    BodyType(type="Pistol grip camera"),
  ])

  Condition = apps.get_model("schema", "Condition")
  Condition.objects.using(db_alias).bulk_create([
      Condition(code="NEW", name="Brand new", min_rating="100", max_rating="100", description="Never used and still sealed. All original packaging, manuals and accessories included."),
      Condition(code="MINT", name="Like new", min_rating="97", max_rating="99", description="Basically new with very little use.  All boxes and original packaging"),
      Condition(code="EXC+", name="Excellent Plus", min_rating="90", max_rating="96", description="Lens Glass very clean – cosmetically may show very slight wear and/or signs of use but only under very close inspection."),
      Condition(code="EXC", name="Excellent", min_rating="84", max_rating="89", description="Shows slight signs of use – Lens Glass is very clean but may have some dust which will not affect picture quality."),
      Condition(code="GOOD", name="Good", min_rating="75", max_rating="83", description="Appears well used and may include dings, brassing, scrapes and bruises but is in fully functional condition. Glass may have cleaning marks or small scratches which won’t affect picture quality."),
      Condition(code="FAIR", name="Fair", min_rating="60", max_rating="74", description="Appears to have been used very heavily with multiple dings, scrapes, scratches and heavy brassing. Lens Glass may have slight fungus, excessive dust and/or scratches that will likely affect picture quality."),
      Condition(code="POOR", name="Poor", min_rating="50", max_rating="59", description="Very rough looking. Multiple impressions metal, extreme finish loss and excessive brassing. Glass will have marks, fungus and/or haze which will affect picture quality"),
      Condition(code="BROKEN", name="Broken", min_rating="0", max_rating="49", description="Has one or more faults")
  ])

  ExposureProgram = apps.get_model("schema", "ExposureProgram")
  ExposureProgram.objects.using(db_alias).bulk_create([
    ExposureProgram(name="Fixed"),
    ExposureProgram(name="Manual"),
    ExposureProgram(name="Program AE"),
    ExposureProgram(name="Aperture-priority AE"),
    ExposureProgram(name="Shutter speed priority AE"),
    ExposureProgram(name="Creative (Slow speed)"),
    ExposureProgram(name="Action (High speed)"),
    ExposureProgram(name="Portrait"),
    ExposureProgram(name="Landscape"),
    ExposureProgram(name="Bulb"),
  ])

  FocusType = apps.get_model("schema", "FocusType")
  FocusType.objects.using(db_alias).bulk_create([
    FocusType(name="Autofocus"),
    FocusType(name="Fixed focus"),
    FocusType(name="Zone focus"),
    FocusType(name="Rangefinder"),
    FocusType(name="SLR"),
    FocusType(name="TLR"),
    FocusType(name="View camera"),
  ])

  MeteringMode = apps.get_model("schema", "MeteringMode")
  MeteringMode.objects.using(db_alias).bulk_create([
    MeteringMode(name="None"),
    MeteringMode(name="Average"),
    MeteringMode(name="Center-weighted Average"),
    MeteringMode(name="Spot"),
    MeteringMode(name="Multi-spot"),
    MeteringMode(name="Multi-segment"),
    MeteringMode(name="Partial"),
  ])

  MeteringType = apps.get_model("schema", "MeteringType")
  MeteringType.objects.using(db_alias).bulk_create([
    MeteringType(name="Cadmium sulphide (CdS)"),
    MeteringType(name="Selenium"),
    MeteringType(name="Silicon"),
  ])

  Process = apps.get_model("schema", "Process")
  Process.objects.using(db_alias).bulk_create([
    Process(name="Black & white negative"),
    Process(name="Black & white reversal"),
    Process(name="C-41"),
    Process(name="E-6"),
    Process(name="Polaroid"),
    Process(name="K-14"),
    Process(name="Cyanotype"),
  ])

  ShutterType = apps.get_model("schema", "ShutterType")
  ShutterType.objects.using(db_alias).bulk_create([
    ShutterType(type="Focal plane (horizontal travel)"),
    ShutterType(type="Focal plane (vertical travel)"),
    ShutterType(type="Leaf"),
    ShutterType(type="Rotary"),
    ShutterType(type="Sliding"),
    ShutterType(type="Ball bearing"),
    ShutterType(type="Electronic"),
  ])

  
def reverse_func(apps, schema_editor):
  db_alias = schema_editor.connection.alias

  AccessoryType = apps.get_model("schema", "AccessoryType")
  AccessoryType.objects.using(db_alias).filter(type="Power winder")
  AccessoryType.objects.using(db_alias).filter(type="Battery grip")
  AccessoryType.objects.using(db_alias).filter(type="Viewfinder")
  AccessoryType.objects.using(db_alias).filter(type="Focusing screen")
  AccessoryType.objects.using(db_alias).filter(type="Film back")
  AccessoryType.objects.using(db_alias).filter(type="Lens hood")
  AccessoryType.objects.using(db_alias).filter(type="Case")
  AccessoryType.objects.using(db_alias).filter(type="Lens cap")

  ArchiveType = apps.get_model("schema", "ArchiveType")
  ArchiveType.objects.using(db_alias).filter(type="Film")
  ArchiveType.objects.using(db_alias).filter(type="Slide")
  ArchiveType.objects.using(db_alias).filter(type="Print")

  BodyType = apps.get_model("schema", "BodyType")
  BodyType.objects.using(db_alias).filter(type="Box camera")
  BodyType.objects.using(db_alias).filter(type="Compact camera")
  BodyType.objects.using(db_alias).filter(type="Folding camera")
  BodyType.objects.using(db_alias).filter(type="SLR")
  BodyType.objects.using(db_alias).filter(type="TLR")
  BodyType.objects.using(db_alias).filter(type="Bridge camera")
  BodyType.objects.using(db_alias).filter(type="View camera")
  BodyType.objects.using(db_alias).filter(type="Pistol grip camera")
  
  Condition = apps.get_model("schema", "Condition")
  Condition.objects.using(db_alias).filter(code="NEW")
  Condition.objects.using(db_alias).filter(code="MINT")
  Condition.objects.using(db_alias).filter(code="EXC+")
  Condition.objects.using(db_alias).filter(code="EXC")
  Condition.objects.using(db_alias).filter(code="GOOD")
  Condition.objects.using(db_alias).filter(code="FAIR")
  Condition.objects.using(db_alias).filter(code="POOR")
  Condition.objects.using(db_alias).filter(code="BROKEN")

  ExposureProgram = apps.get_model("schema", "ExposureProgram")
  ExposureProgram.objects.using(db_alias).filter(name="Fixed"),
  ExposureProgram.objects.using(db_alias).filter(name="Manual"),
  ExposureProgram.objects.using(db_alias).filter(name="Program AE"),
  ExposureProgram.objects.using(db_alias).filter(name="Aperture-priority AE"),
  ExposureProgram.objects.using(db_alias).filter(name="Shutter speed priority AE"),
  ExposureProgram.objects.using(db_alias).filter(name="Creative (Slow speed)"),
  ExposureProgram.objects.using(db_alias).filter(name="Action (High speed)"),
  ExposureProgram.objects.using(db_alias).filter(name="Portrait"),
  ExposureProgram.objects.using(db_alias).filter(name="Landscape"),
  ExposureProgram.objects.using(db_alias).filter(name="Bulb"),

  FocusType = apps.get_model("schema", "FocusType")
  FocusType.objects.using(db_alias).filter(name="Autofocus"),
  FocusType.objects.using(db_alias).filter(name="Fixed focus"),
  FocusType.objects.using(db_alias).filter(name="Zone focus"),
  FocusType.objects.using(db_alias).filter(name="Rangefinder"),
  FocusType.objects.using(db_alias).filter(name="SLR"),
  FocusType.objects.using(db_alias).filter(name="TLR"),
  FocusType.objects.using(db_alias).filter(name="View camera"),

  MeteringMode = apps.get_model("schema", "MeteringMode")
  MeteringMode.objects.using(db_alias).filter(name="None"),
  MeteringMode.objects.using(db_alias).filter(name="Average"),
  MeteringMode.objects.using(db_alias).filter(name="Center-weighted Average"),
  MeteringMode.objects.using(db_alias).filter(name="Spot"),
  MeteringMode.objects.using(db_alias).filter(name="Multi-spot"),
  MeteringMode.objects.using(db_alias).filter(name="Multi-segment"),
  MeteringMode.objects.using(db_alias).filter(name="Partial"),

  MeteringType = apps.get_model("schema", "MeteringType")
  MeteringType.objects.using(db_alias).filter(name="Cadmium sulphide (CdS)"),
  MeteringType.objects.using(db_alias).filter(name="Selenium"),
  MeteringType.objects.using(db_alias).filter(name="Silicon"),

  Process = apps.get_model("schema", "Process")
  Process.objects.using(db_alias).filter(name="Black & white negative"),
  Process.objects.using(db_alias).filter(name="Black & white reversal"),
  Process.objects.using(db_alias).filter(name="C-41"),
  Process.objects.using(db_alias).filter(name="E-6"),
  Process.objects.using(db_alias).filter(name="Polaroid"),
  Process.objects.using(db_alias).filter(name="K-14"),
  Process.objects.using(db_alias).filter(name="Cyanotype"),

  ShutterType = apps.get_model("schema", "ShutterType")
  ShutterType.objects.using(db_alias).filter(type="Focal plane (horizontal travel)"),
  ShutterType.objects.using(db_alias).filter(type="Focal plane (vertical travel)"),
  ShutterType.objects.using(db_alias).filter(type="Leaf"),
  ShutterType.objects.using(db_alias).filter(type="Rotary"),
  ShutterType.objects.using(db_alias).filter(type="Sliding"),
  ShutterType.objects.using(db_alias).filter(type="Ball bearing"),
  ShutterType.objects.using(db_alias).filter(type="Electronic"),

  

class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0009_auto_20190813_1338'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
