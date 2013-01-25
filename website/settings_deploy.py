SERVICES = {
    "nginx":
        {
            "port": 25684,
            "gunicorn_port": 14449,
            "templates": ["{project_dir}/nginx.conf.template"],
            "start": ["nginx", "-c", "{project_dir}/nginx.conf"],
            "restart": ["kill", "-s", "SIGHUP", "{pid}"],
        },
    "gunicorn":
        {
            "port": 14449,
            "templates": ["{project_dir}/settings_gunicorn.py.template"],
            "before": ["./before_deploy.sh"],
            "start": ["gunicorn", "-D", "-c", "settings_gunicorn.py", "{{ project_name }}.wsgi:application"],
            "after": ["./after_deploy.sh"],
            "restart": ["kill", "-s", "SIGHUP", "{pid}"],
        },
}

