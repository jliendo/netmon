from django import forms


class DNSForm(forms.Form):
    dns_server = forms.CharField(
        required=False,
        max_length=254,
    )
    domain = forms.CharField(
        required=True,
        max_length=254,
    )

class PingForm(forms.Form):
    target = forms.GenericIPAddressField(
        required=True,
    )


class TraceForm(forms.Form):
    target = forms.GenericIPAddressField(
        required=True,
    )
