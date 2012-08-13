from django import forms
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Max
from django.template.defaultfilters import slugify
from django.utils import timezone

from django.contrib.auth.models import User

from jsonfield import JSONField


class Survey(models.Model):
    
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="surveys")
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    published = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.pk:
            self.updated = timezone.now()
        return super(Survey, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("formly_dt_survey_detail", kwargs={"pk": self.pk})
    
    def duplicate(self): # @@@ This could like use with some refactoring
        survey = Survey.objects.get(pk=self.pk)
        survey.pk = None
        survey.save()
        survey.pages.all().delete()
        
        pages = {}
        page_targets = []
        choice_targets = []
        
        for page in Survey.objects.get(pk=self.pk).pages.all():
            orig_page_target = page.target
            orig_page_pk = page.pk
            page.pk = None
            page.survey = survey
            page.target = None
            page.save()
            pages[orig_page_pk] = page
            if orig_page_target:
                page_targets.append({
                    "page": page,
                    "orig_target_pk": orig_page_target.pk
                })
            for field in Page.objects.get(pk=orig_page_pk).fields.all():
                orig_field_pk = field.pk
                field.pk = None
                field.survey = survey
                field.page = page
                field.save()
                for choice in Field.objects.get(pk=orig_field_pk).choices.all():
                    orig_target = choice.target
                    choice.pk = None
                    choice.field = field
                    choice.target = None
                    choice.save()
                    if orig_target:
                        choice_targets.append({
                            "choice": choice,
                            "orig_target_pk": orig_target.pk
                        })
        
        for page_target in page_targets:
            page = page_target["page"]
            page.target = pages[page_target["orig_target_pk"]]
            page.save()
        for choice_target in choice_targets:
            choice = choice_target["choice"]
            choice.target = pages[choice_target["orig_target_pk"]]
            choice.save()
        
        return survey
    
    @property
    def fields(self):
        for page in self.pages.all():
            for field in page.fields.all():
                yield field
    
    def next_page(self, user):
        return self.first_page().next_page(user=user)
    
    def first_page(self):
        if self.pages.count() == 0:
            self.pages.create()
        return self.pages.all()[0]
    
    def publish(self):
        self.published = timezone.now()
        self.save()


class Page(models.Model):
    survey = models.ForeignKey(Survey, related_name="pages")
    page_num = models.PositiveIntegerField(null=True, blank=True)
    subtitle = models.CharField(max_length=255, blank=True)
    # Should be null when a FieldChoice on it's last field has a target.
    target = models.ForeignKey("self", null=True, blank=True)
    
    class Meta:
        unique_together = [
            ("survey", "page_num")
        ]
        ordering = ["survey", "page_num"]
    
    def save(self, *args, **kwargs):
        if self.page_num is None:
            max_page = self.survey.pages.aggregate(Max("page_num"))
            self.page_num = (max_page.get("page_num__max") or 0) + 1
        return super(Page, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.label()
    
    def label(self):
        if self.subtitle:
            return self.subtitle
        else:
            return "Page %d" % self.page_num
    
    def get_absolute_url(self):
        return reverse("formly_dt_page_update", kwargs={"pk": self.pk})
    
    def next_page(self, user):
        target = self
        
        if self.completed(user=user):
            try:
                target = self.survey.pages.get(
                    page_num=self.page_num + 1
                )
            except Page.DoesNotExist:
                target = None
            
            if self.target:
                target = self.target
            
            # Choice target resolved first
            choice_results = self.results.filter(
                question__field_type__in=[
                    Field.RADIO_CHOICES,
                    Field.SELECT_FIELD,
                    Field.CHECKBOX_FIELD,
                ],
                result__user=user
            )
            choice_targets = FieldChoice.objects.filter(
                pk__in=[
                    int(x.answer)
                    for x in choice_results
                    if not isinstance(x.answer, (list, dict))
                ],
                target__isnull=False
            )
            if choice_targets.count() > 0:
                # Use the first one it finds for lack of a better directive
                target = choice_targets[0].target
            
            if target and target.completed(user=user):
                target = target.next_page(user=user)
        
        return target
    
    def completed(self, user):
        return self.results.filter(result__user=user).count() > 0
    
    def is_last_page(self):
        return self.next_page() is None


class Field(models.Model):
    TEXT_FIELD = 0
    TEXT_AREA = 1
    RADIO_CHOICES = 2
    DATE_FIELD = 3
    SELECT_FIELD = 4
    CHECKBOX_FIELD = 5
    MEDIA_FIELD = 6
    BOOLEAN_FIELD = 7
    
    FIELD_TYPE_CHOICES = [
        (TEXT_FIELD, "text field"),
        (TEXT_AREA, "textarea"),
        (RADIO_CHOICES, "radio choices"),
        (SELECT_FIELD, "dropdown field"),
        (CHECKBOX_FIELD, "checkbox field (can select multiple answers"),
        (DATE_FIELD, "date field"),
        (MEDIA_FIELD, "media upload field"),
        (BOOLEAN_FIELD, "boolean field")
    ]
    
    survey = models.ForeignKey(Survey, related_name="fields") # Denorm
    page = models.ForeignKey(Page, related_name="fields")
    label = models.CharField(max_length=100)
    field_type = models.IntegerField(choices=FIELD_TYPE_CHOICES)
    help_text = models.CharField(max_length=255, blank=True)
    ordinal = models.IntegerField()
    # Should this be moved to a separate Constraint model that can also
    # represent cross field constraints
    required = models.BooleanField()
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.ordinal = (self.page.fields.aggregate(
                Max("ordinal")
            )["ordinal__max"] or 0) + 1
        return super(Field, self).save(*args, **kwargs)
    
    def move_up(self):
        try:
            other_field = self.page.fields.order_by("-ordinal").filter(
                ordinal__lt=self.ordinal
            )[0]
            existing = self.ordinal
            other = other_field.ordinal
            self.ordinal = other
            other_field.ordinal = existing
            other_field.save()
            self.save()
        except IndexError:
            return
    
    def move_down(self):
        try:
            other_field = self.page.fields.order_by("ordinal").filter(
                ordinal__gt=self.ordinal
            )[0]
            existing = self.ordinal
            other = other_field.ordinal
            self.ordinal = other
            other_field.ordinal = existing
            other_field.save()
            self.save()
        except IndexError:
            return
    
    class Meta:
        unique_together = [
            ("page", "label")
        ]
        ordering = ["ordinal"]
        
    def __unicode__(self):
        return "%s of type %s on %s" % (
            self.label, self.get_field_type_display(), self.survey
        )
    
    def get_absolute_url(self):
        return reverse("formly_dt_field_update", kwargs={"pk": self.pk})
    
    @property
    def needs_choices(self):
        return self.field_type in [
            Field.RADIO_CHOICES,
            Field.SELECT_FIELD,
            Field.CHECKBOX_FIELD
        ]
    
    @property
    def name(self):
        return slugify(self.label)
    
    def form_field(self):
        choices = [(x.pk, x.label) for x in self.choices.all()]
        kwargs = dict(
            label=self.label,
            help_text=self.help_text,
            required=self.required
        )
        field_class = forms.CharField
        
        if self.field_type == Field.TEXT_AREA:
            kwargs.update({"widget": forms.Textarea()})
        elif self.field_type == Field.RADIO_CHOICES:
            field_class = forms.ChoiceField
            kwargs.update({"widget": forms.RadioSelect(), "choices": choices})
        elif self.field_type == Field.DATE_FIELD:
            field_class = forms.DateField
        elif self.field_type == Field.SELECT_FIELD:
            field_class = forms.ChoiceField
            kwargs.update({"widget": forms.Select(), "choices": choices})
        elif self.field_type == Field.CHECKBOX_FIELD:
            field_class = forms.MultipleChoiceField
            kwargs.update({"widget": forms.CheckboxInput(), "choices": choices})
        elif self.field_type == Field.BOOLEAN_FIELD:
            field_class = forms.BooleanField
        elif self.field_type == Field.MEDIA_FIELD:
            field_class = forms.FileField
        
        return field_class(**kwargs)


class FieldChoice(models.Model):
    field = models.ForeignKey(Field, related_name="choices")
    label = models.CharField(max_length=100)
    target = models.ForeignKey(Page, null=True, blank=True)
    
    def __unicode__(self):
        return self.label


class SurveyResult(models.Model):
    survey = models.ForeignKey(Survey, related_name="survey_results")
    user = models.ForeignKey(User, related_name="survey_results")
    date_submitted = models.DateTimeField(default=timezone.now)
    
    def get_absolute_url(self):
        return reverse("survey_edit", kwargs={"pk": self.pk, "page": 1})


class FieldResult(models.Model):
    survey = models.ForeignKey(Survey, related_name="results") # Denorm
    page = models.ForeignKey(Page, related_name="results") # Denorm
    result = models.ForeignKey(SurveyResult, related_name="results")
    question = models.ForeignKey(Field, related_name="results")
    upload = models.FileField(upload_to="formly/", blank=True)
    answer = JSONField(blank=True) # @@@ I think this should be something different than a string
    
    def answer_value(self):
        if self.answer:
            return self.answer.get("answer")
    
    def answer_display(self):
        val = self.answer_value()
        if val and self.question.needs_choices:
            return FieldChoice.objects.get(pk=int(val))
        return val
    
    class Meta:
        ordering = ["result", "question"]
