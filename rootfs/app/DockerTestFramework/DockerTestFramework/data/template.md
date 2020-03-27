## Test Results {{ docker_name }}

## Test's: {{ report_status }}

| Test | Result |
| ----------------------- | --- |{% for test in test_report %}
| {{ test[0] }} | {{ test[1] }} |{% endfor %}

<div data-role="main" class="ui-content">
<div data-role="collapsible"><h2>ShellCheck Results</h2><p>
{% for test in shell_check %}
<div data-role="collapsible"><h2>File: {{ test[0] }}</h2>
<p>
<section markdown="1"> 

```
{{ test[1] }}
```

</p></div>
{% endfor %}
</p></div></div>

<main>
{% for container in tag_data %}
<section markdown="1">
## {{ image }}:{{ container["tag"] }}
{% if gui == 'true' %}
[![{{ container["tag"] }}]({{ container["tag"] }}.png =600x*)]({{ container["tag"] }}.png)
{% endif %}
### Build Version: {{ container["git_version"] }}

<div data-role="collapsible"><h2>Logs</h2><p>

```
{{ container["logs"] }}
```

</p></div>


<div data-role="collapsible"><h2>Package Info</h2><p>

```
{{ container["packages"] }}
```

</p></div>

</section>
{% endfor %}
</main>