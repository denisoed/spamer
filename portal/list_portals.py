list_portals = [
    {
        'name': 'Hacker news',
        'url_auth': 'https://news.ycombinator.com/login',
        'url_submit': 'https://news.ycombinator.com/submit',
        'inp_login': 'acct',
        'inp_password': 'pw',
        'inp_title': 'title',
        'inp_url': 'url',
        'inp_text': 'text',
        'auth_by': '<form method="post" action="login">',
        'auth_complete': '<span class="pagetop">'
    },
    {
        'name': 'Golang news',
        'url_auth': 'https://www.golangnews.com/users/login',
        'url_submit': 'https://www.golangnews.com/stories/create',
        'inp_login': 'email',
        'inp_password': 'password',
        'inp_title': 'name',
        'inp_url': 'url',
        'inp_text': 'summary',
        'auth_by': '<form action="/users/login" method="post">',
        'auth_complete': '<li class="user_badge" alt="Google Go Links">'
    },
    {
        'name': 'Reddit',
        'url_auth': 'https://www.reddit.com/',
        'url_submit': 'https://www.reddit.com/api/live/create',
        'inp_login': 'user',
        'inp_password': 'passwd',
        'inp_title': 'title',
        'inp_text': 'description',
        'auth_by': 'action="https://www.reddit.com/post/login"',
        'auth_complete': '<span class="user">'
    },
    {
        'name': 'Habrahabr',
        'url_auth': 'https://id.tmtm.ru/login/',
        'url_submit': 'https://habrahabr.ru/sandbox/add/',
        'inp_login': 'email',
        'inp_password': 'password',
        'inp_title': 'title',
        'inp_url': 'url',
        'inp_text': 'text',
        'auth_by': '<form action="/ajax/login/" class="s-form login_form validateble" id="login_form" method="post" data-remote="true" novalidate >',
        'auth_complete': 'class="user-info__nickname"'
    }
]
