## Test Results {{ docker_name }}

## Test's: {{ report_status }}

| Test | Result |
| ----------------------- | --- |{% for test in test_report %}
| {{ test[0] }} | {{ test[1] }} |{% endfor %}


<main>
  
 ## ShellCheck Results
 
<details><summary>Expand</summary><blockquote><p>
{% for test in shell_check %}
<section markdown="1">
<details><summary>File: {{ test[0] }}</summary><p>

```
{{ test[1] }}
```

</p></details>
</blockquote></p></details>
</section>
{% endfor %}
 
{% for container in tag_data %}
<section markdown="1">

## {{ image }}:{{ container["tag"] }}
{% if gui == 'true' %}
[![{{ container["tag"] }}]({{ container["tag"] }}.png =600x*)]({{ container["tag"] }}.png)
{% endif %}
### Build Version: {{ container["git_version"] }}

### Logs

<details><summary>Expand</summary><p>

```
{{ container["logs"] }}
```

</p></details>

### Package Info

<details><summary>Expand</summary><p>

```
{{ container["packages"] }}
```

</p></details>
</section>
{% endfor %}
</main>
