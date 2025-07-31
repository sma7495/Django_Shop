
{% extends "mail_templated/base.tpl" %}

{% block subject %}
Verification Message
{% endblock %}

{% block body %}
your new password: {{password}}
{% endblock %}

{% block html %}
<p> your new password: {{password}} </p>
{% endblock %}