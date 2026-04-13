from django.db import models

# DNS proxy state is managed via files (blocked_domains.txt, dns_proxy.log)
# and subprocess control, so no database models are needed.
