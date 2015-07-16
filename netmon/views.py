import os

from django.views.generic import TemplateView, FormView

from forms import DNSForm, PingForm, TraceForm


class NetMonView(TemplateView):
    template_name = 'netmon.html'


class CDPView(TemplateView):
    template_name = "cdp.html"

    def get_context_data(self, **kwargs):
        context = super(CDPView, self).get_context_data(**kwargs)
        cdp_file = "/tmp/cdp.pcap"
        if os.path.isfile(cdp_file):
            command = "/usr/bin/tshark " \
                      "-r {} -V".format(cdp_file)
            output = os.popen(command).read()
        else:
            output = "No existe cdp_file. Intenta unos segundos mas tarde."
        context['output'] = output
        return context


class LLDPView(TemplateView):
    template_name = "lldp.html"

    def get_context_data(self, **kwargs):
        context = super(LLDPView, self).get_context_data(**kwargs)
        lldp_file = "/tmp/lldp.pcap"
        if os.path.isfile(lldp_file):
            command = "/usr/bin/tshark " \
                      "-r {} -V".format(lldp_file)
            output = os.popen(command).read()
        else:
            output = "No existe lldp_file. Intenta unos segundos mas tarde."
        context['output'] = output
        return context


class DHCPView(TemplateView):
    template_name = "dhcp.html"

    def get_context_data(self, **kwargs):
        interface = 'eth0'
        context = super(DHCPView, self).get_context_data(**kwargs)
        command = 'cat /sys/class/net/{}/address'.format(interface)
        mac = os.popen(command).read().strip()
        command = '/usr/local/bin/dhtest ' \
                  '-m {} -V -i {}'.format(mac, interface)
        resultado = os.popen(command).read()
        resultado = ''.join([i if ord(i) < 128 else ' ' for i in resultado])
        context['mac'] = mac
        context['resultado'] = resultado
        return context


class DNSView(FormView):
    template_name = "dns.html"
    form_class = DNSForm

    def form_valid(self, form):
        domain = form.cleaned_data['domain']
        dns_server = form.cleaned_data['dns_server']
        if dns_server:
            dns_server = "@{}".format(dns_server)
        command = "/usr/bin/timeout 10 /usr/bin/dig {} {} any".format(dns_server, domain)
        resultado = os.popen(command).read()
        if not resultado:
            resultado = "Timeout. Intentar de nuevo."
        return self.render_to_response(
            self.get_context_data(
                form=form,
                output=resultado,
            )
        )

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response(
            self.get_context_data(
                form=form,
            )
        )


class PingView(FormView):
    template_name = "ping.html"
    form_class = PingForm

    def form_valid(self, form):
        target = form.cleaned_data['target']
        command = "/usr/bin/timeout 10 /bin/ping -c 3 -W 1 {}".format(target)
        resultado = os.popen(command).read()
        return self.render_to_response(
            self.get_context_data(
                form=form,
                output=resultado,
            )
        )

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response(
            self.get_context_data(
                form=form,
            )
        )


class TraceView(FormView):
    template_name = "trace.html"
    form_class = TraceForm

    def form_valid(self, form):
        target = form.cleaned_data['target']
        command = "/usr/bin/timeout 10 /usr/bin/traceroute -n -w 1 -m 8 {}".format(target)
        resultado = os.popen(command).read()
        return self.render_to_response(
            self.get_context_data(
                form=form,
                output=resultado,
            )
        )

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return self.render_to_response(
            self.get_context_data(
                form=form,
            )
        )
