from django import forms
from django.forms import inlineformset_factory
from .models import ClosingReport, PaidOut, StaffMember, StaffRole


class ClosingReportForm(forms.ModelForm):
    bartenders = forms.ModelMultipleChoiceField(
        queryset=StaffMember.objects.filter(role=StaffRole.BARTENDER, active=True),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    barbacks = forms.ModelMultipleChoiceField(
        queryset=StaffMember.objects.filter(role=StaffRole.BARBACK, active=True),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    security = forms.ModelMultipleChoiceField(
        queryset=StaffMember.objects.filter(role=StaffRole.SECURITY, active=True),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = ClosingReport
        fields = [
            "business_date",
            "bartenders", "barbacks", "security",
            "total_cash", "cash_payments",
            "eighty_six_list", "shift_notes",
        ]
        widgets = {
            "business_date": forms.DateInput(attrs={"type": "date"}),
            "eighty_six_list": forms.Textarea(attrs={"rows": 3}),
            "shift_notes": forms.Textarea(attrs={"rows": 4}),
        }

    def clean(self):
        cleaned = super().clean()

        bartenders = cleaned.get("bartenders") or []
        barbacks = cleaned.get("barbacks") or []
        security = cleaned.get("security") or []

        if len(bartenders) > 4:
            self.add_error("bartenders", "Select up to 4 bartenders.")
        if len(barbacks) > 2:
            self.add_error("barbacks", "Select up to 2 barbacks.")
        if len(security) > 2:
            self.add_error("security", "Select up to 2 security guards.")

        return cleaned


PaidOutFormSet = inlineformset_factory(
    ClosingReport,
    PaidOut,
    fields=("who", "amount", "description"),
    extra=0,                # <-- important change
    can_delete=True,
)