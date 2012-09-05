SERVICES = {
    "nginx":
        {
            "port": 27190,
            "start": ["nginx", "-c", "{project_dir}/nginx.conf"],
            "restart": ["kill", "-s", "SIGHUP", "{pid}"],
            "templates": ["nginx.conf.template"],
        },
    "gunicorn":
        {
            "port": 18650,
            "before": ["python", "manage.py", "collectstatic", "--noinput"],
            "start": ["gunicorn", "-D", "-c", "settings_gunicorn.py", "{{ project_name }}.wsgi:application"],
            "restart": ["kill", "-s", "SIGHUP", "{pid}"],
        },
}

