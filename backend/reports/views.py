from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.http import HttpResponse

from .forms import ClosingReportForm, PaidOutFormSet
from .models import ClosingReport
from .pdf_utils import build_closing_report_pdf


def management_recipients():
    return getattr(settings, "CLOSING_REPORT_RECIPIENTS", [])


@login_required
def closing_create(request):
    if request.method == "POST":
        form = ClosingReportForm(request.POST)
        report = ClosingReport(created_by=request.user)  # temporary instance for formset binding
        formset = PaidOutFormSet(request.POST, instance=report)

        if form.is_valid() and formset.is_valid():
            report = form.save(commit=False)
            report.created_by = request.user
            report.save()
            form.save_m2m()

            formset.instance = report
            formset.save()

            return redirect("reports_closing_preview", report_id=str(report.id))
    else:
        form = ClosingReportForm()
        formset = PaidOutFormSet()

    return render(request, "reports/closing_form.html", {"form": form, "formset": formset})


@login_required
def closing_preview(request, report_id):
    report = get_object_or_404(ClosingReport, id=report_id)
    return render(request, "reports/closing_preview.html", {"report": report})


@login_required
def closing_send(request, report_id):
    report = get_object_or_404(ClosingReport, id=report_id)

    # Only allow POST to send email
    if request.method != "POST":
        return redirect("reports_closing_preview", report_id=str(report.id))

    if report.emailed_at:
        messages.warning(request, "This report has already been emailed.")
        return redirect("reports_closing_preview", report_id=str(report.id))

    recipients = management_recipients()
    if not recipients:
        messages.error(request, "No management recipients configured. Ask an admin to set CLOSING_REPORT_RECIPIENTS.")
        return redirect("reports_closing_preview", report_id=str(report.id))

    subject = f"Closing Report — {report.business_date:%Y-%m-%d}"

    context = {"report": report}
    text_body = render_to_string("reports/email_report.txt", context)
    html_body = render_to_string("reports/email_report.html", context)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
        to=recipients,
    )
    msg.attach_alternative(html_body, "text/html")

    pdf_bytes = build_closing_report_pdf(report)
    filename = f"closing-report-{report.business_date:%Y-%m-%d}.pdf"
    msg.attach(filename, pdf_bytes, "application/pdf")

    msg.send()

    report.emailed_at = timezone.now()
    report.emailed_by = request.user
    report.save(update_fields=["emailed_at", "emailed_by"])

    return render(request, "reports/closing_done.html", {"report": report})

@login_required
def closing_pdf(request, report_id):
    report = get_object_or_404(ClosingReport, id=report_id)

    pdf_bytes = build_closing_report_pdf(report)
    filename = f"closing-report-{report.business_date:%Y-%m-%d}.pdf"

    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response