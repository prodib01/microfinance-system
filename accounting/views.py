from django.shortcuts import render
from .models import JournalEntries, Account


def journalentries(request, account_id):
    journalentries = JournalEntries.objects.filter(account=account_id).order_by(
        "-created_at"
    )
    account = Account.objects.get(pk=account_id)
    return render(
        request,
        "pages/accountinfo.html",
        {"journalentries": journalentries, "account": account},
    )
