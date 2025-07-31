
{% extends "mail_templated/base.tpl" %}
{% block subject %}
Verification Message
{% endblock %}

{% block body %}
Please Click on link blow:
{% endblock %}

{% block html %}
<a href = "http://{{host_name}}{% url 'account:api:verify' token%}" > Click here to verify </a>
{% endblock %}