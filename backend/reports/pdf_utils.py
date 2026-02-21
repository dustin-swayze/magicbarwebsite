from io import BytesIO
from decimal import Decimal

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


def money(value):
    try:
        return f"${Decimal(value):,.2f}"
    except Exception:
        return "$0.00"


def build_closing_report_pdf(report) -> bytes:
    """
    Returns PDF bytes for a ClosingReport.
    Generates on-demand; nothing saved to disk.
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)
    width, height = LETTER

    left = 0.75 * inch
    y = height - 0.75 * inch
    line = 14  # line spacing

    def draw_line(text, bold=False):
        nonlocal y
        if y < 0.75 * inch:
            c.showPage()
            y = height - 0.75 * inch
        c.setFont("Helvetica-Bold" if bold else "Helvetica", 11)
        c.drawString(left, y, text)
        y -= line

    # Header
    draw_line("Closing Report", bold=True)
    draw_line(f"Business Date: {report.business_date}")
    draw_line(f"Submitted: {report.created_at:%Y-%m-%d %H:%M}")
    draw_line(f"Submitted By: {getattr(report.created_by, 'username', str(report.created_by))}")
    draw_line("")

    # Staff
    bartenders = ", ".join([s.name for s in report.bartenders.all()]) or "—"
    barbacks = ", ".join([s.name for s in report.barbacks.all()]) or "—"
    security = ", ".join([s.name for s in report.security.all()]) or "—"

    draw_line("Staff", bold=True)
    draw_line(f"Bartenders: {bartenders}")
    draw_line(f"Barbacks: {barbacks}")
    draw_line(f"Security: {security}")
    draw_line("")

    # Money
    draw_line("Money", bold=True)
    draw_line(f"Total Cash: {money(report.total_cash)}")
    draw_line(f"Cash Payments: {money(report.cash_payments)}")
    draw_line("")

    # 86 list
    draw_line("86 List", bold=True)
    text = report.eighty_six_list.strip() or "—"
    for part in text.splitlines():
        draw_line(part)

    draw_line("")

    # Shift notes
    draw_line("Shift Notes", bold=True)
    notes = report.shift_notes.strip() or "—"
    for part in notes.splitlines():
        draw_line(part)

    draw_line("")

    # Paid outs
    draw_line("Paid Outs", bold=True)
    paid_outs = list(report.paid_outs.all())
    if not paid_outs:
        draw_line("—")
    else:
        for p in paid_outs:
            draw_line(f"- {p.who} | {money(p.amount)} | {p.description}")

    # Footer / emailed status
    draw_line("")
    if report.emailed_at:
        draw_line(f"Emailed: {report.emailed_at:%Y-%m-%d %H:%M}", bold=True)
    else:
        draw_line("Emailed: Not yet", bold=True)

    c.showPage()
    c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes